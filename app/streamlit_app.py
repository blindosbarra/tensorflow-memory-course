"""TensorFlow Memory AI Lab — the study interface.

Run it with:

    uv sync --extra dev --extra gui
    uv run streamlit run app/streamlit_app.py

What this replaces: before this app, "studying" meant opening Jupyter and
reading 61 notebooks, while the only agent in the repo was a CLI that
generated one document per notebook, identically for everybody, and had no
way to be asked a question. The GUI puts the three missing pieces in one
place — **who you are** (the sidebar profile, which every agent reads),
**what you don't understand** (the tutor pane next to the notebook), and
**what you get out** (the generated lesson document).

Layout decisions worth keeping:

- **Notebook and tutor sit side by side, each in its own scrolling pane.**
  A tutor you have to navigate away from to consult is a tutor you stop
  consulting. Every code cell has a "chiedi al tutor" button that pre-fills
  the question with that cell, so a doubt costs one click, not a paragraph
  of retyping.
- **Notebooks are read-only here.** Execution belongs to Jupyter, which
  already does it well; "Apri in Jupyter" hands the file over. This app
  never runs learner code, so it can't wedge on a cell that trains a model
  for ten minutes.
- **Nothing personal is committed.** Profile, progress and notes go to a
  git-ignored `.learner/`; the API key to a git-ignored `.env`.
"""

from __future__ import annotations

import base64
from pathlib import Path
import subprocess
import sys

import streamlit as st
import streamlit.components.v1 as components

# The app is launched as a script (`streamlit run app/streamlit_app.py`), so
# the package is only importable if the project was installed into the venv.
# It is (`uv sync` installs it), but a bare `streamlit run` from a different
# interpreter is a plausible mistake with a confusing traceback — this makes
# the failure legible instead.
try:
    from lesson_agent import catalog, notebook_view, profile as profile_mod, settings
    from lesson_agent.async_bridge import run_coro
    from lesson_agent.catalog import LessonProgress, Status
    from lesson_agent.profile import Comfort, Depth, LearnerProfile, Level
    from lesson_agent.read_notebook import read_lesson_context
    from lesson_agent.render_html import OUTPUT_DIR
except ModuleNotFoundError as exc:  # pragma: no cover - startup guard
    st.error(
        f"Non riesco a importare `lesson_agent` ({exc}). Avvia l'app dalla "
        "radice del repository con:\n\n"
        "```bash\nuv sync --extra dev --extra gui\n"
        "uv run streamlit run app/streamlit_app.py\n```"
    )
    st.stop()

PAGE_PERCORSO = "📚 Percorso"
PAGE_STUDIA = "🎓 Studia"
PAGE_DOCUMENTI = "📄 Documenti"


# --------------------------------------------------------------------------
# Cached loaders
# --------------------------------------------------------------------------


@st.cache_data(show_spinner=False)
def load_modules_cached() -> list[catalog.Module]:
    return catalog.load_modules()


@st.cache_data(show_spinner=False)
def load_cells_cached(notebook_path: str, mtime: float) -> tuple[notebook_view.ViewCell, ...]:
    """Parse a notebook for display.

    `mtime` is part of the cache key on purpose: edit and re-run a notebook in
    Jupyter, come back to this tab, and the new outputs show up instead of a
    stale cached parse.
    """

    return notebook_view.read_view_cells(Path(notebook_path))


@st.cache_data(show_spinner=False)
def read_doc_page(doc_path: Path) -> tuple[dict, str]:
    """The lesson's course page, frontmatter split off from the body."""

    from lesson_agent.read_notebook import parse_frontmatter

    return parse_frontmatter(doc_path)


def get_progress() -> dict[str, LessonProgress]:
    if "progress" not in st.session_state:
        st.session_state.progress = catalog.load_progress()
    return st.session_state.progress


def get_profile() -> LearnerProfile:
    if "profile" not in st.session_state:
        st.session_state.profile = profile_mod.load_profile()
    return st.session_state.profile


