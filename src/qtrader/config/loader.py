import os
import sys
from pathlib import Path
import yaml
import json

from .merge import deep_merge
from .templating import render_template


# -------------------------
# Platform architecture
# -------------------------
def detect_arch() -> str:
    if sys.platform == "darwin":
        return "m64"
    if sys.platform.startswith("linux"):
        return "l64"
    if sys.platform.startswith("win"):
        return "w64"
    raise RuntimeError(f"Unsupported platform: {sys.platform}")


# -------------------------
# Variable expander
# -------------------------
def expand_vars(vars_dict: dict, stack_name: str) -> dict:
    """
    Expand placeholders like:
      qbin: "{qhome}/{arch}/q"
      data: "{data_root}/{stack_name}"

    Expansion is run twice since some vars depend on other vars.
    """
    for _ in range(2):
        for k, v in vars_dict.items():
            if isinstance(v, str):
                try:
                    vars_dict[k] = v.format(
                        stack_name=stack_name,
                        **vars_dict
                    )
                except Exception as e:
                    raise ValueError(f"Error expanding var '{k}': {e}")
    return vars_dict


# -------------------------
# YAML Loader
# -------------------------
def load_stack(stack: str, mode: str = "dev"):
    """
    Load a stack configuration:
      - base.yaml
      - env.<mode>.yaml (optional)

    Steps:
      1. Apply Jinja templating (env, arch, stack_name)
      2. Deep merge configs
      3. Expand vars.* placeholders
      4. Write final merged+expanded JSON for q processes
    """
    stack_dir = Path("stacks") / stack
    if not stack_dir.exists():
        raise FileNotFoundError(f"Stack not found: {stack_dir}")

    base_file = stack_dir / "base.yaml"
    if not base_file.exists():
        raise FileNotFoundError(f"No base.yaml in {stack_dir}")

    overlay_file = stack_dir / f"env.{mode}.yaml"

    stack_name = stack
    arch = detect_arch()
    env = os.environ

    # ---- Load + template base.yaml ----
    base_raw = base_file.read_text()
    rendered_base = render_template(
        base_raw,
        env=env,
        arch=arch,
        stack_name=stack_name
    )
    base_cfg = yaml.safe_load(rendered_base) or {}

    # ---- Load + template overlay ----
    if overlay_file.exists():
        overlay_raw = overlay_file.read_text()
        rendered_overlay = render_template(
            overlay_raw,
            env=env,
            arch=arch,
            stack_name=stack_name
        )
        overlay_cfg = yaml.safe_load(rendered_overlay) or {}
    else:
        overlay_cfg = {}

    # ---- Merge ----
    cfg = deep_merge(base_cfg, overlay_cfg)

    # ---- Expand vars.* ----
    vars_cfg = cfg.get("vars", {})
    cfg["vars"] = expand_vars(vars_cfg, stack_name)

    # ---- Write final JSON for q ----
    json_out = stack_dir / f"{stack}.json"
    json_out.write_text(json.dumps(cfg, indent=2))

    return cfg