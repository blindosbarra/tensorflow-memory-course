# SDD — Interactive lesson-companion agent (Google ADK, multi-agent)

Status as of 2026-08-12 (end of session 2): **all six pipeline steps
implemented and unit-tested; the five-agent `Workflow` builds and validates
correctly; nothing has been run against a real Gemini call yet — no
`GOOGLE_API_KEY` was available in this sandbox this session.** Section 7 is
the handover for whoever resumes with that key available: it has the exact
one-line command to run and what to check. This document is written for a
fresh session with no memory of this conversation.

This is a **new feature track, independent of the remediation queue**
(`reports/handover/queue.yaml`, `reports/SDD-remediation-2026-08-06.md`,
`reports/handover/AGENT_LOOP.md`, WI-1..WI-15). Do **not** add this work to
`queue.yaml`: that file is polled by `scripts/next_work_item.py` for the
autonomous remediation loop, which expects notebook/doc fixes against the
existing WI list — an ADK multi-agent subsystem would confuse it. Track this
feature's own progress in this document instead, and update it at the end
of every session (like `queue.yaml`'s `notes`, but for this track).

---

## 1. What was asked

The course (`notebooks/`, 61 lessons) is theory-heavy. The user wants an
agent that accompanies each lesson: it prepares the standard lesson
documentation (theory, math, explanations), and the user then interacts
with it — asking it to add information or go deeper on specific points.
The agent must produce a set of HTML pages and charts explaining the
lesson tied to each notebook.

## 2. Decisions made this session (do not re-litigate)

Asked and answered via `AskUserQuestion`, in order:

1. **Agent framework:** not a Claude Code skill/subagent — the user
   explicitly asked for **Google ADK (Agent Development Kit) 2.x**, with a
   **multi-agent architecture**, naming five roles:
   1. an agent that **writes the output document**,
   2. an agent that **gathers information** and builds the content,
   3. an agent that **technically validates** the content,
   4. an agent focused on the **math**,
   5. an agent focused on the **Python code**, to help the user understand it.
2. **Output destination:** HTML + charts, **committed to the repo** (not
   published as ephemeral Artifacts).
3. **Initial scope:** build the tool first and validate it on 1-2 lessons
   on demand — do **not** batch-generate all 61 lessons yet.
4. **LLM backend:** **Google AI Studio** (`GOOGLE_API_KEY` env var), not
   Vertex AI. No GCP project exists in this repo for this purpose today.
   The key is provided by the user **outside the chat** (e.g. `!export
   GOOGLE_API_KEY=...` in this session, or a git-ignored `.env`) — never
   paste a key into the conversation, and never commit one.
5. **Model:** the user asked for "the most recent Gemini Flash" for **all
   five** agents (not the flash/pro split I offered). Verified against
   `ai.google.dev/gemini-api/docs/models` on 2026-08-11: the current
   stable, recommended general-purpose Flash model is **`gemini-3.6-flash`**.
   Put this string in exactly one place (a constants module) so bumping it
   later is a one-line change — model names move fast and this will be
   stale again within months.

## 3. Environment state

- `google-adk` **2.6.3** was installed for exploration with
  `uv pip install google-adk --python .venv` — this was **not** added to
  `pyproject.toml`, so it will vanish on a fresh `uv sync`. Tomorrow's
  first step is to add it properly (see §6).
- Network egress confirmed reachable from this sandbox: `pypi.org` (200)
  and `generativelanguage.googleapis.com` (404 on `/`, i.e. TLS+DNS work —
  a real request needs the API key) both responded.
- **2026-08-12 update:** `google-adk>=2.6` is now a proper
  `lesson-agent` optional-dependency group in `pyproject.toml` (installed
  version resolved: 2.6.3, matching the exploration build). Installed via
  `uv sync --extra dev --extra ml --extra lesson-agent` (all three extras
  together, so the `ml`/`dev` tooling used elsewhere in the repo — pytest,
  tensorflow, etc. — doesn't get dropped from `.venv`; a bare `uv sync
  --extra lesson-agent` uninstalls everything not in that one group).
- No `GOOGLE_API_KEY` is set in this environment yet.
- Confirmed by grepping the repo: there is **no existing** Vertex AI/ADK/
  Gemini-API integration anywhere in `src/`, `scripts/`, or config. The
  hits for "Vertex AI" etc. are all course *content* (the PMLE module
  teaches Vertex AI conceptually) — nothing to reconcile with, this is
  greenfield.

## 4. ADK API, verified against the installed source (not doc pages)

Early research via `WebFetch` on `ai.google.dev`/`adk.dev`/GitHub-raw pages
gave **inconsistent** answers about the current API (small fetch-model
summaries contradicted each other, e.g. on whether `Event.is_final_response()`
exists). Do not trust those summaries. Instead `google-adk` was installed
into `.venv` and its source read directly
(`.venv/lib/python3.12/site-packages/google/adk/`). These facts are
confirmed against **2.6.3** source, line references below:

- Top-level exports (`google/adk/__init__.py`): `Agent`, `Context`,
  `Event`, `Runner`, `Workflow`. **`InMemoryRunner` is not re-exported at
  top level** — import it from `google.adk.runners`:
  `from google.adk.runners import InMemoryRunner`.
- `Agent` (`google/adk/agents/llm_agent.py`, aliased at top level):
  `Agent(name=..., model=..., instruction=..., tools=[python_functions],
  sub_agents=[...], output_schema=SomePydanticModel)`. Plain Python
  functions can be tools directly (ADK wraps them; docstring becomes the
  tool description, e.g. `contributing/samples/workflows/sequence` in the
  upstream repo).
- `Workflow` (`google/adk/workflow/_workflow.py:145`) — **`class
  Workflow(BaseNode)`**, not a `BaseAgent`. This matters for how you hand
  it to the runner (next point). Built with:
  `Workflow(name=..., edges=[("START", node1, node2, ...)])` — a
  deterministic sequential graph. A node in the tuple can be a plain
  Python function or an `Agent`; output of one node becomes the input of
  the next automatically.
  - **Fan-out/fan-in:** an edge element can itself be a tuple of nodes,
    e.g. `("START", (math_node, code_node), join_node, next_node)` runs
    `math_node` and `code_node` in parallel; `JoinNode(name=...)` (from
    `google.adk.workflow`) collects their results into a `dict` keyed by
    each node's name, which the next function receives as its single
    argument.
  - `google.adk.workflow` also exports `FunctionNode`, `Node`/`node`
    (decorator), `RetryConfig`, `NodeTimeoutError`, `DEFAULT_ROUTE`,
    `Edge` — not yet explored in depth, only `Workflow`/`JoinNode` were
    needed for the plan in §5.
- `InMemoryRunner.__init__` (`google/adk/runners.py:2295`) takes
  `agent: Optional[BaseAgent]` **and separately** `node: Any = None`.
  Since `Workflow` is a `BaseNode`, not a `BaseAgent`, **pass it as
  `InMemoryRunner(node=my_workflow)`**, not `agent=`.
- **Sessions are not auto-created.** `Runner.__init__` has
  `auto_create_session: bool = False` (`runners.py:214`), and
  `InMemoryRunner.__init__` does **not** forward or expose this flag — it
  is hard-set to the base default. `run_async` calls
  `_get_or_create_session` (`runners.py:913`), which raises
  `SessionNotFoundError` if the session doesn't exist and
  `auto_create_session` is `False`. **You must create the session
  yourself first:**
  ```python
  await runner.session_service.create_session(
      app_name=runner.app_name, user_id=user_id, session_id=session_id,
  )
  ```
- Running and reading the result (`runners.py:1023` `run_async`, or the
  sync wrapper `run` at `runners.py:955` for a quick script):
  ```python
  from google.genai import types

  async for event in runner.run_async(
      user_id=user_id,
      session_id=session_id,
      new_message=types.UserContent(parts=[types.Part(text=prompt)]),
  ):
      if event.is_final_response() and event.content and event.content.parts:
          text = "".join(p.text for p in event.content.parts if p.text)
  ```
  `Event.is_final_response()` **does** exist
  (`google/adk/events/event.py:276`) — an earlier WebFetch summary that
  claimed otherwise was wrong; verified by reading the method body.
  `Event.node_name` (`event.py:263`) identifies which node in a `Workflow`
  produced a given event — useful for picking out one specific node's
  output (e.g. the final `render_html` node) when multiple nodes ran.

## 5. Proposed pipeline (design only — not implemented)

One run = one notebook (`notebooks/lezione-NN-*.ipynb`) in, one
self-contained HTML file out. Six nodes, wired as a `Workflow`:

1. **`read_notebook`** (plain function, no LLM) — parses the target
   notebook's markdown + code cells, pulls the matching
   `docs/modules/*.md` summary page and the matching
   `knowledge/<topic>/evidence.yaml` research pack, and produces one
   structured context blob. Fully unit-testable without any API key.
2. **`gather_info_agent`** (LLM) — role 2 from §2. Reads the context blob,
   produces an information brief: theory points, key facts, which sources
   back which claim.
3. **fan-out** to **`math_agent`** and **`code_agent`** (LLM, parallel) —
   roles 4 and 5. `math_agent` explains the formulas present in the lesson
   (LaTeX); `code_agent` walks the notebook's Python cells concept by
   concept for the reader.
4. **`JoinNode`** → **`writer_agent`** (LLM) — role 1. Drafts the
   structured lesson document (theory + math + code explanation sections)
   from the three upstream outputs.
5. **`validator_agent`** (LLM) — role 3. Technically reviews the draft
   against the notebook's actual code/printed output and the
   `evidence.yaml` sources; flags inaccuracies.
   **v1 decision: report-only** — it appends a validation section to the
   document rather than looping the writer for automatic revision. Keeps
   the first version simple, deterministic, and inspectable. An
   LLM-judge/retry loop is a plausible v2, not now.
6. **`render_html`** (plain function, no LLM) — assembles the writer's
   sections + the validator's report into one self-contained HTML file,
   with charts (matplotlib, following the `dataviz` skill's guidance —
   load it before writing any chart code) built from data actually present
   in the notebook where possible (real printed metrics) rather than
   decorative filler. **Confirmed 2026-08-12:** writes to
   `docs/lezioni-interattive/<lesson_id>.html`, using the lesson's slug
   (e.g. `capstone-pipeline.html`), not `lezione-NN.html` — this matches
   how `docs/modules/*.md` is named and survives notebook renumbering
   (§4 confirmed notebook numbers and doc slugs have already drifted apart
   once in this course's history). Commits it like any other repo file.

Decided 2026-08-12 (session 2), resolving the three open questions above:

- **Structured output: yes, Pydantic `output_schema` for every LLM agent**
  (`gather_info_agent`, `math_agent`, `code_agent`, `writer_agent`,
  `validator_agent`). Plain text would force `render_html`/downstream
  agents to re-parse free text; a schema per agent is more upfront work
  but keeps the pipeline mechanical and testable. Schemas live in
  `src/lesson_agent/schemas.py`.
- **Repo layout: `src/lesson_agent/` confirmed**, added to
  `pyproject.toml`'s `[tool.hatch.build.targets.wheel] packages` list
  alongside `src/memory_ai` (was `["src/memory_ai"]`, now
  `["src/memory_ai", "src/lesson_agent"]`). CLI entry point:
  `scripts/generate_lesson_doc.py <lezione-id>`, mirroring how other
  one-off scripts in `scripts/` already sit outside the package and import
  from `src/`.
- **Test strategy: LLM-touching tests are skipped by default, not
  excluded from `testpaths`.** The repo's `pytest` gate (`testpaths =
  ["tests"]`) keeps running unconditionally — no new pytest config, no
  separate marker registration. Instead:
  - `tests/test_lesson_agent_read_notebook.py` and
    `tests/test_lesson_agent_render_html.py` are plain unit tests (no
    network, no API key) and always run.
  - Any test that drives an `Agent`/`Workflow` through a real Gemini call
    is decorated
    `@pytest.mark.skipif(not os.environ.get("GOOGLE_API_KEY"),
    reason="requires GOOGLE_API_KEY (real Gemini call)")` — so `uv run
    pytest` stays deterministic and free in CI/sandboxes without the key,
    while a dev with the key locally still exercises them. No dedicated
    `tests/lesson_agent/` subdirectory: the existing `tests/` layout is
    flat (one file per module), so new files follow that convention with
    a `test_lesson_agent_` prefix rather than introducing the repo's first
    test subpackage.

## 6. Resume checklist for tomorrow (2026-08-11 version — see §7 for what
actually happened)

1. ~~Add `google-adk` as a new optional-dependency group in
   `pyproject.toml`~~ **Done 2026-08-12.**
2. ~~Set `GOOGLE_API_KEY` in the shell~~ **Still not done** — no key was
   available in this sandbox in session 2 either. This is now the one
   blocking item; see §7.
3. ~~Decide the two open layout questions in §5~~ **Done 2026-08-12**, see
   the "Decided 2026-08-12" block in §5.
4. ~~Implement `read_notebook` and `render_html` first~~ **Done
   2026-08-12** — `src/lesson_agent/read_notebook.py`,
   `src/lesson_agent/render_html.py`, both unit-tested without an API key.
5. ~~Write the three simplest agent instructions ... confirm one real
   end-to-end LLM call works before adding `writer_agent`/`validator_agent`
   on top~~ **Partially done, deviated from plan:** all five agents were
   written together in `src/lesson_agent/agents.py` (see its module
   docstring for the session-state data-flow model this required
   reverse-engineering from source — not something the 2026-08-11 API
   notes in §4 covered). The graph builds and validates
   (`tests/test_lesson_agent_agents.py::test_build_workflow_graph_shape`,
   passes with no API key). **The "confirm one real call works" step
   itself could not run** — no key. This is the single highest-risk
   unknown left: the session-state templating mechanism (`{lesson_context}`
   etc. in `instruction`, `output_key` writes) is reverse-engineered from
   reading `_llm_agent_wrapper.py`/`llm_agent.py` source, not verified
   against a live call. It may not work as reasoned. See §7.
6. **Not done** — needs a live run first (see item 2/5 above).
7. **Not done** — depends on 6.

## 7. Session 2 (2026-08-12) — what was built, and the exact next step

**Branch note:** this session ran on `claude/wi-15-capstone-citations`
(confirmed with the user via `AskUserQuestion` — that branch was already
fully merged into `master`, and the branch name suggested in an earlier
handover note, `claude/remediation-queue-item-bz0inh`, belongs to the
unrelated remediation track (this document's intro says this feature is
independent of that queue). If you resume in a different
sandbox/session, check you're on the same branch or ask which one to use —
don't assume.

### Files added

- `src/lesson_agent/__init__.py` (empty)
- `src/lesson_agent/constants.py` — `MODEL = "gemini-3.6-flash"`, single
  source of truth (§2.5).
- `src/lesson_agent/read_notebook.py` — `read_lesson_context` +
  `format_context_for_agent`. Pure, no LLM. Finds the doc page via
  `deliverables:` in frontmatter (not filename parsing — see its
  docstring for why). **Fixed two pre-existing YAML bugs while building
  this**: `docs/modules/capstone-pipeline.md` and
  `docs/modules/capstone-demo.md` had unquoted `title: X: Y` frontmatter,
  invalid YAML (unquoted `: ` in a block scalar reads as a nested
  mapping). Quoted both titles; no content change.
- `src/lesson_agent/render_html.py` — `render_html` / `write_lesson_html`.
  Pure, no LLM. `extract_numeric_series` looks for a printed JSON list of
  same-shaped records to chart; returns `None` (no chart section) when a
  notebook only prints one record — which is lezione-58's actual shape,
  confirmed by hand-eyeballing the rendered PNG in this session (a
  synthetic 3-item series; real chart choice/colors follow the `dataviz`
  skill's reference palette, light mode only).
- `src/lesson_agent/schemas.py` — the five agents' `output_schema`
  Pydantic models (`InfoBrief`, `MathExplanation`, `CodeWalkthrough`,
  `WriterOutput`, `ValidatorOutput`).
- `src/lesson_agent/agents.py` — the five `Agent`s + `build_workflow()`.
  **Read its module docstring before touching this file** — it documents
  the session-state data-flow model (`{placeholder}` in `instruction`,
  `output_key`, seeded `create_session(state=...)`) reverse-engineered
  from `google-adk==2.6.3` source this session, since no bundled example
  covers it and the 2026-08-11 API notes (§4) didn't either.
- `scripts/generate_lesson_doc.py` — the CLI entry point. Exits with code
  2 and a clear message if `GOOGLE_API_KEY` is unset (verified: does not
  crash, does not prompt).
- `tests/test_lesson_agent_read_notebook.py`,
  `tests/test_lesson_agent_render_html.py`,
  `tests/test_lesson_agent_agents.py` — 16 tests total, all pass without
  an API key; one (`test_generate_lesson_doc_lezione_58`) is `skipif`'d on
  a missing `GOOGLE_API_KEY` and was never actually run this session.
- `pyproject.toml` — `lesson-agent` optional-dependency group, both
  packages in `[tool.hatch.build.targets.wheel]`.

Full repo `uv run pytest` (`--extra dev --extra ml --extra lesson-agent`):
**156 passed, 1 skipped**, at the end of this session.

### What is genuinely unverified

Everything in `agents.py` is built from reading ADK source, not from
running it. Three things could plausibly be wrong on the first live
attempt:

1. Whether `{lesson_context}` / `{info_brief}` / etc. placeholders in
   `instruction` actually get resolved from session state the way the
   `llm_agent.py` docstring says (this session did not find a working
   executable example to confirm against, only the docstring's claim and
   the general ADK templating convention).
2. Whether `output_schema` + Gemini Flash reliably returns JSON that
   `validate_schema` can parse on the first try (no retry/repair logic is
   wired in yet — a `RetryConfig` exists on nodes per §4 but is unused
   here).
3. Whether `session.state["writer"]` / `["validator"]` are actually
   present and shaped as `WriterOutput`/`ValidatorOutput` expect once the
   real run finishes — `model_validate` will raise clearly if not, which
   is the intended fail-fast behavior, but it hasn't fired in anger yet.

### Exact next step (needs `GOOGLE_API_KEY`)

```
export GOOGLE_API_KEY=...   # user-provided, outside any committed file
uv run python scripts/generate_lesson_doc.py capstone-pipeline
```

Watch stderr for `[<node_name>] evento ricevuto` lines — confirms which
nodes actually ran and in what order. On success it prints `Scritto:
docs/lezioni-interattive/capstone-pipeline.html`; open that file and read
it. If it fails, the traceback will point at one of the three unverified
points above — start there, not by re-deriving the ADK API from scratch
(§4 and `agents.py`'s docstring already did that work).

Once one lesson's page reads well to a human, decide whether/how to batch
the other 60 (§5, "Initial scope" decision — still not revisited).

## 8. Change log

- **2026-08-11** — Initial write-up. Requirements gathered via
  `AskUserQuestion` (§2), ADK API verified against installed source (§4),
  pipeline designed (§5). No code written.
- **2026-08-12** — Session 2. Implemented all six pipeline steps (§7):
  `read_notebook`, `render_html`, `schemas`, `agents`/`Workflow`, the CLI
  script, and tests for all of it (156 passed, 1 skipped in the full repo
  suite). Resolved both open design questions from §5. Fixed two
  pre-existing YAML frontmatter bugs found while building `read_notebook`.
  Reverse-engineered the ADK session-state data-flow model from source
  (`agents.py` docstring). **Blocked on `GOOGLE_API_KEY`**: not available
  in this sandbox, so nothing in `agents.py`/`generate_lesson_doc.py` has
  run against a real Gemini call — see §7 for the exact next command and
  the three specific things most likely to break on first contact.