# --------------------------------------------------------------------------
# Sidebar: who you are, and whether the agents can run
# --------------------------------------------------------------------------


def render_profile_form() -> None:
    current = get_profile()
    st.sidebar.subheader("Il tuo profilo")
    st.sidebar.caption(
        "Ogni agente legge questo profilo prima di scrivere. Cambialo e "
        "rigenera un documento: il testo cambia davvero."
    )

    with st.sidebar.form("profile_form"):
        levels = list(Level)
        level = st.selectbox(
            "Livello",
            levels,
            index=levels.index(current.level),
            format_func=lambda item: item.label,
        )

        comforts = list(Comfort)
        math_comfort = st.select_slider(
            "Dimestichezza con la matematica",
            options=comforts,
            value=current.math_comfort,
            format_func=lambda item: item.label,
        )
        python_comfort = st.select_slider(
            "Dimestichezza con Python",
            options=comforts,
            value=current.python_comfort,
            format_func=lambda item: item.label,
        )

        depths = list(Depth)
        depth = st.selectbox(
            "Quanto vuoi che sia approfondito",
            depths,
            index=depths.index(current.depth),
            format_func=lambda item: item.label,
        )

        background = st.text_area(
            "Il tuo background",
            value=current.background,
            placeholder="Es. sviluppo backend in Python da 5 anni, zero ML.",
            help="Serve agli agenti per scegliere le analogie giuste.",
        )
        goals = st.text_area(
            "Cosa vuoi ottenere",
            value=current.goals,
            placeholder="Es. voglio costruire un sistema di memoria per un chatbot.",
        )
        known_topics_raw = st.text_input(
            "Argomenti che conosci già (separati da virgola)",
            value=", ".join(current.known_topics),
            placeholder="pandas, algebra lineare, backpropagation",
        )

        if st.form_submit_button("Salva profilo", use_container_width=True):
            updated = LearnerProfile(
                level=level,
                math_comfort=math_comfort,
                python_comfort=python_comfort,
                depth=depth,
                background=background,
                goals=goals,
                known_topics=[t.strip() for t in known_topics_raw.split(",") if t.strip()],
            )
            profile_mod.save_profile(updated)
            st.session_state.profile = updated
            # Conversations started under the old profile were seeded with the
            # old briefing and would keep answering at the old level.
            st.session_state.tutor_sessions = {}
            st.success("Profilo salvato. Le conversazioni col tutor ripartono da capo.")


def render_settings_panel() -> settings.AgentReadiness:
    readiness = settings.check_readiness()

    with st.sidebar.expander("⚙️ Impostazioni agenti", expanded=not readiness.ready):
        key = settings.api_key()
        st.write(f"**GOOGLE_API_KEY:** {settings.describe_key(key)}")
        st.write(f"**Modello:** `{settings.model_name()}`")

        if readiness.ready:
            st.success(readiness.reason)
        else:
            st.warning(readiness.reason)

        new_key = st.text_input(
            "Incolla la tua chiave Google AI Studio",
            type="password",
            help="Salvata in `.env` alla radice del repo, che è git-ignored. "
            "Non finisce mai in un commit né nei log.",
        )
        if st.button("Salva chiave", use_container_width=True):
            try:
                settings.write_env_key(new_key)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success("Chiave salvata in `.env`.")
                st.rerun()

        st.caption(
            "Serve una chiave di [Google AI Studio](https://aistudio.google.com/apikey). "
            "Senza chiave puoi comunque leggere i notebook e usare il resto "
            "dell'app: solo tutor e generazione documenti sono disattivati."
        )

    return readiness


# --------------------------------------------------------------------------
# Page: il percorso
# --------------------------------------------------------------------------


def _open_lesson(lesson_id: str) -> None:
    st.session_state.selected_lesson = lesson_id
    st.session_state.page = PAGE_STUDIA


