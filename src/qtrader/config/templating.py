# config/templating.py
from jinja2 import Template

def render_template(text: str, *, env: dict, arch: str, stack_name: str) -> str:
    """
    Renders a YAML text using Jinja2, injecting env, arch, and stack_name.
    """
    tmpl = Template(text)
    return tmpl.render(
        env=env,
        arch=arch,
        stack_name=stack_name,
    )