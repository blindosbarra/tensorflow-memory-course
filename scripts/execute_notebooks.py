"""Execute every notebook in an isolated copy and fail on errors."""

from __future__ import annotations

from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient


def execute_notebook(path: Path) -> None:
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