def render_percorso(modules: list[catalog.Module]) -> None:
    progress = get_progress()
    # Unwritten lessons are shown in the syllabus but must not inflate the
    # denominator — you can't complete a lesson nobody has written.
    lessons = [item for item in catalog.all_lessons(modules) if item.is_published]
    done = sum(
        1
        for lesson in lessons
        if progress.get(lesson.lesson_id, LessonProgress()).status is Status.COMPLETATA
    )
    in_corso = sum(
        1
        for lesson in lessons
        if progress.get(lesson.lesson_id, LessonProgress()).status is Status.IN_CORSO
    )

    st.title("Il tuo percorso")
    st.caption(
        "Questo è **il tuo** avanzamento, salvato in `.learner/progress.json` "
        "e non condiviso con nessuno. È un'altra cosa rispetto a "
        "`course/progress.yaml`, che dice a che punto sono gli autori del corso."
    )

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Lezioni completate", f"{done}/{len(lessons)}")
    col_b.metric("In corso", in_corso)
    col_c.metric("Moduli", len(modules))
    st.progress(done / len(lessons) if lessons else 0.0)

    for module in modules:
        published = [item for item in module.lessons if item.is_published]
        module_done = sum(
            1
            for lesson in published
            if progress.get(lesson.lesson_id, LessonProgress()).status is Status.COMPLETATA
        )
        suffix = " · opzionale" if module.optional else ""
        with st.expander(
            f"**{module.title}** — {module_done}/{len(published)}{suffix}",
            expanded=module_done < len(published) and not module.optional,
        ):
            for lesson in module.lessons:
                entry = progress.get(lesson.lesson_id, LessonProgress())
                col_icon, col_title, col_meta, col_button = st.columns([0.5, 6, 2, 1.6])
                col_icon.write(entry.status.icon)
                col_title.write(lesson.display_title)

                meta = []
                if lesson.estimated_minutes:
                    meta.append(f"{lesson.estimated_minutes} min")
                if not lesson.is_published:
                    meta.append("non ancora scritta")
                elif not lesson.has_notebook:
                    meta.append("solo teoria")
                col_meta.caption(" · ".join(meta) if meta else "")

                col_button.button(
                    "Apri",
                    key=f"open-{lesson.lesson_id}",
                    use_container_width=True,
                    disabled=not lesson.is_published,
                    on_click=_open_lesson,
                    args=(lesson.lesson_id,),
                )


# --------------------------------------------------------------------------
# Page: studia una lezione
# --------------------------------------------------------------------------


