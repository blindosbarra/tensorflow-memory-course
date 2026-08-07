# Agent loop — operating procedure

This is the handover for an autonomous coding loop working through the
remediation of this repository.

**Every iteration starts cold.** Nothing carries over in context. The durable
state is `reports/handover/queue.yaml`; the work specification is
`reports/SDD-remediation-2026-08-06.md`. Read them, do one thing, record it,
stop.

---

## The loop prompt

Paste this as the recurring instruction:

```text
Work one item from the remediation queue.

1. Run: uv run python scripts/next_work_item.py
   - exit 2 → stop the loop and report why (all done, or a decision is needed)
   - exit 3 → the queue file is malformed; fix it and stop
2. Read that item's section in reports/SDD-remediation-2026-08-06.md, and
   read sections 1-5 of the same document before your first edit.
3. Set the item's status to in_progress in reports/handover/queue.yaml.
4. Implement exactly that item. Nothing else.
5. Run the item's `verify` commands. They must all pass.
6. Commit the work and the queue update together, in Italian, naming the
   item id in the message body. Push to the assigned branch.
7. Set the item's status to done and stop. One item per iteration.

Never resolve a decision (D1, D2, D3) yourself. Never push to master.
Never mark an item done without having run its verify commands.
```

---

## One iteration in detail

### 1. Pick

```bash
uv run python scripts/next_work_item.py
```

It prints the single item to work on: id, priority, the SDD section to read,
the files in scope, the verification commands, and any note. Priority order
is P0 → P3, and items whose dependencies or decisions are unmet are never
offered.

Useful variants:

```bash
uv run python scripts/next_work_item.py --board   # every item and why it waits
uv run python scripts/next_work_item.py --check   # validate the queue only
```

### 2. Read before editing

Read **sections 1-5** of `reports/SDD-remediation-2026-08-06.md` before your
first edit of the iteration. They contain the context you do not have:
the teaching model, the repository layout, the environment, the conventions,
and the notebook-editing traps that break automated edits.

Then read the section for your item. It is written to be sufficient on its
own — exact files, exact cell indices, the change required, and what
"done" means.

### 3. Claim

Set the item's `status` to `in_progress` in `reports/handover/queue.yaml`
before you start. This is what lets a later iteration tell the difference
between "not started" and "abandoned halfway".

### 4. Implement

Only the item you picked. If you notice something else wrong, do not fix it:
add it to the queue as a new item, or note it in the existing item, and move
on. Unrelated changes are prohibited by `AGENTS.md` and make the diff
unreviewable.

If the item turns out to be bigger than one iteration (WI-13 is the likely
case), split it: complete a coherent piece, record what remains in the item's
`notes`, leave the status `in_progress`, commit, and stop. The next iteration
picks up from the note.

### 5. Verify

Run every command in the item's `verify` list. They must all pass before the
item can be marked done.

The commands are per-item on purpose: a documentation fix does not need the
15-minute notebook run, and a notebook fix does. Do not skip the ones that
are listed, and do not substitute a cheaper check.

Two invariants apply to any item that touches notebooks:

- `scripts/execute_notebooks.py` must report **61/61**;
- `git status --porcelain` must be **empty** after that run. The notebooks
  rewrite `datasets/processed/`, and today they regenerate it byte-identically
  to what is committed. A dirty tree after a run means determinism broke.

If verification fails and you cannot fix it within the iteration, revert your
changes, set the item back to `todo`, record what failed in its `notes`, and
stop. A reverted iteration with an accurate note is worth more than a
half-finished commit.

### 6. Commit and push

One item per commit. Message in Italian, imperative, explaining why and not
only what, naming the item id in the body. Commit the queue update in the
same commit as the work — they must not drift apart.

```bash
git push -u origin <assigned-branch>
```

Never push to `master`.

### 7. Record and stop

Set the item's `status` to `done`. Stop. Do not pick a second item in the
same iteration — the loop exists so that each item gets a clean start and a
reviewable diff.

---

## Guardrails

**Never resolve a decision.** `D1`, `D2` and `D3` in the queue's `meta`
belong to the course author. They carry recommendations; a recommendation is
not an answer. If every remaining item is waiting on one, the picker exits 2
and prints the open questions — that is the loop's signal to stop and ask,
not to choose.

**Never invent content.** If a source is missing, add an entry to
`course/research_gaps.md` instead of filling the gap. Do not invent APIs,
metrics, results, DOIs or compatibility claims. A previous review of this
repository caught a fabricated DOI marked `verified`; that must not recur.

**Never mark done what you have not verified.** The whole point of this
queue is that its state can be trusted by an agent that was not there.

**Never widen the scope.** The SDD item defines the boundary.

**Do not follow `templates/lesson.md`.** It still describes the model that
commit `3fa5799` deleted (separate starter `.py` files and dedicated pytest
suites). Following it rebuilds scaffolding that was deliberately removed.
WI-8 rewrites it.

---

## Recovering a crashed iteration

If the picker warns that an item was left `in_progress`:

1. Check whether a commit references it: `git log --oneline -5`.
2. If a commit exists and its verification passed, set the item to `done`.
3. If no commit exists and `git status` is clean, the iteration died before
   doing anything: set it back to `todo`.
4. If no commit exists and the tree is dirty, inspect the diff. Either finish
   it or revert it — do not build on top of an unknown partial state.

---

## Stop conditions

The loop should stop, and say so, when:

- the picker exits **2** with "All work items are done";
- the picker exits **2** because everything left needs a decision — report
  the open questions to the author;
- the picker exits **3**: the queue is malformed, which is a bug in the last
  iteration's edit;
- verification fails twice on the same item across two iterations. Something
  is wrong with the specification, not with the attempt; report it.

---

## Current state at handover

| | |
|---|---|
| Ready now, no decisions needed | WI-1, WI-2, WI-3, WI-4, WI-8, WI-9, WI-10, WI-13 |
| Waiting on D2 | WI-5, WI-6, WI-7 |
| Waiting on D1 | WI-12 |
| Waiting on D1, D2, D3 | WI-11 |

Eight items can be worked immediately. The first is WI-1, which is the only
place in the course where published code fails in a learner's hands, and its
fix has already been prototyped and verified.

Baseline at handover: `ruff`, `mypy src`, `pytest` and
`mkdocs build --strict` all pass; `scripts/execute_notebooks.py` reports
**56/61**, failing exactly the five notebooks WI-1 repairs.
