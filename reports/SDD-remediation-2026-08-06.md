# SDD — Remediation of the TensorFlow Memory AI Course

Version: 1.1 — 2026-08-07 (converged; see section 10 for what changed)
Status: in implementation — **2 of 13 done and verified** (WI-1, WI-2), **1
cancelled** (WI-5), 10 open. **D1, D2 and D3 all resolved 2026-08-07.**
Source review: `reports/reviews/codebase-status-2026-08-06.md`
Source plan: `reports/fix-plan-2026-08-06.md`
Work queue (durable state): `reports/handover/queue.yaml`
Loop procedure: `reports/handover/AGENT_LOOP.md`

> **Convergence note.** Version 1.0 described work to be done; it did not
> record whether any of it *had* been done, and the machinery it depended on
> lived on a branch that was never merged. One loop iteration ran against
> that gap and produced nothing. Version 1.1 folds the four artifacts —
> review, plan, this SDD, and the handover queue — into one line of truth:
> the SDD specifies, the queue tracks state, `AGENT_LOOP.md` says how to run
> an iteration, and all three now live on the same branch. Every status
> claim below was re-verified against the working tree on 2026-08-07.

---

## 0. How to use this document

This is an implementation specification for coding agents. Each work item
(`WI-n`) is self-contained: it states the problem, the exact files and cell
indices to touch, the required change, acceptance criteria, and the command
that proves it. An agent should be able to pick up a single `WI-n`, complete
it, and stop, without having read the review or the plan.

**Read section 1 through 5 before touching anything.** They contain the
context, conventions, and traps that apply to every work item.

**This document is written in English; everything you author in the
repository must be in Italian.** See section 4.1.

**Every open decision is now resolved** (D1, D2, D3 — 2026-08-07, section 7).
No work item is blocked on a human any more. If a *new* question of the same
kind arises, it is the course author's, not yours: stop and ask.

---

## 1. System context

### 1.1 What this repository is

An executable technical course, in Italian, that teaches data engineering,
TensorFlow/Keras, embeddings, Transformers, Gemma, LoRA and preference
learning, building toward a final project called **Memory AI Lab** (a system
that ingests textual memories and emits structured records with type,
entities, importance, embedding, and graph relations).

The governing specification is `COURSE_FACTORY_SPEC.md`. The agent working
rules are `AGENTS.md`. Both are authoritative and predate this document;
where this SDD contradicts them, this SDD wins **only** for the work items
it defines, and the contradiction is called out explicitly in the item.

### 1.2 The teaching model (important)

Since commit `3fa5799`, **each lesson is a self-contained Jupyter notebook**
in `notebooks/`. A notebook holds theory, runnable examples, a guided
exercise with its explained solution, a quiz, and one incremental step of
the Memory AI Lab project.

The pages in `docs/modules/` are *reference summaries* published to the
MkDocs site — not the lesson itself. `examples/` and `src/memory_ai/` are a
reference implementation, not study material.

This matters because **`templates/lesson.md` still describes the previous
model** (separate `exercises/<id>_starter.py` files and dedicated pytest
suites, both deleted in `3fa5799`). Do not follow that template. See WI-8.

### 1.3 Repository layout

```text
COURSE_FACTORY_SPEC.md    governing spec (definition of done, quality gates)
AGENTS.md                 agent working rules
course/
  course.yaml             declared modules and lessons (84 lesson ids)
  progress.yaml           per-lesson state machine + quality gates (68 entries)
  research_gaps.md        honestly recorded unverified claims
docs/
  index.md, syllabus.md, glossary.md, references.md
  modules/                67 published summary pages (+ modules/en/ for PMLE)
knowledge/<topic>/        research packs (evidence.yaml always; 5 more files rarely)
notebooks/                61 notebooks: lezione-01..60 + one consolidated
src/memory_ai/            library code (only lessons 1-2 today)
tests/                    pytest suite (only covers src/memory_ai)
datasets/
  synthetic/              generated inputs (seeded, committed)
  processed/              notebook outputs (committed, byte-reproducible)
scripts/                  dataset generators + execute_notebooks.py
exercises/, solutions/    STALE leftovers of the pre-3fa5799 model (see WI-8)
reports/                  plans and reviews (this file lives here)
templates/, schemas/, prompts/
mkdocs.yml                site nav — currently 100% consistent, keep it that way
```

### 1.4 Health at the time of writing (measured 2026-08-06)

| Check | Result |
|---|---|
| `ruff check .` | PASS |
| `mypy src` (strict) | PASS, 3 files |
| `pytest` | PASS, 8 tests |
| `mkdocs build --strict` | PASS |
| `scripts/execute_notebooks.py` | **FAIL — 56/61** (5 Gemma notebooks) — **now 61/61 since WI-1, 2026-08-07** |

Do not regress any passing check.

### 1.5 Implementation status (re-verified 2026-08-07)

**2 of 13 done** (WI-1, WI-2 — both P0) and **1 cancelled** (WI-5, by decision
D2). Each row below was checked against the tree, not against a tracker:

| WI | Evidence, checked against the tree |
|---|---|
| WI-1 | **done 2026-08-07** — opt-in guard in all 5 notebooks, `from_preset` wrapped, README documents the opt-in; 61/61 with a clean tree |
| WI-2 | **done 2026-08-07** — the link is now plain text; no `file:///` remains under `docs/` |
| WI-3 | `docs/glossary.md` has 2 entries |
| WI-4 | `docs/references.md` is 14 lines, 6 links; no `scripts/build_references.py` |
| WI-5 | **cancelled 2026-08-07 by D2** — the promise is corrected instead (WI-7) |
| WI-6 | notebooks 31-60 unchanged |
| WI-7 | `README.md:36` and `docs/index.md:20` still promise an exercise in every lesson |
| WI-8 | `exercises/` (15 files), `solutions/`, `templates/lesson.md` all present |
| WI-9 | 21 of 61 notebooks reference a seed, unchanged |
| WI-10 | consolidated notebook unchanged |
| WI-11 | `course.yaml` 84 declared lessons vs `progress.yaml` 68 tracked vs 61 notebooks |
| WI-12 | `mlops` still declared in `course.yaml` with 10 lessons and no notebooks |
| WI-13 | `src/memory_ai/` still holds only `data_cleaning.py`, `data_quality.py` |

The inventory figures in section 1.3 were re-counted at the same time and
are correct as written, with one clarification: `docs/modules/` holds **68**
Italian `.md` files, of which 67 are lesson pages carrying `## Fonti` and one
is `index.md`. The `modules/en/` subtree holds 7 PMLE translations.

---

## 2. Environment setup

```bash
# from the repository root
uv sync --extra dev --extra ml
```

Notes and known constraints:

- Python is pinned to `>=3.11,<3.13`. Local runs observed on 3.11.15.
- `--extra ml` pulls TensorFlow, Keras, KerasHub and NetworkX (~600 MB, a
  few minutes). Notebooks for lessons 10-21, 28 and the Gemma set need it.
- If the global uv cache is blocked, use a local one:
  `UV_CACHE_DIR=.uv-cache uv sync --extra dev --extra ml`.
- **Gemma weights are not downloadable in CI or in a sandbox** — Kaggle
  returns `403` without authentication and an accepted licence. This is the
  root of WI-1; it is expected and must be handled, not worked around.
- Silence TensorFlow noise with `TF_CPP_MIN_LOG_LEVEL=3` when running
  notebooks.

