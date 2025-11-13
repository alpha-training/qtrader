# cli/__main__.py
import typer
from rich import print

from qtrader.config.loader import load_stack
from qtrader.runtime.process_plan import build_launch_plan
from qtrader.runtime.launcher import start_stack, stop_stack

app = typer.Typer(help="qtrader command-line interface")

@app.command()
def up(stack: str, mode: str = "dev"):
    """Start a stack."""
    cfg = load_stack(stack, mode)
    plan = build_launch_plan(cfg)
    start_stack(stack, mode, plan)

@app.command()
def down(stack: str, mode: str = "dev"):
    """Stop a running stack."""
    stop_stack(stack, mode)

def main():
    app()

if __name__ == "__main__":
    main()