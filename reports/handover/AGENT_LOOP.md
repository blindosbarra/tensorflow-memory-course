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

0. Preflight — two checks, and only one of them may stop you.
   a) Machinery present:
        test -f reports/handover/queue.yaml && test -f scripts/next_work_item.py
      If either is missing you are on a checkout without the queue. STOP and
      report "machinery missing". Do NOT report this as "nothing left to do"
      — it is the opposite, and confusing the two wasted the first attempt.
   b) Freshness — is this checkout current? Use whichever works:
        - if `git remote` lists a remote: `git fetch origin master` and check
          your HEAD contains origin/master;
        - otherwise check by CONTENT, which needs no remote:
            uv run python scripts/next_work_item.py --board
          A current checkout shows WI-1, WI-2, WI-3, WI-4 and WI-7 as `done`,
          WI-5 as `cancelled`, and no decision listed as open. If instead the
          board offers you WI-3 or WI-4, the checkout predates work that is
          already merged: STOP and say so.
      **A missing remote is not a reason to stop.** Some sandboxes check the
      repository out with no `origin` and on a branch of their own choosing;
      that is normal and says nothing about the work. Only a *stale board*
      stops you here.
   c) Branch: work on whatever branch this environment gave you — do not
      require a particular name, and do not create one if the harness owns
      that. The only hard rule is: never commit or push to `master`.
1. Run: uv run python scripts/next_work_item.py
   Key on the SENTINEL line it prints, not on the exit code:
     SENTINEL: PICK <id>           → work that item
     SENTINEL: ALL-DONE            → stop, report success
     SENTINEL: NOTHING-ACTIONABLE  → stop, report the open decisions
     SENTINEL: QUEUE-MALFORMED     → fix the queue file and stop
     SENTINEL: QUEUE-MISSING       → see step 0; stop
     no SENTINEL line at all       → the script did not run. This is an
       environment problem. Report it as such and stop. Never read it as
       a statement about the work.
2. Read that item's section in reports/SDD-remediation-2026-08-06.md, and
   read sections 1-5 of the same document before your first edit.
3. Set the item's status to in_progress in reports/handover/queue.yaml.
4. Implement exactly that item. Nothing else.
5. Verify in two tiers. Run `verify_fast` first — it is cheap and catches
   most mistakes. Then run `verify`; the item is not done until those pass.
   If `verify_env` names an environment you cannot build (the ml extra is
   ~600 MB and needs network), see "When the environment will not cooperate"
   below: commit the work with the item left `todo`. Do NOT revert it.
6. Commit the work and the queue update together, in Italian, naming the
   item id in the message body. Push to the branch this environment gave
   you, or the one named in this iteration's instructions if it named one.
   Never a branch named in the queue file, and never `master`. If the
   harness opens the pull request for you, let it.
7. Set the item's status to done and stop. One item per iteration.

Never resolve a decision yourself; D1-D3 are already resolved, treat them as
settled and do not undo work implementing them. Never push to master.
Never mark an item done without having run its verify commands.
Never end an iteration silently: commit something, or say what stopped you.
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

If the item turns out to be bigger than one iteration (WI-6, WI-12 and WI-13
all are), split it: complete a coherent piece, record what remains in the item's
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

Both apply to the **full** run only. A `--only` run of a few notebooks leaves
`datasets/processed/` dirty on purpose: several lessons write the same file
in sequence and the committed version belongs to the last writer. Run
`git checkout -- datasets/` after a partial run, and never read a dirty tree
after `--only` as a determinism failure.

If verification fails **because the change is wrong**, revert your changes,
set the item back to `todo`, record what failed in its `notes`, and stop. A
reverted iteration with an accurate note is worth more than a half-finished
commit.

### When the environment will not cooperate

This is a different case and it has a different answer. If the change is
sound but you *cannot run* the verification — no network for the ~600 MB ml
extra, the sync times out, the sandbox has no room — **do not revert**.
Reverting throws away good work because of a machine, and leaves the next
iteration to redo it from nothing.