---

## 3. Verification commands

The full gate set, in the order `AGENTS.md` specifies:

```bash
uv run ruff check .
uv run mypy src
uv run pytest
TF_CPP_MIN_LOG_LEVEL=3 uv run python scripts/execute_notebooks.py
uv run mkdocs build --strict
```

`execute_notebooks.py` runs all 61 notebooks with `allow_errors=False`,
each with `cwd=notebooks/`, and returns non-zero listing every failure. It
takes roughly 15 minutes end to end.

### 3.1 Two tiers, and which one gates what

Version 1.0 gave every notebook item a single gate: the full 15-minute run,
needing the ~600 MB `ml` extra. An agent that could not build that
environment could not finish *anything*, and the procedure told it to revert.
That is a gate that converts a working change into no change at all.

Each item in `reports/handover/queue.yaml` now carries up to three fields:

- **`verify_fast`** — cheap, run first, catches most mistakes. For notebook
  work this is `nbformat.validate` plus
  `execute_notebooks.py --only <stems>`, which runs just the notebooks you
  touched.
- **`verify`** — the real definition of done. Unchanged: the full run, and
  `git status --porcelain` empty afterwards.
- **`verify_env`** — what the environment must provide. If it names the `ml`
  extra and you cannot build it, that is an environment limit, not a failed
  change.

The `--only` flag is new in this revision; without arguments the script
still runs all 61 notebooks exactly as before.

**Trap — a partial run legitimately dirties the tree.** Several notebooks
write the same file in `datasets/processed/`, each enriching what the
previous one wrote, and the committed version is the *last* writer's output.
Running `--only lezione-01-dati-mancanti` rewrites
`datasets/processed/memory_events_clean.csv` with lesson 1's seven columns,
dropping the outlier flags lesson 2 adds — verified 2026-08-07. `git status`
is then dirty, and **this is not a determinism failure**. Restore with
`git checkout -- datasets/` after a partial run. The clean-tree invariant
applies only after a *full* run.

**When you cannot run `verify`:** commit the change marked unverified,
leave the item `todo`, and record in its `notes` which command you could
not run and why. Do not revert sound work because of a machine, and do not
mark it done. See `AGENT_LOOP.md`, "When the environment will not cooperate".

**Reproducibility invariant:** after a full notebook run, `git status` must
be clean. The notebooks rewrite `datasets/processed/*.csv` and `*.npy`, and
today they regenerate them byte-identically to what is committed. If your
change makes `git status` dirty after a run, you have broken determinism —
fix it before proceeding.

---

## 4. Global conventions

### 4.1 Content language and style

All learner-facing content — notebooks, `docs/`, `course/`, commit
messages — is **Italian**. English technical terms stay in English when
standard (`embedding`, `loss`, `learning rate`, `retrieval`).

From `AGENTS.md`: short sentences; intuition before mathematics; no implicit
prerequisites; every lesson connects theory, code and the Memory AI project;
citations at the end of the relevant section; no long verbatim quotations.

Note the existing content writes accented characters inconsistently
(`perche'` and `perché` both occur). **Match the surrounding file**; do not
launch a normalization pass.

### 4.2 Hard prohibitions

- **No absolute paths.** (`AGENTS.md`; spec Gate C.) One violation exists
  today and WI-4 removes it.
- **No secrets or credentials** in any committed file.
- **No invented facts.** If a source is missing, add an entry to
  `course/research_gaps.md` rather than filling the gap with a guess. Do not
  invent APIs, metrics, results, DOIs, or compatibility claims. A prior
  review caught a fabricated DOI marked `verified`; that must not recur.
- **No unrelated changes.** One work item per commit.

### 4.3 Editing notebooks — mechanics

This is where automated edits most often go wrong. Notebooks are
`nbformat` 4.5 JSON.

- Every cell requires a **unique** `id` (short hex string, e.g. `2aa3e032`).
  When inserting cells, generate new ids that do not collide within the
  file.
- `source` is a **list of strings, each ending in `\n`** (except possibly
  the last). Use `str.splitlines(keepends=True)`.
- Code cells carry `cell_type`, `id`, `metadata`, `source`,
  `execution_count`, `outputs`. Markdown cells carry only `cell_type`, `id`,
  `metadata`, `source` — **never** add `outputs` or `execution_count` to a
  markdown cell.
- For cells you newly insert, set `"execution_count": null` and
  `"outputs": []`. Do not fabricate outputs.
- **Do not reformat or re-serialize the whole notebook.** Load with `json`,
  mutate the specific cells, dump with `indent=1` and a trailing newline to
  match the existing files. Verify the diff touches only intended cells.
- Notebook metadata is `{"kernelspec": {...python3...}, "language_info":
  {...}}`. Leave it alone.
- Output storage is inconsistent across the repo (43 notebooks carry
  outputs, 18 do not). **Preserve whatever the file already does**; do not
  add or strip outputs as a side effect.

- **Never write LaTeX through a layer that interprets escapes.** A markdown
  cell containing `\right)` or `\alpha` is one careless heredoc, shell echo
  or double-decoded string away from holding a literal carriage return
  followed by `ight)`, or a BEL followed by `lpha`. That happened on
  2026-08-09 in lesson 40 and no gate caught it: markdown cells are not
  executed, so the 61/61 run stays green; the JSON is well-formed, so
  `nbformat.validate` passes; and `mkdocs` builds `docs/modules/`, not the
  notebooks. Build the string in Python and let `json.dumps` do the
  escaping. `tests/test_notebook_text_integrity.py` now fails on any stray
  control character in a notebook's source, naming the cell, the line and
  the escape it probably came from.

After editing, validate:

```bash
uv run python -c "
import nbformat,sys
nb=nbformat.read(sys.argv[1],as_version=4); nbformat.validate(nb); print('valid')
" notebooks/<file>.ipynb
uv run pytest tests/test_notebook_text_integrity.py
```

### 4.4 Git

- Branch: work on the branch you were assigned; never push to `master`.
- One work item per commit; reference the item id in the message body.
- Commit messages in Italian, imperative, explaining *why* not just *what*.
- Do not commit `.venv/`, `.uv-cache/`, `.notebook-runtime/`, `site/`,
  `models/` — all already in `.gitignore`.

---

## 5. Work item index

Status column verified against the tree on 2026-08-07. The machine-readable
copy is `reports/handover/queue.yaml`; if the two ever disagree, the queue
is authoritative for *state* and this document for *specification*.

| ID | Title | Priority | Blocked by | Status |
|---|---|---|---|---|
| WI-1 | Fix the Gemma availability guard (5 notebooks) | P0 | — | **done** |
| WI-2 | Remove the absolute path from the site homepage | P0 | — | **done** |
| WI-3 | Rebuild `docs/glossary.md` | P1 | — | todo |
| WI-4 | Regenerate `docs/references.md` from lesson sources | P1 | — | todo |
| WI-5 | ~~Add exercise + solution to lessons 31-60~~ | P1 | — | **cancelled (D2)** |
| WI-6 | Raise theory density in lessons 31-60 | P2 | — | todo |
| WI-7 | Align README and `docs/index.md` with reality | P1 | — | todo |
| WI-8 | Retire stale `exercises/`, `solutions/`, `templates/lesson.md` | P2 | — | todo |
| WI-9 | Seed the 21 non-deterministic notebooks | P2 | — | todo |
| WI-10 | Make the consolidated notebook portable (Windows/macOS) | P2 | — | todo |
| WI-11 | Reconcile `course.yaml` and `progress.yaml` with reality | P2 | — | todo |
| WI-12 | Resolve the `mlops` module and the Vertex AI requirement | P3 | — | todo |
| WI-13 | Extract capstone components into `src/memory_ai/` + tests | P3 | — | todo |

