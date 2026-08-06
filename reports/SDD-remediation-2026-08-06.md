# SDD — Remediation of the TensorFlow Memory AI Course

Version: 1.0 — 2026-08-06
Status: ready for implementation
Source review: `reports/reviews/codebase-status-2026-08-06.md`
Source plan: `reports/fix-plan-2026-08-06.md`

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

**Do not start a work item whose `Blocked by` field names an unresolved
decision.** Open decisions are in section 7.

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

### 1.4 Current health (measured 2026-08-06)

| Check | Result |
|---|---|
| `ruff check .` | PASS |
| `mypy src` (strict) | PASS, 3 files |
| `pytest` | PASS, 8 tests |
| `mkdocs build --strict` | PASS |
| `scripts/execute_notebooks.py` | **FAIL — 56/61** (5 Gemma notebooks) |

Do not regress any passing check.

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

After editing, validate:

```bash
uv run python -c "
import nbformat,sys
nb=nbformat.read(sys.argv[1],as_version=4); nbformat.validate(nb); print('valid')
" notebooks/<file>.ipynb
```

### 4.4 Git

- Branch: work on the branch you were assigned; never push to `master`.
- One work item per commit; reference the item id in the message body.
- Commit messages in Italian, imperative, explaining *why* not just *what*.
- Do not commit `.venv/`, `.uv-cache/`, `.notebook-runtime/`, `site/`,
  `models/` — all already in `.gitignore`.

---

## 5. Work item index

| ID | Title | Priority | Blocked by |
|---|---|---|---|
| WI-1 | Fix the Gemma availability guard (5 notebooks) | P0 | — |
| WI-2 | Remove the absolute path from the site homepage | P0 | — |
| WI-3 | Rebuild `docs/glossary.md` | P1 | — |
| WI-4 | Regenerate `docs/references.md` from lesson sources | P1 | — |
| WI-5 | Add exercise + solution to lessons 31-60 | P1 | D2 |
| WI-6 | Raise theory density in lessons 31-60 | P2 | D2 |
| WI-7 | Align README and `docs/index.md` with reality | P1 | WI-5 |
| WI-8 | Retire stale `exercises/`, `solutions/`, `templates/lesson.md` | P2 | — |
| WI-9 | Seed the 21 non-deterministic notebooks | P2 | — |
| WI-10 | Make the consolidated notebook portable (Windows/macOS) | P2 | — |
| WI-11 | Reconcile `course.yaml` and `progress.yaml` with reality | P2 | D1, D2, D3 |
| WI-12 | Resolve the `mlops` module and the Vertex AI requirement | P3 | D1 |
| WI-13 | Extract capstone components into `src/memory_ai/` + tests | P3 | — |

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

## 7. Open decisions

These block the work items named. They are the course author's to make; do
not assume an answer.

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
