"""Execute every notebook in an isolated copy and fail on errors."""

from __future__ import annotations

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
    notebooks = sorted(Path("notebooks").rglob("*.ipynb"))
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
