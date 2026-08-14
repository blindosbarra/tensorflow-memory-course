"""Smoke tests for the GUI, via Streamlit's own headless harness.

`AppTest` runs `app/streamlit_app.py` exactly as the server would — same
script, same widget state machine — and collects any exception the script
raised. That is enough to catch the failure mode that matters here: the app
renders 70 lessons and 61 notebooks it does not control, and one lesson with
an unexpected shape (no doc page, no notebook, an error output) used to be
enough to blank the page.

No API key is involved: every agent call sits behind a button these tests do
not press, and `check_readiness` disables those buttons when there is no key.
"""

from __future__ import annotations

import pytest

pytest.importorskip("streamlit", reason="la GUI richiede l'extra `gui`")

from pathlib import Path  # noqa: E402

from streamlit.testing.v1 import AppTest  # noqa: E402

# Absolute: `AppTest.from_file` resolves relative paths against the *calling*
# file, i.e. `tests/`, not the repo root.
APP = str(Path(__file__).resolve().parents[1] / "app" / "streamlit_app.py")


@pytest.fixture(autouse=True)
def isolated_learner_state(tmp_path, monkeypatch):
    """Never let a test write into the developer's real `.learner/`.

    One patch point is enough: `profile` and `catalog` both resolve
    `settings.LEARNER_DIR` at call time rather than binding it as a default
    argument, precisely so this redirection works.
    """

    monkeypatch.setattr("lesson_agent.settings.LEARNER_DIR", tmp_path)
    return tmp_path


def _run(page: str | None = None) -> AppTest:
    app = AppTest.from_file(APP, default_timeout=180)
    app.run()
    if page is not None:
        app.radio[0].set_value(page).run()
    assert not app.exception, [str(e.value) for e in app.exception]
    return app


def test_percorso_page_renders() -> None:
    app = _run()
    assert "Il tuo percorso" in [t.value for t in app.title]
    labels = {m.label for m in app.metric}
    assert {"Lezioni completate", "In corso", "Moduli"} <= labels


def test_studia_page_renders_a_notebook() -> None:
    app = _run("🎓 Studia")
    assert app.tabs, "la vista lezione ha delle schede"
    assert app.code, "il notebook renderizzato contiene celle di codice"


def test_documenti_page_renders_without_generated_docs() -> None:
    app = _run("📄 Documenti")
    assert "Documenti generati" in [t.value for t in app.title]


def test_agent_actions_are_disabled_without_a_key(monkeypatch) -> None:
    """No key must mean a clear message, not a crash on the first click."""

    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.setattr("lesson_agent.settings.api_key", lambda *a, **k: None)

    app = _run("🎓 Studia")
    warnings = " ".join(w.value for w in app.warning)
    assert "GOOGLE_API_KEY" in warnings


@pytest.mark.parametrize("lesson_id", ["python-numpy-refresh", "pca-umap", "capstone-demo"])
def test_every_shape_of_lesson_renders(lesson_id: str) -> None:
    """A theory-only lesson, one with figures, and one from the capstone."""

    app = AppTest.from_file(APP, default_timeout=180)
    app.session_state["selected_lesson"] = lesson_id
    app.run()
    app.radio[0].set_value("🎓 Studia").run()
    assert not app.exception, [str(e.value) for e in app.exception]


def test_saving_the_profile_persists_it(isolated_learner_state) -> None:
    """The sidebar form is the only way a learner sets the level; it must stick."""

    from lesson_agent.profile import Level, load_profile

    app = _run()
    assert load_profile(isolated_learner_state).level is Level.PRINCIPIANTE

    level_box = next(box for box in app.selectbox if box.label == "Livello")
    level_box.set_value(Level.AVANZATO)
    submit = next(button for button in app.button if "Salva profilo" in str(button.label))
    submit.click().run()

    assert not app.exception, [str(e.value) for e in app.exception]
    assert load_profile(isolated_learner_state).level is Level.AVANZATO
