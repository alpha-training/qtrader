# cli/__main__.py
# Minimal, cross-platform CLI to orchestrate q/qi/qtrader
import os
import sys
import time
import json
import shutil
import signal
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="qtrader command-line interface")
console = Console()


# ---------- paths & discovery ----------

def repo_root() -> Path:
    # Set by bin/qt shim; fallback to CWD for direct runs
    env = os.environ.get("QTRADER_ROOT")
    return Path(env).resolve() if env else Path.cwd().resolve()


def qi_path() -> Path:
    """
    Resolve qi.q. If not found locally, download a fresh copy.
    """
    import urllib.request

    # 1) Env override
    if p := os.environ.get("QTRADER_QI_PATH"):
        qp = Path(p).expanduser().resolve()
        if qp.exists():
            return qp

    # 2) Local bundled qi/qi.q
    local = repo_root() / "qi" / "qi.q"
    if local.exists():
        return local

    # 3) Download if missing
    url = os.environ.get("QTRADER_QI_URL", "https://alphakdb.com/code/qi.q")
    local.parent.mkdir(parents=True, exist_ok=True)

    try:
        print(f"[yellow]Downloading qi.q from {url}…[/yellow]")
        urllib.request.urlretrieve(url, local)
        print(f"[green]Downloaded qi.q → {local}[/green]")
        return local
    except Exception as e:
        print(f"[bold red]Error:[/bold red] could not fetch qi.q: {e}")
        raise typer.Exit(1)

def get_stack_paths(stack: str) -> dict:
    root = repo_root()
    sdir = root / "stacks" / stack
    base = sdir / "base.json"
    if not base.exists():
        print(f"[bold red]Missing base.json:[/bold red] {base}")
        raise typer.Exit(1)
    return {
        "root": root,
        "stack_dir": sdir,
        "base": base,
        "runtime": sdir / "runtime",
        "conf_defaults": (root / "conf" / "defaults.json"),
        "conf_local": (root / "conf" / "local.json"),
    }


def overlay_path(stack_dir: Path, mode: str) -> Optional[Path]:
    p = stack_dir / f"env.{mode}.json"
    return p if p.exists() else None


# ---------- q binary discovery ----------

def find_qbin() -> Path:
    """
    Priority:
      1) Q_BIN env (explicit override)
      2) QHOME + QARCH + OS default (m64/l64/w64) + .exe on Windows
      3) QHOME direct (q placed directly under QHOME)
      4) PATH lookup (shutil.which("q"))
    """
    # 1) Explicit override
    qbin_env = os.environ.get("Q_BIN")
    if qbin_env:
        qb = Path(qbin_env).expanduser().resolve()
        if qb.exists():
            return qb
        raise_runtime("Q_BIN is set but points to a non-existent file", qb)

    # 2) QHOME + arch
    qhome = os.environ.get("QHOME")
    if qhome:
        qhomep = Path(qhome).expanduser().resolve()
        if not qhomep.exists():
            raise_runtime("QHOME points to a non-existent directory", qhomep)

        exe = "q.exe" if is_windows() else "q"
        qarch_env = os.environ.get("QARCH")

        # OS default arch folder
        default_arch = "w64" if is_windows() else ("m64" if is_mac() else "l64")

        candidates = []
        if qarch_env:
            candidates.append(qarch_env)
        candidates.append(default_arch)
        candidates += ["m64", "l64", "w64", ""]  # fallbacks; "" = directly under QHOME

        for sub in candidates:
            cand = qhomep / sub / exe if sub else qhomep / exe
            if cand.exists():
                return cand

    # 4) PATH
    on_path = shutil.which("q.exe" if is_windows() else "q")
    if on_path:
        return Path(on_path).resolve()

    # If we reach here, nothing found
    msg = "Could not locate q binary. Set Q_BIN or QHOME (with m64/l64/w64) or put 'q' on PATH."
    if qhome:
        msg += f" (Checked QHOME={qhome})"
    print(f"[bold red]{msg}[/bold red]")
    raise typer.Exit(1)


def is_windows() -> bool:
    return sys.platform.startswith("win")


def is_mac() -> bool:
    return sys.platform == "darwin"


def raise_runtime(msg: str, path: Path) -> None:
    print(f"[bold red]Error:[/bold red] {msg}: {path}")
    raise typer.Exit(1)


# ---------- runtime files ----------

def pidfile(rundir: Path, mode: str) -> Path:
    return rundir / f"{mode}.pid"


def logfile(rundir: Path, mode: str) -> Path:
    return rundir / f"{mode}.log"


def read_pid(pf: Path) -> Optional[int]:
    try:
        return int(pf.read_text().strip())
    except Exception:
        return None


def is_running_pid(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        if is_windows():
            # tasklist check
            out = subprocess.check_output(["tasklist", "/FI", f"PID eq {pid}"], stderr=subprocess.DEVNULL)
            return str(pid).encode() in out
        else:
            os.kill(pid, 0)
            return True
    except Exception:
        return False


# ---------- process launch helpers ----------

def launch_detached(cmd: list[str], log_path: Path) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "ab", buffering=0) as lf:
        if is_windows():
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            CREATE_NO_WINDOW = 0x08000000
            flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=lf,
                stderr=lf,
                creationflags=flags,
                close_fds=True,
            )
        else:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=lf,
                stderr=lf,
                start_new_session=True,  # like setsid/nohup
                close_fds=True,
            )
    return proc.pid


