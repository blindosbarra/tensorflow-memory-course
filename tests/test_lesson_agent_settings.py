"""Tests for `lesson_agent.settings` — key/model resolution, without leaking keys."""

from __future__ import annotations

import pytest

from lesson_agent import settings
from lesson_agent.constants import MODEL


def test_env_file_parsing_handles_comments_quotes_and_export(tmp_path, monkeypatch) -> None:
    env = tmp_path / ".env"
    env.write_text(
        "# commento\n"
        "\n"
        'GOOGLE_API_KEY="chiave-fra-virgolette"\n'
        "export LESSON_AGENT_MODEL=gemini-test\n"
        "RIGA_SENZA_UGUALE\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("LESSON_AGENT_MODEL", raising=False)

    assert settings.api_key(env) == "chiave-fra-virgolette"
    assert settings.model_name(env) == "gemini-test"


def test_shell_environment_wins_over_env_file(tmp_path, monkeypatch) -> None:
    """An explicit `export` is the more deliberate act; it must not be clobbered."""

    env = tmp_path / ".env"
    env.write_text("GOOGLE_API_KEY=dal-file\n", encoding="utf-8")
    monkeypatch.setenv("GOOGLE_API_KEY", "dalla-shell")

    assert settings.api_key(env) == "dalla-shell"


def test_model_defaults_to_the_pinned_constant(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("LESSON_AGENT_MODEL", raising=False)
    assert settings.model_name(tmp_path / "assente.env") == MODEL


def test_describe_key_never_returns_the_whole_key() -> None:
    key = "AIzaSy-questa-e-una-chiave-finta-1234"
    described = settings.describe_key(key)
    assert key not in described
    assert described.startswith("impostata")
    assert settings.describe_key(None) == "non impostata"


def test_write_env_key_preserves_other_entries_and_locks_permissions(
    tmp_path, monkeypatch
) -> None:
    env = tmp_path / ".env"
    env.write_text("LESSON_AGENT_MODEL=gemini-test\n", encoding="utf-8")
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    settings.write_env_key("nuova-chiave", env)

    written = settings._parse_env_file(env)
    assert written["GOOGLE_API_KEY"] == "nuova-chiave"
    assert written["LESSON_AGENT_MODEL"] == "gemini-test"
    assert env.stat().st_mode & 0o077 == 0, "il .env non deve essere leggibile da altri"


def test_write_env_key_rejects_blank(tmp_path) -> None:
    with pytest.raises(ValueError):
        settings.write_env_key("   ", tmp_path / ".env")


def test_readiness_is_not_ready_without_a_key(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    readiness = settings.check_readiness(tmp_path / "assente.env")
    assert not readiness.ready
    assert "GOOGLE_API_KEY" in readiness.reason


def test_readiness_is_ready_with_a_key(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("GOOGLE_API_KEY", "chiave-finta")
    readiness = settings.check_readiness(tmp_path / "assente.env")
    assert readiness.ready