Instead:

1. Commit the change, clearly marked as unverified in the message body.
2. Leave the item's status at `todo` and add to its `notes`: what you did,
   which verify command you could not run, and the exact error.
3. Push and stop, reporting that the item needs verification in an
   environment that has the ml extra.

An unverified but committed change with an honest note is recoverable in
one minute by whoever has the environment. A revert is not recoverable at
all.

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

**Never resolve a decision.** Decisions in the queue's `meta` belong to the
course author. They carry recommendations; a recommendation is not an answer.
If every remaining item is waiting on one, the picker prints
`SENTINEL: NOTHING-ACTIONABLE` with the open questions — that is the loop's
signal to stop and ask, not to choose.

`D1`, `D2` and `D3` were all **resolved on 2026-08-07** and no longer block
anything; their outcomes are in `course/research_gaps.md`. Treat a resolved
decision as settled: do not relitigate it, and do not undo work that
implements it. **WI-5 is `cancelled` by D2** — the course author chose to
correct the promise instead of writing thirty exercises. Cancelled is not
"todo, later"; reopening it needs a new decision from the author.

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

Re-verified against the working tree on **2026-08-07**, after the decisions
were taken.

| | |
|---|---|
| Done and verified | WI-1, WI-2, WI-7 |
| Cancelled by decision D2 | WI-5 |
| Ready now — nothing blocks any of them | WI-3, WI-4, WI-6, WI-8, WI-9, WI-10, WI-11, WI-12, WI-13 |

**No item is waiting on a human any more.** D1, D2 and D3 are resolved, so
the picker will keep offering work until all nine remaining items are done.
Suggested order is simply the picker's: P1 first (WI-3, WI-4), then the P2
group, then P3.

Two of the nine are large and will not fit one iteration — **WI-6** (raise
theory depth across 30 notebooks) and **WI-12** (write the reduced `mlops`
path decided in D1). Split them as section 4 describes: complete a coherent
piece, record what remains in the item's `notes`, leave it `in_progress`,
commit, stop.

Baseline now: `ruff`, `mypy src`, `pytest` and `mkdocs build --strict` all
pass, and `scripts/execute_notebooks.py` reports **61/61** with a clean
`git status` afterwards — verified twice. That is the state you must not
regress.

## A preflight must not out-stop the work

The freshness check in step 0 was first written as a bare
`git fetch origin master`, with "stop if you cannot confirm". On 2026-08-08 a
loop ran in a sandbox that checks the repository out with **no `origin`
remote and on a branch called `work`**. The fetch failed, the agent could not
confirm freshness, and it stopped having changed nothing — correct by the
letter of the instruction, useless in effect.

That is the same shape as the exit-code bug below: a signal that cannot tell
"this environment is different" from "it is unsafe to proceed", defaulting to
silence. A guard that stops the work it was written to protect is worse than
no guard, because it looks like diligence.

The fix is the content-based fallback in step 0b: freshness is a property of
the queue, which is in the repository, so it can always be checked without a
network or a remote. Prefer a check on something you already have over a
check on something the environment might not provide.

## What the first attempt taught us

The loop ran once, on 2026-08-07, and produced **zero commits**. The branch
`agent/complete-sdd-remediation` was created and pushed at exactly the merge
commit of PR #1, with nothing on top.

The cause was mechanical, not a judgement failure. This procedure, the queue
and the picker were committed to `claude/codebase-review-status-0ufpuv`
*eleven minutes after* PR #1 merged, so they never reached `master`. The
agent branched from `master`, ran step 1, and got the shell's answer for a
script that does not exist: **exit code 2** — which the old prompt above
defined as "all done, or a decision is needed". The agent stopped and
reported no work, exactly as instructed.

Three changes above come directly from that: the preflight in step 0, the
sentinel lines instead of bare exit codes, and the rule that an iteration
never ends silently. The full analysis is section 6 of the SDD.