def stop_process(pid: int, timeout: float = 5.0) -> bool:
    if not is_running_pid(pid):
        return True
    try:
        if is_windows():
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False)
            # best-effort wait
            t0 = time.time()
            while time.time() - t0 < timeout and is_running_pid(pid):
                time.sleep(0.2)
        else:
            # send SIGTERM to the process group if we launched with start_new_session
            try:
                os.killpg(pid, signal.SIGTERM)
            except Exception:
                os.kill(pid, signal.SIGTERM)
            t0 = time.time()
            while time.time() - t0 < timeout and is_running_pid(pid):
                time.sleep(0.2)
            if is_running_pid(pid):
                os.kill(pid, signal.SIGKILL)
    except Exception:
        return False
    return not is_running_pid(pid)


# ---------- commands ----------

@app.command()
def diag():
    """Print diagnostics for paths and q discovery."""
    root = repo_root()
    qp = qi_path()
    try:
        qb = find_qbin()
        qb_str = str(qb)
    except SystemExit:
        qb_str = "(not found)"
    info = {
        "QTRADER_ROOT": str(root),
        "QTRADER_QI_PATH": str(qp),
        "QHOME": os.environ.get("QHOME", "(unset)"),
        "QARCH": os.environ.get("QARCH", "(unset)"),
        "Q_BIN": os.environ.get("Q_BIN", "(unset)"),
        "q_binary": qb_str,
        "platform": sys.platform,
    }
    console.print(Panel.fit(json.dumps(info, indent=2), title="qtrader diag"))


@app.command()
def init(stack: str, mode: str = typer.Option("dev", "--mode", "-m")):
    """One-shot qi initialization (blocking)."""
    qb = find_qbin()
    qiq = qi_path()
    paths = get_stack_paths(stack)
    sdir, base = paths["stack_dir"], paths["base"]

    ov = overlay_path(sdir, mode)
    argv = [str(qb), str(qiq), "-init", str(base)]
    if ov:
        argv += ["--overlay", str(ov)]
    argv += ["--mode", mode]

    print(f"[cyan]Running init:[/cyan] {' '.join(argv)}")
    res = subprocess.run(argv)
    raise typer.Exit(res.returncode)


@app.command()
def up(stack: str, mode: str = typer.Option("dev", "--mode", "-m"), port: Optional[int] = None):
    """Start a qtrader stack (detached)."""
    qb = find_qbin()
    qiq = qi_path()
    paths = get_stack_paths(stack)
    sdir, base, rundir = paths["stack_dir"], paths["base"], paths["runtime"]
    rundir.mkdir(parents=True, exist_ok=True)

    pf, lf = pidfile(rundir, mode), logfile(rundir, mode)

    # If already running, short-circuit
    if pf.exists():
        pid = read_pid(pf)
        if pid and is_running_pid(pid):
            print(f"[yellow]Already running[/yellow] pid={pid} • log={lf}")
            raise typer.Exit(0)

    ov = overlay_path(sdir, mode)
    argv = [str(qb), str(qiq)]
    if port:
        argv += ["-p", str(port)]  # optional control port (if your q uses it)
    argv += ["-init", str(base)]
    if ov:
        argv += ["--overlay", str(ov)]
    argv += ["--mode", mode]

    print(f"[cyan]Launching (detached):[/cyan] {' '.join(argv)}")
    pid = launch_detached(argv, lf)
    pf.write_text(str(pid))
    print(f"[green]Started[/green] {stack} ({mode}) pid={pid} • log={lf}")


@app.command()
def down(stack: str, mode: str = typer.Option("dev", "--mode", "-m")):
    """Stop a running stack."""
    paths = get_stack_paths(stack)
    rundir = paths["runtime"]
    pf = pidfile(rundir, mode)
    if not pf.exists():
        print(f"[yellow]No PID file[/yellow] for {stack} ({mode}). Already down?")
        raise typer.Exit(0)
    pid = read_pid(pf)
    if not pid:
        print("[yellow]PID file unreadable[/yellow]; removing.")
        try: pf.unlink()
        except Exception: pass
        raise typer.Exit(0)

    if stop_process(pid):
        try: pf.unlink()
        except Exception: pass
        print(f"[green]Stopped[/green] {stack} ({mode}).")
    else:
        print(f"[red]Failed[/red] to stop pid {pid}.")
        raise typer.Exit(1)


@app.command()
def status(stack: str, mode: str = typer.Option("dev", "--mode", "-m")):
    """Show status of a stack."""
    try:
        paths = get_stack_paths(stack)
    except typer.Exit:
        return
    rundir = paths["runtime"]
    pf, lf = pidfile(rundir, mode), logfile(rundir, mode)
    if not pf.exists():
        print(f"[yellow]{stack} ({mode}) is not running[/yellow]")
        return
    pid = read_pid(pf)
    running = bool(pid and is_running_pid(pid))
    color = "green" if running else "red"
    print(f"[{color}]{stack} ({mode}) → pid {pid} • running={running} • log={lf}[/{color}]")


@app.command()
def logs(stack: str,
         mode: str = typer.Option("dev", "--mode", "-m"),
         follow: bool = typer.Option(False, "--follow", "-f")):
    """Show (and optionally follow) stack logs."""
    paths = get_stack_paths(stack)
    lf = logfile(paths["runtime"], mode)
    if not lf.exists():
        print(f"[yellow]No log file yet[/yellow]: {lf}")
        raise typer.Exit(0)

    if not follow:
        print(lf.read_text(errors="ignore"))
        return

    print(f"[cyan]Tailing[/cyan] {lf} (Ctrl+C to stop)")
    with open(lf, "rb") as f:
        # seek to end
        f.seek(0, os.SEEK_END)
        try:
            while True:
                chunk = f.read()
                if chunk:
                    sys.stdout.buffer.write(chunk)
                    sys.stdout.flush()
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\n[yellow]Stopped tailing[/yellow]")


def main():
    app()

if __name__ == "__main__":
    main()