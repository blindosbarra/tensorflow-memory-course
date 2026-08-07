"""Execute every notebook end to end and fail on errors.

Usage:
    uv run python scripts/execute_notebooks.py                 # all notebooks
    uv run python scripts/execute_notebooks.py --only lezione-34-keras-hub

`--only` runs a subset, matched on the file stem, so a remediation item that
touches five notebooks can be gated in a minute instead of the fifteen the
full run costs. It is a development aid: the definition of done for anything
touching notebooks is still the full run with a clean `git status`.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient


def execute_notebook(path: Path) -> None:
    runtime_root = Path(".notebook-runtime").resolve()
    runtime_root.mkdir(exist_ok=True)
    for child in ("ipython", "jupyter_config", "jupyter_data", "jupyter_runtime"):
        (runtime_root / child).mkdir(exist_ok=True)
    os.environ.setdefault("IPYTHONDIR", str(runtime_root / "ipython"))
    os.environ.setdefault("JUPYTER_CONFIG_DIR", str(runtime_root / "jupyter_config"))
    os.environ.setdefault("JUPYTER_DATA_DIR", str(runtime_root / "jupyter_data"))
    os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(runtime_root / "jupyter_runtime"))

    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=600,
        kernel_name="python3",
        allow_errors=False,
    )
    client.execute(cwd=str(path.parent))


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute the course notebooks.")
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="STEM",
        help="run only these notebooks, matched on the file name without .ipynb",
    )
    args = parser.parse_args()

    notebooks = sorted(Path("notebooks").rglob("*.ipynb"))
    if args.only:
        wanted = {stem.removesuffix(".ipynb") for stem in args.only}
        notebooks = [path for path in notebooks if path.stem in wanted]
        missing = sorted(wanted - {path.stem for path in notebooks})
        if missing:
            print(f"No such notebook: {', '.join(missing)}", file=sys.stderr)
            return 2
    if not notebooks:
        print("No notebooks found.")
        return 0

    failures: list[tuple[Path, Exception]] = []
    for path in notebooks:
        print(f"Executing {path}")
        try:
            execute_notebook(path)
        except Exception as exc:  # noqa: BLE001
            failures.append((path, exc))

    if failures:
        for path, exc in failures:
            print(f"FAILED {path}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