Priorities reflect learner impact, per the course author's direction that CI
state is not itself a goal.

---

## WI-1 — Fix the Gemma availability guard

**Priority:** P0 **Blocked by:** — **Est.:** small

### Problem

Five notebooks crash with a `403` traceback partway through the lesson for
any learner who lacks Kaggle credentials and an accepted Gemma licence.

The guard cell intends to detect Gemma availability and skip the model cells
cleanly. It checks the wrong thing — whether `keras_hub` **imports**:

```python
GEMMA_AVAILABLE = False
_motivo = ""
try:
    import keras       # noqa: F401
    import keras_hub   # noqa: F401
    GEMMA_AVAILABLE = True
except Exception as exc:  # noqa: BLE001
    _motivo = f"{type(exc).__name__}: {exc}"
```

`keras_hub` is installed by `--extra ml` (observed: 0.29.1), so the import
succeeds, `GEMMA_AVAILABLE` becomes `True`, and the next cell executes

```python
gemma = keras_hub.models.GemmaCausalLM.from_preset("gemma_2b_en")
```

which attempts an authenticated Kaggle download and raises:

```
KaggleApiHTTPError: 403 Client Error.
You don't have permission to access resource at URL:
https://kaggle.com/models/keras/gemma/keras/gemma_2b_en/3.
```

Package presence and weight reachability are different conditions. The guard
must test the second.

### Files and exact locations

In every file the guard is **cell index 2** and the real `from_preset` call
is **cell index 3**.

| Notebook | Cells | Guard | Call | Guard variant |
|---|---|---|---|---|
| `notebooks/lezione-34-keras-hub.ipynb` | 7 | 2 | 3 | long (918 chars) |
| `notebooks/lezione-35-inferenza-gemma.ipynb` | 7 | 2 | 3 | long (identical) |
| `notebooks/lezione-36-output-strutturato.ipynb` | 8 | 2 | 3 | long (identical) |
| `notebooks/lezione-41-gemma-lora.ipynb` | 7 | 2 | 3 | medium (631 chars) |
| `notebooks/lezione-56-capstone-gemma-lora.ipynb` | 6 | 2 | 3 | short (357 chars) |

In `lezione-34`, `from_preset` also appears as prose in cells 0, 1 and 6 —
those are markdown, leave them.

**Correction (verified 2026-08-07).** The table above is accurate — guard at
cell 2, `from_preset` at cell 3, guard sizes 918/918/918/631/357 characters —
but it is not the complete list of cells that read `GEMMA_AVAILABLE`. Two
notebooks branch on it a second time, further down:

| Notebook | Extra cell reading `GEMMA_AVAILABLE` |
|---|---|
| `notebooks/lezione-35-inferenza-gemma.ipynb` | cell 5 |
| `notebooks/lezione-56-capstone-gemma-lora.ipynb` | cell 4 |

Give those the same treatment as cell 3: they must degrade to the same
`[saltato]` branch. An agent that edits only cells 2 and 3, as v1.0 said,
leaves two cells that can still fail.

**How this was solved (implemented 2026-08-07).** Rather than editing four
cells across two notebooks, cell 3's `except` branch sets
`GEMMA_AVAILABLE = False` after printing its reason. The guard cell states
what the environment *offers*; the load cell corrects it to what the
environment actually *delivered*. Every later cell then reads a truthful
flag and falls back on its own, unmodified — which is why the diff stays at
cells 2 and 3 in all five notebooks.

The structure that makes this work is `if not GEMMA_AVAILABLE:` in place of
`else:`, so the fallback body runs both when Gemma was never available and
when loading it failed, without duplicating the lesson text:

```python
if GEMMA_AVAILABLE:
    try:
        ...  # existing body unchanged
    except Exception as exc:  # noqa: BLE001
        print(f"[saltato] modello non caricabile: {type(exc).__name__}")
        GEMMA_AVAILABLE = False
if not GEMMA_AVAILABLE:
    ...  # existing else branch, unchanged
```

Verified on `lezione-35` and `lezione-56` with `GEMMA_ENABLED=1` and
deliberately invalid Kaggle credentials: the load fails, cell 3 prints
`[saltato] modello non caricabile: ProxyError`, and the downstream cells
produce their rule-based results (`['Marco', 'Glasgow']`) with no
`NameError` for the undefined `gemma`.

### Required change

**(a)** Replace the body of cell 2 in each of the five notebooks with the
canonical guard below. Keep each notebook's existing explanatory comment
tone; the logic must be identical across all five.

```python
# Guardia di ambiente: KerasHub + pesi Gemma sono un extra opzionale (`ml`)
# e richiedono un download autenticato di diversi GB da Kaggle, con licenza
# accettata. Non basta che il pacchetto sia installato: servono anche le
# credenziali. In assenza, le celle del modello vengono SALTATE in modo
# pulito e il resto della lezione gira comunque.
import os

GEMMA_AVAILABLE = False
_motivo = ""
if os.environ.get("GEMMA_ENABLED", "").lower() not in ("1", "true", "yes"):
    _motivo = "GEMMA_ENABLED non impostata"
elif not (os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY")):
    _motivo = "credenziali Kaggle assenti (KAGGLE_USERNAME/KAGGLE_KEY)"
else:
    try:
        import keras  # noqa: F401
        import keras_hub  # noqa: F401
        GEMMA_AVAILABLE = True
    except Exception as exc:  # noqa: BLE001
        _motivo = f"{type(exc).__name__}: {exc}"

if GEMMA_AVAILABLE:
    print("KerasHub disponibile: le celle del modello verranno eseguite.")
else:
    print("KerasHub/Gemma NON disponibile in questo ambiente.")
    print("Motivo:", _motivo)
    print("Le celle che richiedono il modello stampano [saltato]; "
          "il resto della lezione gira comunque.")
```

The explicit `GEMMA_ENABLED` opt-in is deliberate: a learner who happens to
have Kaggle credentials in the environment must not have a multi-gigabyte
download start without asking for it.

**(b)** In cell 3 of each notebook, wrap the `from_preset` call so an
unforeseen failure (licence not accepted, network down, preset renamed)
degrades to the same `[saltato]` branch instead of raising. Preserve the
existing `else:` messages verbatim — they explain to the learner what the
model *would* have produced, and they are part of the lesson.

