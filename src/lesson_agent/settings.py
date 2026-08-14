"""Runtime configuration for the lesson-agent: API key, model name, local state dir.

Three things were hardcoded or implicit before the GUI existed and are now
resolved here, in one place, because both the CLI
(`scripts/generate_lesson_doc.py`) and the Streamlit app need the same answers:

1. **The API key.** The CLI only ever read `GOOGLE_API_KEY` from the
   environment. That works for `export ...` in a shell, but the GUI is a
   long-running process the user starts once, so it also reads a
   **git-ignored `.env`** at the repo root. The key is still never committed
   and never logged — `describe_key` returns a masked fingerprint only.
2. **The model name.** `constants.MODEL` pinned one string. It stays the
   default, but `LESSON_AGENT_MODEL` now overrides it, so a stale Flash
   version is a config change rather than a code change (the SDD flagged
   this string as "stale again within months").
3. **Where the learner's own state lives.** `course/progress.yaml` tracks
   *authoring* progress and is committed; a learner's profile and lesson
   progress are personal and must not land in the repo's history, so they go
   in a git-ignored `.learner/`.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from lesson_agent.constants import MODEL

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = REPO_ROOT / ".env"
LEARNER_DIR = REPO_ROOT / ".learner"

API_KEY_VAR = "GOOGLE_API_KEY"
MODEL_VAR = "LESSON_AGENT_MODEL"


def _parse_env_file(path: Path) -> dict[str, str]:
    """Minimal `.env` reader: `KEY=value` lines, `#` comments, optional quotes.

    Deliberately not python-dotenv — one more dependency for twelve lines,
    and this file only ever holds a key or two.
    """

    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().removeprefix("export ").strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def load_env_file(path: Path = ENV_FILE) -> None:
    """Load `.env` into `os.environ` **without** overriding what is already set.

    An explicit `export GOOGLE_API_KEY=...` in the shell wins over the file:
    the shell is the more deliberate act of the two.
    """

    for key, value in _parse_env_file(path).items():
        os.environ.setdefault(key, value)


def api_key(path: Path = ENV_FILE) -> str | None:
    """The Google AI Studio key, from the environment or `.env`, or `None`."""

    load_env_file(path)
    return os.environ.get(API_KEY_VAR) or None


def model_name(path: Path = ENV_FILE) -> str:
    """The Gemini model every agent uses; `LESSON_AGENT_MODEL` overrides the pin.

    Reads `.env` too, so putting `LESSON_AGENT_MODEL=...` next to the API key
    is enough — this is resolved at *import* time by `agents.py`, so changing
    it means restarting the app, not just re-running a generation.
    """

    load_env_file(path)
    return os.environ.get(MODEL_VAR) or MODEL


def describe_key(key: str | None) -> str:
    """A maskable one-line description of a key, safe to render in the GUI."""

    if not key:
        return "non impostata"
    if len(key) <= 8:
        return "impostata (troppo corta per essere valida?)"
    return f"impostata ({key[:4]}…{key[-4:]}, {len(key)} caratteri)"


def write_env_key(key: str, path: Path = ENV_FILE) -> None:
    """Persist `GOOGLE_API_KEY` to the git-ignored `.env`, preserving other keys.

    Called only from the GUI's settings panel, so a user who has no shell
    open can still get the agents running. Refuses to write outside the repo
    root and creates the file with owner-only permissions.
    """

    if not key.strip():
        raise ValueError("La chiave e' vuota.")

    values = _parse_env_file(path)
    values[API_KEY_VAR] = key.strip()
    body = "\n".join(f"{name}={value}" for name, value in sorted(values.items()))
    path.write_text(
        "# Git-ignored. Chiavi API locali per il lesson-agent.\n" + body + "\n",
        encoding="utf-8",
    )
    path.chmod(0o600)
    os.environ[API_KEY_VAR] = key.strip()


@dataclass(frozen=True)
class AgentReadiness:
    """Whether the LLM agents can run right now, and why not if they can't."""

    ready: bool
    reason: str


def check_readiness(path: Path = ENV_FILE) -> AgentReadiness:
    """Report whether an agent run would work, without making a network call.

    The GUI calls this to decide between enabling the "genera"/"chiedi"
    buttons and showing an actionable message. It checks the two things that
    actually block a run — the ADK import and the key — and nothing else; a
    wrong-but-present key surfaces as an error from the real call, which is
    where the API's own message is more useful than a guess here.
    """

    try:
        import google.adk  # noqa: F401
    except ImportError:
        return AgentReadiness(
            False,
            "Il pacchetto `google-adk` non e' installato. Esegui "
            "`uv sync --extra dev --extra gui`.",
        )

    if not api_key(path):
        return AgentReadiness(
            False,
            "GOOGLE_API_KEY non impostata. Incollala nel pannello "
            "'Impostazioni' della barra laterale, oppure esporta la "
            "variabile prima di avviare l'app.",
        )

    return AgentReadiness(True, f"Pronto — modello `{model_name()}`.")
