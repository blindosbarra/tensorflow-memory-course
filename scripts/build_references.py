"""Rebuild `docs/references.md` from the `## Fonti` sections of the lessons.

The aggregate page used to be maintained by hand and drifted: it listed six
links, all from lessons 1-2, while all 67 published lesson pages carry their
own sources. Generating it means it cannot drift again.

Usage:
    uv run python scripts/build_references.py           # rewrite the page
    uv run python scripts/build_references.py --check   # fail if out of date

`--check` is what tells you the page needs regenerating after editing a
lesson's sources; it writes nothing and exits 1 on a difference.

Where the content comes from:

- the lesson pages are `docs/modules/*.md`, one per lesson id;
- `docs/modules/en/` is skipped — those are translations of the PMLE pages,
  and their sources already appear under the Italian originals;
- module and lesson order follow `course/course.yaml`, so the output order is
  a property of the course, not of the filesystem.

Sources are de-duplicated by URL within a module: one entry per URL, keeping
the description from its first occurrence and listing every lesson that cites
it. A bullet with no URL is not an external source (the one case today is a
cross-reference to sibling lessons); those are skipped and reported on stderr
rather than dropped in silence.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import NamedTuple

import yaml

COURSE_PATH = Path("course/course.yaml")
MODULES_DIR = Path("docs/modules")
OUTPUT_PATH = Path("docs/references.md")

FONTI_RE = re.compile(r"^## Fonti\s*\n(.*?)(?=^## |\Z)", re.S | re.M)
# A bullet runs until the next bullet or a blank line; continuation lines are
# indented, which is how the multi-line entries in these pages are written.
BULLET_RE = re.compile(r"^- (.*(?:\n(?!\s*-\s|\s*$).*)*)", re.M)
URL_RE = re.compile(r"https?://[^\s<>()\[\]]+")

HEADER = """# Riferimenti

Tutte le fonti citate dalle lezioni, raggruppate per modulo.

<!-- Pagina generata da scripts/build_references.py: non modificarla a mano.
     Le fonti si aggiungono nella sezione "## Fonti" della lezione, poi si
     rigenera con `uv run python scripts/build_references.py`. -->
"""


class Source(NamedTuple):
    """One cited source, with the lessons that cite it."""

    description: str
    url: str
    lessons: list[str]


def load_module_order() -> list[tuple[str, list[str]]]:
    """Return `(module id, lesson ids)` in the order the course declares them."""

    course = yaml.safe_load(COURSE_PATH.read_text(encoding="utf-8"))
    order: list[tuple[str, list[str]]] = []
    for module in course.get("modules") or []:
        lessons = [
            lesson["id"] if isinstance(lesson, dict) else lesson
            for lesson in module.get("lessons") or []
        ]
        order.append((module["id"], lessons))
    return order


def clean_description(bullet: str, urls: list[str]) -> str:
    """Collapse a bullet to one line and take the URLs out of the prose."""

    text = " ".join(bullet.split())
    for url in urls:
        text = text.replace(f"<{url}>", "").replace(url, "")
    # what tends to be left behind once the link is gone
    text = re.sub(r"\s*[—–-]\s*$", "", text.strip())
    text = re.sub(r"[\s:;,.]+$", "", text.strip())
    return text.strip()


def read_sources(page: Path) -> list[tuple[str, str]]:
    """Return `(description, url)` for every source cited by one lesson page."""

    match = FONTI_RE.search(page.read_text(encoding="utf-8"))
    if not match:
        return []

    found: list[tuple[str, str]] = []
    for bullet in BULLET_RE.findall(match.group(1)):
        urls = URL_RE.findall(bullet)
        if not urls:
            print(
                f"  nessun URL, ignorata: {page.name}: {' '.join(bullet.split())[:70]}",
                file=sys.stderr,
            )
            continue
        description = clean_description(bullet, urls)
        # A bullet occasionally carries more than one link; each is a source.
        for index, url in enumerate(urls):
            found.append((description if index == 0 else f"{description} (segue)", url))
    return found


def collect() -> list[tuple[str, list[Source]]]:
    """Gather every module's sources, de-duplicated by URL."""

    collected: list[tuple[str, list[Source]]] = []
    for module_id, lesson_ids in load_module_order():
        by_url: dict[str, Source] = {}
        for lesson_id in lesson_ids:
            page = MODULES_DIR / f"{lesson_id}.md"
            if not page.exists():
                continue  # lesson declared in course.yaml but not written yet
            for description, url in read_sources(page):
                existing = by_url.get(url)
                if existing is None:
                    by_url[url] = Source(description, url, [lesson_id])
                elif lesson_id not in existing.lessons:
                    existing.lessons.append(lesson_id)
        if by_url:
            collected.append((module_id, list(by_url.values())))
    return collected


def render(collected: list[tuple[str, list[Source]]]) -> str:
    """Render the page. Ordering is fully determined by the inputs."""

    lines = [HEADER]
    for module_id, sources in collected:
        lines.append(f"## {module_id}\n")
        for source in sources:
            cited = ", ".join(source.lessons)
            description = source.description or source.url
            lines.append(f"- {description} — <{source.url}> ({cited})")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild docs/references.md.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit 1 if the page is out of date",
    )
    args = parser.parse_args()

    collected = collect()
    page = render(collected)

    if args.check:
        current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if current != page:
            print(
                f"{OUTPUT_PATH} non e' aggiornata: rigenerala con "
                "`uv run python scripts/build_references.py`",
                file=sys.stderr,
            )
            return 1
        print(f"{OUTPUT_PATH}: aggiornata")
        return 0

    OUTPUT_PATH.write_text(page, encoding="utf-8")
    total = sum(len(sources) for _, sources in collected)
    print(f"{OUTPUT_PATH}: {total} fonti da {len(collected)} moduli")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