Sketch (adapt to each notebook's actual body):

```python
if GEMMA_AVAILABLE:
    try:
        import keras_hub
        gemma = keras_hub.models.GemmaCausalLM.from_preset("gemma_2b_en")
        ...  # existing body unchanged
    except Exception as exc:  # noqa: BLE001
        print(f"[saltato] modello non caricabile: {type(exc).__name__}")
        ...  # same fallback text as the else branch
else:
    ...  # existing else branch, unchanged
```

**(c)** Add a short section to `README.md` explaining how to actually enable
Gemma (`GEMMA_ENABLED=1`, `KAGGLE_USERNAME`/`KAGGLE_KEY`, accepted licence)
and stating that without it the lessons still run and remain studiable.

### Prior validation

This fix was prototyped against `lezione-35-inferenza-gemma.ipynb` before
this document was written. Result: the notebook executed with no errors and
took the fallback branch, printing

```
KerasHub/Gemma NON disponibile in questo ambiente.
Motivo: GEMMA_ENABLED non impostata
[saltato] gemma.generate(prompt, max_length=32)
entita' estratte (fallback a regole): ['Marco', 'Glasgow']
```

The rest of the lesson ran normally. The approach is known to work; the
remaining work is applying it to five files and adding the try/except.

### Acceptance criteria

1. All five notebooks execute cleanly with no Gemma credentials present.
2. `GEMMA_AVAILABLE` is `False` in that environment, and each model cell
   prints its `[saltato]` explanation.
3. No notebook imports `keras_hub` at module level outside the guard.
4. `README.md` documents the opt-in.
5. Nothing else in the five notebooks changed (verify the diff).

### Verification

```bash
TF_CPP_MIN_LOG_LEVEL=3 uv run python scripts/execute_notebooks.py   # expect 61/61
git status --porcelain                                              # expect empty
```

### Out of scope

Testing the `GEMMA_AVAILABLE == True` path (requires real credentials).
Changing which preset the lessons use.

---

## WI-2 — Remove the absolute path from the site homepage

**Priority:** P0 **Blocked by:** — **Est.:** trivial

### Problem

`docs/index.md` line 15 links the spec through a local filesystem URL:

```markdown
... in conformità alla specifica [`COURSE_FACTORY_SPEC.md`](file:///usr/local/google/home/sommacampagna/projects/tensorflow-memory-course/COURSE_FACTORY_SPEC.md).
```

It is broken for every reader of the published site, and it exposes the
author's local path and username. It violates `AGENTS.md` ("Non utilizzare
path assoluti") and spec Gate C ("nessun path locale assoluto").
`mkdocs --strict` does not catch it because it parses as an external URL.

This is the only absolute path in the repository.

### Required change

`COURSE_FACTORY_SPEC.md` lives at the repository root and is **not** part of
`docs/`, so it is not published. Either link to it on the repository host,
or drop the link and keep the reference as plain text. Prefer the latter
unless a canonical public URL is confirmed — do not invent one.

### Acceptance criteria

- `grep -rn "file:///" docs/` returns nothing.
- No local username or filesystem path anywhere under `docs/`.
- `uv run mkdocs build --strict` passes.

---

## WI-3 — Rebuild `docs/glossary.md`

**Priority:** P1 **Blocked by:** — **Est.:** medium

### Problem

The glossary has **two entries** — "Imputazione" and "Missing value" — for a
60-lesson course covering embeddings, attention, Transformers, LoRA, QLoRA,
DPO, RLHF, hybrid retrieval and drift. Spec Gate E requires an updated
glossary.

### Required change

Populate the glossary by **extracting terms already defined in the
lessons**. This is extraction, not new writing: every definition must trace
to a lesson that already teaches the term. Do not introduce concepts the
course does not cover.

Suggested coverage, one short definition each, alphabetical, matching the
existing two-level heading format (`## Term`):

data cleaning and evaluation (imputazione, outlier, duplicato,
near-duplicate, data leakage, train/validation/test, overfitting, dropout,
calibrazione); tensors and training (tensore, gradiente, loss function,
optimizer, learning rate, backpropagation, `GradientTape`); text and
retrieval (tokenizzazione, vocabolario, embedding, sentence embedding,
cosine similarity, PCA, UMAP, clustering, Recall@K, MRR, retrieval ibrido);
memory representation (memoria episodica/semantica/preferenza, recency
decay, importance scoring, grafo delle memorie, contraddizione);
Transformers and adaptation (self-attention, blocco Transformer, sampler,
transfer learning, freezing, LoRA, rank, QLoRA, quantizzazione, adapter);
preference learning (feedback schema, coppia chosen/rejected, reward
function, DPO, RLHF, RLAIF, online learning); operations (drift,
monitoring, pipeline).

Cross-reference the lesson that introduces each term where it helps.

### Acceptance criteria

- Every glossary term appears in at least one lesson notebook or module
  page.
- No term is defined in a way that contradicts its lesson.
- `uv run mkdocs build --strict` passes.

---

## WI-4 — Regenerate `docs/references.md`

**Priority:** P1 **Blocked by:** — **Est.:** small

### Problem

`docs/references.md` holds six links, all belonging to lessons 1-2 (pandas,
scikit-learn, one TensorFlow tutorial). The course has 67 module pages and
**every one of them already has a `## Fonti` section**. The aggregate page
is simply stale.

### Required change

Rebuild the page from the per-lesson `Fonti` sections so it cannot drift
again. Preferred: a small script (for example
`scripts/build_references.py`) that reads `docs/modules/**/*.md`, collects
the `## Fonti` entries, de-duplicates, groups by module, and writes
`docs/references.md`. Document how to re-run it.

If a source appears in a lesson but its URL cannot be verified, do not
promote it silently — carry over whatever marker the lesson already uses and
record anything unresolved in `course/research_gaps.md`.

### Acceptance criteria

- `docs/references.md` covers all modules, not just lessons 1-2.
- Regenerating twice produces identical output (deterministic ordering).
- No invented or unverified URLs added.
- `uv run mkdocs build --strict` passes.

---

## WI-5 — Add exercise and solution to lessons 31-60

**Priority:** P1 **Blocked by:** **D2** **Est.:** large

### Problem

Lessons 1-30 each contain a guided exercise and an explained solution.
**None of lessons 31-60 does** — 30 notebooks, half the course. Both
`README.md` and `docs/index.md` promise the exercise for *every* lesson.

This is also a regression against the binding review
`reports/reviews/course-content-review.md`, whose blocker B1 was "the
student never writes code". It was fixed for lessons 1-2, extended through
lesson 30, and never applied from Phase 5 onward.

### The established pattern (follow it exactly)

Four consecutive cells, taken from `lezione-28-retrieval-ibrido.ipynb`
(cells 3-6):

1. **markdown** — `## Parte N — Esercizio guidato`, then the task in the
   second person, naming concrete inputs and referencing earlier lessons
   where relevant.
2. **code** — starter: a comment saying exactly what to compute, then
   `pass`. Nothing else.
3. **markdown** — `### Soluzione spiegata`: the reasoning and the expected
   result, in prose, before any code.
4. **code** — the working solution ending in an `assert` that encodes the
   property being taught.

Verbatim example of cells 2 and 4 of that block:

```python
# Scrivi qui: calcola i due punteggi e stampali.

pass
```

```python
a = punteggio_ibrido(similarita=0.5, segnale_grafo=0.0, importanza_candidato=1.0)
b = punteggio_ibrido(similarita=0.5, segnale_grafo=1.0, importanza_candidato=0.0)
print(f'candidato A (solo importanza alta): {a:.3f}')
print(f'candidato B (solo segnale grafo)  : {b:.3f}')
assert b > a
```

The `assert` is what makes the exercise verifiable when the notebook runs —
it is not optional.

### Insertion point per notebook

Every target notebook ends with a single markdown cell containing both
`## Riepilogo (max 8 punti)` and `## Quiz`. **Insert the four-cell block
immediately before that final cell.**

| Notebook | Cells | Insert before index |
|---|---|---|
| `lezione-31-self-attention.ipynb` | 11 | 10 |
| `lezione-32-blocco-transformer.ipynb` | 11 | 10 |
| `lezione-33-tokenizer-generazione.ipynb` | 11 | 10 |
| `lezione-34-keras-hub.ipynb` | 7 | 6 |
| `lezione-35-inferenza-gemma.ipynb` | 7 | 6 |
| `lezione-36-output-strutturato.ipynb` | 8 | 7 |
| `lezione-37-valutazione-generativa.ipynb` | 7 | 6 |
| `lezione-38-transfer-learning.ipynb` | 8 | 7 |
| `lezione-39-lora-math.ipynb` | 9 | 8 |
| `lezione-40-lora-from-scratch.ipynb` | 9 | 8 |
| `lezione-41-gemma-lora.ipynb` | 7 | 6 |
| `lezione-42-qlora.ipynb` | 8 | 7 |
| `lezione-43-baseline-comparison.ipynb` | 8 | 7 |
| `lezione-44-adapter-packaging.ipynb` | 8 | 7 |
| `lezione-45-feedback-schema.ipynb` | 7 | 6 |
| `lezione-46-chosen-rejected.ipynb` | 9 | 8 |
| `lezione-47-reward-functions.ipynb` | 10 | 9 |
| `lezione-48-dpo-intuition.ipynb` | 7 | 6 |
| `lezione-49-preference-tuning.ipynb` | 9 | 8 |
| `lezione-50-rlhf-rlaif.ipynb` | 7 | 6 |
| `lezione-51-online-learning-risks.ipynb` | 9 | 8 |
| `lezione-52-capstone-architettura.ipynb` | 6 | 5 |
| `lezione-53-capstone-dataset.ipynb` | 7 | 6 |
| `lezione-54-capstone-classificatore.ipynb` | 7 | 6 |
| `lezione-55-capstone-embedding-grafo.ipynb` | 8 | 7 |
| `lezione-56-capstone-gemma-lora.ipynb` | 6 | 5 |
| `lezione-57-capstone-valutazione.ipynb` | 8 | 7 |
| `lezione-58-capstone-pipeline.ipynb` | 8 | 7 |
| `lezione-59-capstone-monitoring.ipynb` | 8 | 7 |
| `lezione-60-capstone-demo.ipynb` | 7 | 6 |

Indices assume no prior insertion; re-derive them if WI-1 or another item
has already changed a file. Locate the final `## Riepilogo` cell
programmatically rather than trusting the number.

Number the exercise part consistently with the notebook's existing
`## Parte N` headings; several Phase 6-8 notebooks do not use `Parte N`
headings at all, in which case use `## Esercizio guidato` without a number.

### Design constraints for the exercises

- The exercise must be solvable with what the **notebook itself** has
  already defined and run. No new dependency, no new dataset.
- It must not duplicate the guided example — the binding review rejected
  exactly that ("la soluzione e' identica all'esempio guidato").
- It must be doable in a couple of minutes; lessons target 15-30 minutes
  total.
- **It must not require Gemma weights.** Phases 6-8 are fully exercisable
  without them: lesson 40 trains a LoRA adapter in pure NumPy, lesson 47
  builds a reward function, lesson 57 evaluates offline.
- For `lezione-34`, `35`, `36`, `41`, `56` the model is genuinely required.
  Per decision **D2**, either write the exercise against the rule-based
  fallback path those notebooks already contain, or mark the lesson
  demonstrative and state so in the notebook. Pick one and apply it to all
  five consistently.

### Acceptance criteria

1. Each in-scope notebook has the four-cell block, correctly ordered.
2. Every solution cell ends in an `assert` that passes when the notebook is
   executed top to bottom.
3. The exercise is not a restatement of the guided example.
4. No notebook requires Gemma weights to complete its exercise.
5. `nbformat.validate` passes on every edited file; cell ids are unique.

### Verification

```bash
TF_CPP_MIN_LOG_LEVEL=3 uv run python scripts/execute_notebooks.py   # 61/61
git status --porcelain                                              # empty
```

### Suggested batching

One commit per phase, not one per notebook: Phase 5 (31-37), Phase 6
(38-44), Phase 7 (45-51), Phase 8 (52-60).

---

## WI-6 — Raise theory density in lessons 31-60

**Priority:** P2 **Blocked by:** **D2** **Est.:** large

### Problem

Measured across the notebooks:

| Range | Median markdown words | Median code cells |
|---|---|---|
| Lessons 1-30 | 1085 | 6 |
| Lessons 31-60 | 355 | 3 |

The back half is roughly **one third** the depth of the front half. At
lesson 31 the course silently changes character. WI-5 adds the missing
exercises but does not close this gap.

### Required change

Bring the `## Teoria essenziale` sections of Phases 5-8 up to the standard
set by Phases 0-4. Use lessons 1-30 as the calibration reference, and
`templates/lesson.md`'s *content* guidance (not its exercise workflow, which
is obsolete — see WI-8): intuition before mathematics, assumptions and
trade-offs stated, the *why* before the *how*, a primary citation near every
significant technical claim.

