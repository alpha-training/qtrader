# runtime/launcher.py

import os
import signal
import subprocess
import time
from pathlib import Path
import sys

def pidfile(stack_dir: Path, mode: str):
    return stack_dir / "runtime" / f"{mode}.pid"

def logfile(stack_dir: Path, mode: str):
    return stack_dir / "runtime" / f"{mode}.log"


def is_running_pid(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        # Windows
        if sys.platform.startswith("win"):
            out = subprocess.check_output(
                ["tasklist", "/FI", f"PID eq {pid}"],
                stderr=subprocess.DEVNULL
            )
            return str(pid).encode() in out
        # Unix
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def launch_detached(cmd: list[str], log_path: Path) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    lf = open(log_path, "ab", buffering=0)

    if sys.platform.startswith("win"):
        flags = (
            subprocess.CREATE_NEW_PROCESS_GROUP |
            subprocess.DETACHED_PROCESS |
            subprocess.CREATE_NO_WINDOW
        )
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=lf,
            stderr=lf,
            creationflags=flags
        )
    else:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=lf,
            stderr=lf,
            start_new_session=True,  # detached
        )
    return proc.pid


def start_stack(stack: str, mode: str, plan: dict):
    stack_dir = Path("stacks") / stack
    pf = pidfile(stack_dir, mode)
    lf = logfile(stack_dir, mode)

    # if running, skip
    if pf.exists():
        pid = int(pf.read_text())
        if is_running_pid(pid):
            print(f"[already running] pid={pid}")
            return

    # launch processes one by one in dependency order
    for name in plan["_order"]:
        proc_cfg = plan[name]
        pid = launch_detached(proc_cfg["cmd"], lf)
        print(f"[start] {name} pid={pid}")

    pf.write_text(str(pid))  # last process pid


def stop_stack(stack: str, mode: str):
    stack_dir = Path("stacks") / stack
    pf = pidfile(stack_dir, mode)

    if not pf.exists():
        print("No PID file")
        return

    pid = int(pf.read_text())

    if not is_running_pid(pid):
        print("Not running")
        try: pf.unlink()
        except: pass
        return

    print(f"Stopping pid {pid}...")

    if sys.platform.startswith("win"):
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"])
    else:
        try:
            os.killpg(pid, signal.SIGTERM)
        except Exception:
            os.kill(pid, signal.SIGTERM)

    time.sleep(0.5)

    if not is_running_pid(pid):
        print("[stopped]")
        pf.unlink()
    else:
        print("[failed to stop]")