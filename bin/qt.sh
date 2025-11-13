#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root (bin/ is alongside this file)
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Let the Python CLI know where the repo root is
export QTRADER_ROOT="$REPO_ROOT"

# Hand off to the installed qtrader CLI (inside venv, ideally)
exec qtrader "$@"