Do not pad. The target is explanatory completeness, not word count.

Note that lessons 2 and 30-60 have no `## Fonti` section inside the
notebook, though all 67 published module pages do. Adding sources to the
notebooks as citations are introduced is in scope here.

### Acceptance criteria

- No lesson 31-60 remains below roughly half the median depth of lessons
  1-30.
- Every new technical claim has a primary source, recorded in the lesson and
  in `knowledge/<topic>/evidence.yaml`.
- Unverifiable claims go to `course/research_gaps.md` instead of being
  asserted.

---

## WI-7 — Align README and `docs/index.md` with reality

**Priority:** P1 **Blocked by:** WI-5 **Est.:** trivial

### Problem

Two published statements are currently false for lessons 31-60:

- `README.md`: "Ogni lezione e' **un notebook autosufficiente** in
  `notebooks/`: teoria, esempi eseguibili, esercizio guidato con soluzione
  spiegata, quiz con risposte, e un passo del **progetto del corso**".
- `docs/index.md`: "ogni lezione è accompagnata dal proprio notebook Jupyter
  autosufficiente con teoria, esempi di codice eseguibili, esercizio guidato
  e passo incrementale del Memory AI Lab".

### Required change

After WI-5 lands, verify each claim against the notebooks and correct
whatever is still not true. If decision **D2** leaves some lessons without
an exercise, say so plainly rather than leaving a blanket promise.

Also check the claim that every lesson carries "un passo del progetto": it
does not hold for lesson 13 or for lessons 52-60 — though for 52-60 the
reason is that they *are* the capstone, which the text should make clear.

### Acceptance criteria

Every claim in `README.md` and `docs/index.md` about lesson structure is
verifiable against the notebooks.

---

## WI-8 — Retire the stale exercise scaffolding

**Priority:** P2 **Blocked by:** — **Est.:** small

### Problem

Commit `3fa5799` moved the course to self-contained notebooks and deleted
`exercises/*_starter.py` and `tests/exercises/`. Three leftovers still
describe the old model:

1. `exercises/*.md` and `solutions/*.md` — 15 files each, lessons 1-15 only,
   superseded by the notebooks.
2. Two published pages (`docs/modules/data-cleaning-01-missing-values.md`,
   `docs/modules/duplicates-types-outliers.md`) tell the reader "Le risposte
   commentate sono in `solutions/<id>.md`" — a directory outside `docs/`,
   therefore unreachable from the site.