def open_in_jupyter(notebook_path: Path) -> tuple[bool, str]:
    """Hand the notebook to Jupyter Lab in a detached process.

    Returns `(ok, message)` rather than raising: a missing `jupyter`
    executable is a normal thing to hit (the `gui` extra installs it, a bare
    `lesson-agent` install doesn't) and the GUI should say what to run
    instead of showing a traceback.
    """

    executable = Path(sys.executable).with_name("jupyter")
    if not executable.exists():
        return False, (
            "`jupyter` non è installato in questo ambiente. Esegui "
            "`uv sync --extra dev --extra gui`, oppure apri il file a mano: "
            f"`{notebook_path}`"
        )
    try:
        subprocess.Popen(  # noqa: S603 - fixed executable, path from the catalog
            [str(executable), "lab", str(notebook_path)],
            cwd=str(settings.REPO_ROOT),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError as exc:
        return False, f"Non sono riuscito ad avviare Jupyter: {exc}"
    return True, (
        "Jupyter Lab si sta avviando in una nuova scheda del browser. "
        "Se non si apre, guarda il terminale da cui hai lanciato l'app."
    )


def render_notebook_pane(lesson: catalog.Lesson) -> None:
    if lesson.notebook_path is None:
        if lesson.doc_path is None:
            st.warning(
                "Questa lezione è prevista da `course/course.yaml` ma non è "
                "ancora stata scritta (fase MLOps, vedi `course/progress.yaml`). "
                "Non c'è niente da studiare qui, per ora."
            )
            return
        st.info(
            "Questa lezione è **solo teoria**: non ha un notebook. "
            "Il testo di riferimento è la pagina del corso qui sotto."
        )
        _, body = read_doc_page(lesson.doc_path)
        st.markdown(body)
        return

    cells = load_cells_cached(
        str(lesson.notebook_path), lesson.notebook_path.stat().st_mtime
    )
    code_cells = sum(1 for c in cells if c.cell_type == "code")
    st.caption(
        f"{len(cells)} celle · {code_cells} di codice · sola lettura — "
        "per eseguire, usa **Apri in Jupyter**"
    )

    for cell in cells:
        if cell.cell_type == "markdown":
            st.markdown(cell.source)
            continue

        st.code(cell.source, language="python")
        for output in cell.outputs:
            if output.kind == "image":
                st.image(base64.b64decode(output.image_base64), use_container_width=True)
            elif output.kind == "error":
                st.error("Questa cella ha prodotto un errore:")
                st.code(output.text, language="text")
            else:
                st.text(output.text.rstrip())

        if st.button(
            f"💬 Chiedi al tutor della cella {cell.index}",
            key=f"ask-{lesson.lesson_id}-{cell.index}",
        ):
            st.session_state.pending_question = (
                f"Spiegami la cella {cell.index} di questa lezione:\n\n"
                f"```python\n{notebook_view.cell_excerpt(cell)}\n```\n\n"
                "Cosa fa, riga per riga, e perché serve qui?"
            )
            st.rerun()
        st.divider()


def get_tutor_session(lesson: catalog.Lesson):  # type: ignore[no-untyped-def]
    """One live tutor conversation per lesson, kept across Streamlit reruns."""

    from lesson_agent.tutor import TutorSession

    sessions = st.session_state.setdefault("tutor_sessions", {})
    if lesson.lesson_id not in sessions:
        context = read_lesson_context(lesson.notebook_path)
        sessions[lesson.lesson_id] = run_coro(
            TutorSession.create(context, get_profile()), timeout=120
        )
    return sessions[lesson.lesson_id]


def render_tutor_pane(lesson: catalog.Lesson, readiness: settings.AgentReadiness) -> None:
    st.subheader("Il tutor")
    if not readiness.ready:
        st.warning(readiness.reason)
        return
    if lesson.notebook_path is None:
        st.info("Il tutor lavora sul notebook della lezione; questa non ne ha uno.")
        return

    session = get_tutor_session(lesson)

    for turn in session.turns:
        with st.chat_message("user"):
            st.markdown(turn.question)
        with st.chat_message("assistant"):
            st.markdown(turn.answer)

    pending = st.session_state.pop("pending_question", "")
    question = st.text_area(
        "La tua domanda",
        value=pending,
        key=f"question-{lesson.lesson_id}-{len(session.turns)}",
        placeholder="Es. perché qui si usa la cosine similarity e non la distanza euclidea?",
        height=120,
    )

    col_ask, col_reset = st.columns([3, 1])
    if col_ask.button("Chiedi", type="primary", use_container_width=True, disabled=not question):
        with st.spinner("Il tutor sta pensando…"):
            try:
                run_coro(session.ask(question), timeout=300)
            except Exception as exc:  # noqa: BLE001 - surfaced to the user verbatim
                st.error(f"Il tutor non ha risposto: {exc}")
            else:
                st.rerun()
    if col_reset.button("Azzera", use_container_width=True):
        st.session_state.tutor_sessions.pop(lesson.lesson_id, None)
        st.rerun()


def render_document_tab(lesson: catalog.Lesson, readiness: settings.AgentReadiness) -> None:
    st.subheader("Documento della lezione")
    st.caption(
        "Cinque agenti in pipeline: teoria → (matematica ∥ codice) → redazione "
        "→ revisione tecnica. Leggono il tuo profilo, quindi il documento è "
        "scritto per te, non per uno studente medio."
    )

    if lesson.notebook_path is None:
        st.info("Questa lezione non ha un notebook da cui generare un documento.")
        return

    focus = st.text_area(
        "Un dubbio da mettere al centro del documento (facoltativo)",
        key=f"focus-{lesson.lesson_id}",
        placeholder="Es. non ho capito perché il decadimento è esponenziale e non lineare.",
        help="Se lo compili, il redattore dedica una sezione a questa domanda "
        "e il revisore controlla che ti abbia davvero risposto.",
    )

    existing = OUTPUT_DIR / f"{lesson.lesson_id}.html"
    if not readiness.ready:
        st.warning(readiness.reason)
    elif st.button("Genera documento", type="primary"):
        from lesson_agent.runner import run_lesson_pipeline

        status = st.status("Avvio della pipeline…", expanded=True)
        try:
            context = read_lesson_context(lesson.notebook_path)
            result = run_coro(
                run_lesson_pipeline(
                    context,
                    get_profile(),
                    focus=focus,
                    on_progress=lambda label: status.update(label=label),
                ),
                timeout=900,
            )
        except Exception as exc:  # noqa: BLE001 - surfaced to the user verbatim
            status.update(label="Generazione fallita", state="error")
            st.error(f"{type(exc).__name__}: {exc}")
        else:
            status.update(label=f"Fatto — {result.output_path}", state="complete")
            st.session_state.progress = catalog.record_generated_doc(
                get_progress(), lesson.lesson_id
            )
            errors = [f for f in result.validator.findings if f.severity == "error"]
            if errors:
                st.warning(
                    f"Il revisore ha segnalato {len(errors)} problem"
                    f"{'a' if len(errors) == 1 else 'i'} da leggere nel documento."
                )
            st.rerun()

    if existing.exists():
        st.divider()
        st.caption(f"Ultimo documento generato: `{existing}`")
        components.html(existing.read_text(encoding="utf-8"), height=700, scrolling=True)
        st.download_button(
            "Scarica HTML",
            data=existing.read_text(encoding="utf-8"),
            file_name=existing.name,
            mime="text/html",
        )
    else:
        st.info("Nessun documento generato per questa lezione, per ora.")


def render_course_page_tab(lesson: catalog.Lesson) -> None:
    """The hand-written `docs/modules/<lesson>.md` page, plus its verified sources."""

    if lesson.doc_path is None:
        st.warning("Questa lezione non ha ancora una pagina del corso.")
        return

    _, body = read_doc_page(lesson.doc_path)
    st.markdown(body)

    if lesson.sources:
        st.divider()
        st.subheader("Fonti verificate")
        if not lesson.has_evidence:
            st.caption(
                "Questa lezione non ha un `evidence.yaml`: le fonti sono "
                "citate nella pagina ma non c'è un pacchetto di verifica."
            )
        for source in lesson.sources:
            st.markdown(f"- <{source}>")


def render_notes_tab(lesson: catalog.Lesson) -> None:
    progress = get_progress()
    entry = progress.get(lesson.lesson_id, LessonProgress())
    notes = st.text_area(
        "Le tue note su questa lezione",
        value=entry.notes,
        height=300,
        placeholder="Cosa hai capito, cosa vuoi riguardare, i tuoi esperimenti.",
    )
    if st.button("Salva note"):
        st.session_state.progress = catalog.save_notes(progress, lesson.lesson_id, notes)
        st.success("Note salvate in `.learner/progress.json`.")


def render_studia(modules: list[catalog.Module], readiness: settings.AgentReadiness) -> None:
    lesson_id = st.session_state.get("selected_lesson")
    lesson = catalog.find_lesson(modules, lesson_id) if lesson_id else None

    # Unwritten lessons are listed in the syllabus but can't be studied.
    lessons = [item for item in catalog.all_lessons(modules) if item.is_published]
    chosen = st.selectbox(
        "Lezione",
        lessons,
        index=lessons.index(lesson) if lesson in lessons else 0,
        format_func=lambda item: f"{item.module_title} · {item.display_title}",
    )
    if chosen is not lesson:
        st.session_state.selected_lesson = chosen.lesson_id
        lesson = chosen

    assert lesson is not None
    progress = catalog.touch_lesson(get_progress(), lesson.lesson_id)
    st.session_state.progress = progress
    entry = progress[lesson.lesson_id]

    st.title(lesson.title)
    meta = [f"modulo *{lesson.module_title}*"]
    if lesson.estimated_minutes:
        meta.append(f"~{lesson.estimated_minutes} min")
    if lesson.prerequisites:
        meta.append("prerequisiti: " + ", ".join(lesson.prerequisites))
    st.caption(" · ".join(meta))

    col_status, col_jupyter = st.columns([2, 1.4])
    statuses = list(Status)
    new_status = col_status.selectbox(
        "Il tuo stato",
        statuses,
        index=statuses.index(entry.status),
        format_func=lambda item: f"{item.icon} {item.label}",
        label_visibility="collapsed",
    )
    if new_status is not entry.status:
        st.session_state.progress = catalog.set_status(progress, lesson.lesson_id, new_status)
        st.rerun()

    col_jupyter.button(
        "📓 Apri in Jupyter",
        use_container_width=True,
        disabled=lesson.notebook_path is None,
        key=f"jupyter-{lesson.lesson_id}",
        on_click=lambda: st.session_state.__setitem__(
            "jupyter_result", open_in_jupyter(lesson.notebook_path)
        ),
    )
    if "jupyter_result" in st.session_state:
        ok, message = st.session_state.pop("jupyter_result")
        (st.success if ok else st.warning)(message)

    # The course page is a tab, not a link button: a `file://` URL opened from
    # a page served over http is blocked by every current browser, so the
    # button would look clickable and silently do nothing.
    tab_study, tab_doc, tab_page, tab_notes = st.tabs(
        ["📓 Notebook + tutor", "📄 Documento", "📖 Pagina del corso", "🗒️ Note"]
    )

    with tab_study:
        col_nb, col_tutor = st.columns([3, 2], gap="medium")
        with col_nb, st.container(height=760):
            render_notebook_pane(lesson)
        with col_tutor, st.container(height=760):
            render_tutor_pane(lesson, readiness)

    with tab_doc:
        render_document_tab(lesson, readiness)

    with tab_page:
        render_course_page_tab(lesson)

    with tab_notes:
        render_notes_tab(lesson)


# --------------------------------------------------------------------------
# Page: documenti generati
# --------------------------------------------------------------------------


def render_documenti(modules: list[catalog.Module]) -> None:
    st.title("Documenti generati")
    st.caption(
        f"Le pagine prodotte dagli agenti finiscono in `{OUTPUT_DIR}/`, "
        "una per lezione. Rigenerare una lezione sovrascrive la sua pagina."
    )

    pages = sorted(OUTPUT_DIR.glob("*.html")) if OUTPUT_DIR.exists() else []
    if not pages:
        st.info(
            "Non hai ancora generato nessun documento. Vai su **Studia**, "
            "scegli una lezione e apri la scheda **Documento**."
        )
        return

    titles = {lesson.lesson_id: lesson.title for lesson in catalog.all_lessons(modules)}
    chosen = st.selectbox(
        "Documento",
        pages,
        format_func=lambda p: titles.get(p.stem, p.stem),
    )
    st.caption(f"`{chosen}`")
    html = chosen.read_text(encoding="utf-8")
    components.html(html, height=800, scrolling=True)
    st.download_button("Scarica HTML", data=html, file_name=chosen.name, mime="text/html")


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(
        page_title="TensorFlow Memory AI Lab",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    settings.load_env_file()

    st.sidebar.title("🧠 Memory AI Lab")
    page = st.sidebar.radio(
        "Sezione",
        [PAGE_PERCORSO, PAGE_STUDIA, PAGE_DOCUMENTI],
        key="page",
        label_visibility="collapsed",
    )
    readiness = render_settings_panel()
    render_profile_form()

    modules = load_modules_cached()

    if page == PAGE_PERCORSO:
        render_percorso(modules)
    elif page == PAGE_STUDIA:
        render_studia(modules, readiness)
    else:
        render_documenti(modules)


main()