3. `templates/lesson.md` still instructs authors to write
   `exercises/<lesson-id>_starter.py` with TODOs and dedicated failing
   tests. **Any agent that follows this template will rebuild the deleted
   model.** This is the most damaging of the three.

### Required change

- Decide per directory: delete `exercises/` and `solutions/`, or move their
  content into `docs/` so the links resolve. Deleting is preferred — the
  notebooks already carry exercise and solution.
- Remove or repoint the two `solutions/...md` references.
- Rewrite `templates/lesson.md` to describe the **current** model: a
  self-contained notebook, the four-cell exercise block from WI-5, quiz with
  answers, one Memory AI Lab step, and a module page in `docs/modules/` as
  the reference summary.

### Acceptance criteria

- No published page references a path that is not reachable from the site.
- `templates/lesson.md` describes only artifacts that exist.
- `uv run mkdocs build --strict` passes.

---

## WI-9 — Seed the non-deterministic notebooks

**Priority:** P2 **Blocked by:** — **Est.:** medium

### Problem

21 notebooks use randomness, data splitting, or Keras training without
fixing a seed. Spec Gate C requires "seed controllato dove possibile". The
most consequential is `lezione-54-capstone-classificatore.ipynb`, which
trains and saves `models/memory_type_classifier.keras`, an artifact reused
by later lessons — so an unseeded run changes downstream results.

Affected: lessons 1, 6, 7, 30, 34, 35, 36, 38, 39, 41, 42, 43, 44, 46, 47,
48, 49, 50, 51, 54, 56.

### Required change

Set seeds where randomness affects a result the learner is asked to read.
For Keras use `keras.utils.set_random_seed(...)`; for NumPy prefer an
explicit `np.random.default_rng(SEED)` (the pattern already used in
`scripts/generate_*.py`) over the legacy global functions.

Where a lesson *teaches* non-determinism, keep the randomness and make the
point explicit instead of seeding it away — `lezione-20-clustering.ipynb`
already does this well for K-Means label assignment. Do not flatten a
deliberate teaching moment.

### Acceptance criteria

- Two consecutive full notebook runs produce an identical `git status`
  (clean) and identical committed artifacts.
- Any intentionally unseeded cell carries a comment explaining why.

---

## WI-10 — Make the consolidated notebook portable

**Priority:** P2 **Blocked by:** — **Est.:** trivial

### Problem

`notebooks/consolidato-memoria-lezioni-01-15.ipynb` does an unguarded
`import resource` to report peak RAM. The `resource` module does not exist
on Windows, so the notebook fails outright — and `README.md` explicitly
supports Windows with PowerShell instructions. On macOS the reported number
is also wrong: `ru_maxrss` is bytes there, not kilobytes, and the cell's own
comment says "KB -> MB su Linux".

### Required change

Guard the import and degrade gracefully, or replace it with a portable
measurement. If keeping `resource`, handle the platform-dependent unit
correctly rather than documenting the bug in a comment.

### Acceptance criteria

- The notebook runs on Linux, macOS and Windows.
- Reported memory is either correct on all three or clearly labelled as
  unavailable.

---

## WI-11 — Reconcile the trackers with reality

**Priority:** P2 **Blocked by:** D1, D2, D3 **Est.:** medium

### Problem

`course/course.yaml` and `course/progress.yaml` no longer describe the
repository.

1. **17 of 84 declared lessons do not exist** — no page, no notebook, and no
   entry in `progress.yaml`, so they are invisible as gaps too:
   - `mlops` (all 10): `reproducible-project`, `containers-artifacts`,
     `local-training-pipeline`, `vertex-ai-training`, `vertex-ai-pipelines`,
     `registry-deployment`, `batch-online-inference`, `model-evaluation`,
     `monitoring-drift`, `cost-cleanup-security`;
   - `data-engineering`: `tfdata-performance`, `data-validation`;
   - `keras-dnn`: `forward-pass`, `losses-optimizers`, `backprop-autodiff`,
     `sequential-functional-api`, `callbacks-checkpoints`.
2. **`status` no longer discriminates.** `foundations`, `data-engineering`
   and `keras-dnn` are `planned` while fully written and published; `mlops`
   is `planned` and genuinely empty. Same label, opposite situations.
3. **`progress.yaml` overstates gates.** All 68 entries carry a
   `quality_gates` block. `code: pass` on the five Gemma lessons is false
   until WI-1; `didactics: pass` on the 30 lessons without an exercise
   depends on D2; `research: pass` on the 58 topics whose research pack
   holds only `evidence.yaml` depends on D3.
4. `course_status` reads
   `milestones_0_to_5_authored_ready_for_learner_review` and
   `current_milestone: milestone-5`, while the syllabus and site describe 8
   phases plus a capstone.
5. No human learner review has been filed, though the 2026-07-12
   verification named it a non-delegable blocking gate. `reports/reviews/`
   contains no `*-learner-review.md`.

### Required change

Bring both files into correspondence with what exists. Every lesson id
declared in `course.yaml` must either have artifacts on disk or be visibly
`planned` in `progress.yaml`. Gate values must reflect measured state.

**Optional, recommended:** add `scripts/check_course_consistency.py` that
reports lessons declared but not tracked, tracked but missing their declared
artifacts, pages not declared, and lessons at `learner_review`/`done` with a
non-`pass` gate. The course author has said CI is not a priority, so this is
a tool to run by hand before a work session — not a gate. Its value is
avoiding a repeat of the manual audit that produced this document.

### Acceptance criteria

- Declared, tracked and present lesson counts reconcile, or every difference
  is explicitly `planned`.
- No `quality_gates` value asserts a state contradicted by a measurable
  check.

---

## WI-12 — Resolve the `mlops` module and the Vertex AI requirement

**Priority:** P3 **Blocked by:** **D1** **Est.:** large or trivial per D1

### Problem

`COURSE_FACTORY_SPEC.md` §2 makes "esiste almeno una pipeline Vertex AI
documentata e testabile" part of the definition of done. The repository
contains **no** Vertex AI or `google-cloud-aiplatform` code at all. Vertex AI
appears only as exam theory in the optional PMLE module, which does not
satisfy Step 5 of the operational process.

### Required change

Per decision **D1**. If option B (recommended): write 2-3 locally executable
MLOps lessons (project and artifact packaging, reproducible local training
pipeline, with the evaluation and monitoring already in capstone lessons 57
and 59 formalized as a step), remove or mark `planned` the 7 cloud lessons,
and **amend spec §2** so the requirement is reachable without a billable GCP
project.

Amending the spec is legitimate. Leaving it stating a requirement nobody
intends to meet is not.

Also decide the 7 missing `data-engineering`/`keras-dnn` lessons. Several of
those topics are already taught inside lessons 10-14, so removing them as
standalone ids is likely more honest than writing new lessons.

### Acceptance criteria

- No lesson id is declared without a decision recorded.
- Spec §2 states only requirements the repository intends to satisfy.

---

## WI-13 — Extract capstone components into `src/memory_ai/`

**Priority:** P3 **Blocked by:** — **Est.:** large

### Problem

`pytest` covers only `src/memory_ai/`, which contains just the lessons 1-2
data-cleaning utilities (`data_cleaning.py`, `data_quality.py`, 208 lines).
Spec §2 requires that "il progetto finale funziona localmente", but the
Memory AI Lab exists only as code copied from notebook cell to notebook
cell, with no tests.

### Required change

Extract the capstone components into `src/memory_ai/` with tests:
type classifier, importance scorer, embedding, similarity search, entity and
relation graph, hybrid retrieval, the `MemoryRecord` schema and the pipeline
that orchestrates them (lesson 52 already defines the dataclass and a stub
pipeline; lesson 58 assembles `MemoryAILab`).

Have the capstone notebooks import from the package instead of redefining.
Keep the teaching intent: lessons that build a component *from scratch* must
keep building it — extract the finished component, do not replace the
pedagogy with an import.

Existing code sets the quality bar: full type annotations (mypy strict
passes), docstrings explaining the didactic decision, explicit column
validation, auditable reports returned as frozen dataclasses.

### Acceptance criteria

- The Memory AI Lab pipeline runs end to end from `src/memory_ai/` alone.
- `uv run mypy src` passes under strict.
- Each extracted component has tests.
- Capstone notebooks still teach construction where that is the point.

---

## 6. Postmortem — why the first attempt implemented nothing

A coding loop was pointed at this document on 2026-08-07. It created the
branch `agent/complete-sdd-remediation`, pushed it at exactly the merge
commit of PR #1, and added **zero commits**. Not a partial item, not a
failed attempt: no work at all. The cause is worth recording, because it was
a defect in this specification's delivery, not in the agent's reasoning.

### 6.1 The proximate cause: a missing file that looked like a finished job

The loop's first instruction was:

```text
1. Run: uv run python scripts/next_work_item.py
   - exit 2 → stop the loop and report why (all done, or a decision is needed)
```

That script — together with `reports/handover/queue.yaml` and
`AGENT_LOOP.md` — was committed to `claude/codebase-review-status-0ufpuv` at
06:47:48 UTC. PR #1 had merged at 06:36:52 UTC and carried only the three
report documents. The machinery missed the merge by eleven minutes and was
never merged afterwards.

The agent branched from `master`, where the script does not exist. A Python
interpreter asked to run a file that is not there exits with code **2**:

```console
$ uv run python scripts/next_work_item.py; echo $?
python3: can't open file 'scripts/next_work_item.py': [Errno 2] No such file
2
```

Exit 2 was defined as "all done, or a decision is needed". The agent did
what it was told: it stopped and reported that there was nothing to do. The
one failure mode the loop was designed to prevent — spinning without a stop
condition — was traded for a worse one: stopping instantly with a false
success signal.

The lesson generalises past this repository. **An exit code that means
"nothing to do" must never be reachable by an environment fault.** A control
signal has to be something only the working system can produce; absence of
output must be distinguishable from a report of completion. Hence the
sentinel lines and the step-0 preflight now in `AGENT_LOOP.md`.

### 6.2 Contributing causes that would have stopped it anyway

Even with the machinery present, three things stood between the agent and a
commit:

1. **The verification gate could not be paid.** WI-1 is first in priority
   order, and its only gate was the full 61-notebook run, requiring the
   ~600 MB `ml` extra and about fifteen minutes. The procedure then said: if
   verification fails, revert. An agent in a sandbox without that
   environment would have written the correct fix and thrown it away.
   Section 3.1 and the `verify_fast`/`verify_env` fields exist because of
   this.

2. **The branch pointer disagreed with the assignment.** `queue.yaml` named
   `claude/codebase-review-status-0ufpuv` as *the* branch while the agent
   had been assigned `agent/complete-sdd-remediation`, and step 6 said only
   "push to the assigned branch". The queue field is now
   `machinery_landed_on` and is explicitly not a push target.

3. **The reading cost was front-loaded and undifferentiated.** This document
   is ~1100 lines of English, and the procedure required sections 1-5 before
   *any* edit. That is the right call before touching notebooks; it is a
   poor trade before WI-2, which deletes one URL from one line. The tiering
   in section 3.1 is a partial answer; a fuller one would let trivial items
   declare a shorter reading set.

### 6.3 The instruction was not achievable as phrased

The loop was asked to "complete the SDD remediation". It cannot be
completed by any agent: **5 of 13 items are blocked on decisions D1, D2 and
D3, which are the course author's and which an agent is explicitly forbidden
to resolve** (section 7). The reachable ceiling for autonomous work is
8 items — WI-1, 2, 3, 4, 8, 9, 10, 13 — after which the correct behaviour
is to stop and ask.

An instruction whose success condition is unreachable will report failure or
manufacture progress. Neither is useful. Ask for the eight, or resolve the
three decisions first.

### 6.4 The same shape again — `in_progress` was a one-way door (2026-08-09)

An iteration on 2026-08-09 ran the preflight and stopped on
`SENTINEL: NOTHING-ACTIONABLE`, reporting that everything left waited on a
human decision. Nothing did: D1-D4 were resolved, and the stop message
printed no question because there was none to print.

What was actually left was WI-6 and WI-13, both `in_progress`, both carrying
a written remainder in `notes` — lessons 34-60 for one, the classifier, the
graph, the retrieval and the pipeline for the other. `AGENT_LOOP.md` section 4
tells an iteration that cannot finish a large item to do exactly that: split
it, record the remainder, leave the status `in_progress`, stop, and let the
next iteration pick up from the note. `actionable()` in
`scripts/next_work_item.py` selected `todo` and `blocked` only. The status
the procedure asked for was the one status that removed the item from
circulation.

Two iterations had followed the instruction correctly, and the queue was left
with no reachable work and eight days of real work still in it. Nothing was
lost, because the notes were good; but nothing would ever have been picked up
either, and the loop would have gone on paying the cost of a full preflight
to report a false completion.

This is the third occurrence of the failure mode in 6.1 — an environment or a
state the control signal cannot express, collapsing into "nothing to do":

| | The state | What the signal could say |
|---|---|---|
| 2026-08-07 | script absent | exit 2 = "all done" |
| 2026-08-08 | sandbox with no `origin` | "cannot confirm freshness" = stop |
| 2026-08-09 | item split, work remaining | not `todo` = not offerable |

The fix has three parts. The picker offers `in_progress` items, first among
their priority, so a split item is finished before another is opened. It
prints `RESUME` rather than `NEXT` and labels the notes as the handover, so
continuing is distinguishable from restarting. And when it does stop, it
prints per item what that item waits on — a decision by name, a dependency by
id and status, a *cancelled* dependency called out as dead, or "nothing at
all", which reports itself as a bug in the picker rather than a question the
author has to answer. `tests/test_next_work_item.py` pins all of it.

The rule, stated once for whoever writes the next piece of loop machinery:
**any state the procedure instructs an agent to produce, the tooling must be
able to consume.** A procedure and its tooling that disagree do not raise an
error; the tooling wins, quietly, and its silence is indistinguishable from
success.

---

## 7. Decisions — RESOLVED 2026-08-07

**All three were decided by the course author on 2026-08-07.** Nothing in
this section blocks work any more. The rationale is recorded in
`course/research_gaps.md`, section "Decisioni dell'autore del corso"; the
machine-readable copy is `meta.decisions` in `reports/handover/queue.yaml`.

| Decision | Outcome | Effect on the work items |
|---|---|---|
| **D1** mlops module | **Shrink to a short local path.** 2-3 runnable lessons on packaging, artifacts and a local pipeline; cloud theory stays with the PMLE module. | WI-12 unblocked, and it is now the *reduction* job, not a build job. Seven declared lesson ids leave `course.yaml`; `COURSE_FACTORY_SPEC.md` §2 must be amended. |
| **D2** exercises 31-60 | **Correct the promise.** Two declared lesson types: with exercise (1-30), read-only (31-60). No new exercises. | **WI-5 is cancelled, not deferred.** WI-7 becomes the deliverable and is unblocked. WI-6 (theory depth) survives — see below. |
| **D3** research packs | **Amend the spec.** `evidence.yaml` mandatory, the other five files recommended. | WI-11 unblocked; the spec §5 amendment is part of it. |

**D2 does not cancel WI-6.** The two were bundled only because both rewrite
the same 30 notebooks. Exercises and depth are different promises: lessons
31-60 sit at a median of 355 markdown words against 1085 for lessons 1-30,
and a read-only lesson at one third the depth of its neighbours is still a
weak lesson. WI-6 is now `todo` on its own merits.

The original analysis that produced these decisions is kept below, because
it records *why* each option was weighed — useful if a future change of
circumstance reopens one of them.

### Original analysis (pre-decision)

They blocked the work items named. They were the course author's to make.

### D1 — The `mlops` module (blocks WI-12, part of WI-11)

| Option | Cost | Effect |
|---|---|---|
| A. Build it fully | Very high — 10 lessons plus a real Vertex AI pipeline, GCP project, credentials, cost | Satisfies spec §2 literally |
| B. Reduce to a local path | Medium — 2-3 lessons on packaging, artifacts, local pipeline; cloud theory delegated to PMLE | Course stays runnable without a cloud account |
| C. Remove from `course.yaml` | Low | Spec §2 must be amended |

**Recommendation: B.** The course is built to run without external
dependencies — the Gemma guard exists for that reason. A *testable* Vertex
AI pipeline contradicts that: it needs a billable GCP project no learner is
guaranteed to have.

### D2 — Exercises for lessons 31-60 (blocks WI-5, WI-6)

| Option | Cost | Effect |
|---|---|---|
| A. Add to all 30 | High | README and site claims become true |
| B. Correct the claims | Very low | Two documented lesson types: with exercise (1-30), read-only (31-60) |
| C. Hybrid | Medium | Exercises where the learner can genuinely write code; claims corrected elsewhere |

**Recommendation: C, leaning toward A.** Phases 6-8 are fully exercisable
without Gemma. Only lessons 34, 35, 36, 41 and 56 genuinely depend on the
model.

### D3 — Incomplete research packs (blocks part of WI-11)

58 of 67 `knowledge/<topic>/` directories contain only `evidence.yaml`;
spec §5 requires five more files.

| Option | Cost | Effect |
|---|---|---|
| A. Complete all | Very high — 5 files × 58 topics | Full §5 conformance |
| B. Amend the spec | Low | `evidence.yaml` mandatory, the rest recommended |

**Recommendation: B.** All 58 have the evidence, which is what serves the
"no invention" rule. The other five files did not block writing lessons 3-60.

---

## 8. Sequencing

```text
WI-1  ──┐
WI-2  ──┤  no decisions needed, start immediately
WI-3  ──┤
WI-4  ──┘
        │
        ├─ WI-8, WI-9, WI-10  (independent, any time)
        │
   D2 ──┴─→ WI-5 ──→ WI-7
            WI-6
   D1 ─────→ WI-12
   D1,D2,D3 → WI-11
   (none)  → WI-13
```

Parallel-safe groups: `{WI-1}`, `{WI-2, WI-3, WI-4}`, `{WI-8, WI-9, WI-10}`
touch disjoint files. WI-5 and WI-6 touch the same 30 notebooks — assign
them to the same agent, or run WI-5 to completion first.

WI-1 and WI-5 both edit the five Gemma notebooks. Land WI-1 first.

---

## 9. Definition of done for this SDD

The remediation is complete when:

1. All 61 notebooks execute top to bottom with no credentials of any kind.
2. Every claim in `README.md` and `docs/index.md` about lesson structure is
   true.
3. No absolute path, credential, or unreachable link exists in `docs/`.
4. `course.yaml` and `progress.yaml` describe what the repository contains.
5. `COURSE_FACTORY_SPEC.md` states only requirements intended to be met.
6. `ruff`, `mypy src`, `pytest` and `mkdocs build --strict` all pass, and a
   full notebook run leaves `git status` clean.
7. Every decision D1-D3 is recorded with its rationale in
   `course/research_gaps.md` or a `reports/reviews/` entry.

None of the seven hold today. Condition 7 in particular has no artifact at
all: D1, D2 and D3 are recorded only in this document and in the queue, and
`course/research_gaps.md` does not mention them.

**The autonomous ceiling.** Conditions 1, 3 and 6 are reachable by an agent
without any decision (WI-1, WI-2, WI-9, WI-10 and the checks). Conditions 2,
4, 5 and 7 are not: they depend on D1, D2 and D3. Do not ask a loop to
satisfy this section — ask it for the eight unblocked items, then decide.

---

## 10. Change log

### 1.2 — 2026-08-09 (the loop could not resume its own work)

- **Section 6.4 records the third instance of the 6.1 failure mode**: the
  picker never offered an item left `in_progress`, which is precisely the
  state the procedure asks for when an item is split across iterations. The
  loop reported "nothing actionable" with two started items and no open
  decision.
- **`scripts/next_work_item.py` offers `in_progress` items**, first among
  their priority, prints `RESUME` for them, and — when it does stop — names
  per item what it waits on instead of blaming a decision by default.
- **`tests/test_next_work_item.py`** covers the selection rules, the stop
  messages, and that the shipped queue is not in that deadlock.

### 1.1 — 2026-08-07 (convergence)

Written after the first implementation attempt produced zero commits. This
revision changes no work item's intent; it makes the document usable by the
agent that has to execute it.

- **Status is now recorded.** Section 1.5 gives per-item evidence, verified
  against the tree rather than a tracker; section 5 gains a status column.
  v1.0 could not distinguish "not started" from "done".
- **The machinery is on the same branch as the specification.** `queue.yaml`,
  `AGENT_LOOP.md` and `scripts/next_work_item.py` were stranded on an
  unmerged branch, which is what broke the first run. They are now here.
- **Section 6 records the postmortem**, including the exit-code collision
  that ended the loop with a false "nothing to do".
- **Verification is tiered** (section 3.1): `verify_fast` for the iteration,
  `verify` for done, `verify_env` for what the machine must provide. A new
  `--only` flag on `scripts/execute_notebooks.py` makes the fast tier real.
  An agent that cannot build the ml extra now commits with a note instead of
  reverting.
- **WI-1's scope was corrected**: `GEMMA_AVAILABLE` is also read by cell 5
  of `lezione-35` and cell 4 of `lezione-56`, which v1.0 did not list.
- **Inventory clarified**: `docs/modules/` holds 68 Italian pages (67 lesson
  pages with `## Fonti`, plus `index.md`) and 7 English PMLE pages. All other
  counts in section 1.3 were re-verified and were correct.
- **Section 9 states the autonomous ceiling**: 8 of 13 items, because 5 wait
  on decisions no agent may take.

### 1.0 — 2026-08-06

Initial specification: 13 work items derived from
`reports/reviews/codebase-status-2026-08-06.md` and
`reports/fix-plan-2026-08-06.md`.
