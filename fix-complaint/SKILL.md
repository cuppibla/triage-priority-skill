---
name: fix-complaint
description: Fix one numbered user complaint (complaints/NN.md) in a chat-workbench scenario the safe way — verification plan first, reproduce the bug, find the real root cause, pick the fix and say why, test thoroughly, verify on a fresh checkout, deliver on a branch named fixN-<slug>, and end with a report a human can read in one minute in very easy English. Use whenever Annie says "fix complaint N", "fix complaints 2", "work complaint 3", "修 complaint", pastes a complaint file, or asks for a root cause + fix + proof for a reported bug in any scenario-NN folder — even if she doesn't say "skill". Not for triage/priority (use triage-priority) or for reviewing someone else's PR.
---

# Fix a complaint, prove it, explain it in one minute

The goal is not "make the error go away". The goal is: **Annie can trust the fix
without re-doing the work, and understand it in 60 seconds.** Every step below exists
to earn that trust. Skipping a step saves five minutes and costs the whole point.

Order matters. Do the steps in this order and write each one down as you go, because
the final report is mostly assembled from these notes.

## Step 0 — Read, don't guess

- Read `complaints/NN.md`. It is a symptom, written by a user. Treat it like a bug
  report, not a spec: the user says what they saw, not what is broken.
- Read the scenario's `CLAUDE.md` (commands, architecture, conventions). Read
  `NOTES.md` and `PULL_REQUESTS.md` if present — a teammate may already have a theory
  or an open PR. Their theory can be wrong; check it, don't adopt it.
- **Spoiler rule:** do not open `../reference/` or `../run-artifacts/`. Those hold the
  answers. The value of this exercise is finding it yourself.

## Step 1 — Verification plan, BEFORE touching code

Write this first, in the reply, so the plan can't be bent later to fit whatever you
happened to change:

```
## Verification plan (written before the fix)
Bug in one sentence: ...
I will call it fixed when:
  1. <observable thing>  — checked by: <exact command / test name>
  2. ...
Reproduce: <exact steps or script that should FAIL today>
Must still pass: npm test (+ anything else CLAUDE.md lists)
Real-app check: <yes/no, and how — e.g. two tabs on two workers>
```

Why first: a plan written after the fix tends to test the fix, not the complaint.

## Step 2 — Reproduce it

Make the bug happen on `main` before changing anything. Prefer a small script or a
failing test over clicking around, because you will re-run it after the fix and put
it in the report. Save it under `$CLAUDE_JOB_DIR/tmp/` or `tests/` (if it will become
the regression test).

If you cannot reproduce: say so plainly, and do not "fix" it anyway. Try the
conditions in the complaint literally (busy room, two tabs, two workers, reconnect,
a specific user). If it truly won't show, report that as the result.

## Step 3 — Root cause, not first suspect

- Find the mechanism: which line does the wrong thing, and *why* it is wrong. Write it
  as `path/file.js:line` plus one plain sentence.
- Ask "why does that line exist / what did the author assume?" — the answer is usually
  the real cause (e.g. "assumes one process", "assumes ack arrives before broadcast").
- Separate **symptom** (what the user saw), **trigger** (when it happens) and **cause**
  (the broken assumption). Cluster scenarios: check whether the state is per-process.
- Look one step further: does the same broken assumption exist elsewhere? Note it even
  if you don't fix it.

## Step 4 — Choose the fix and say why

List 2–3 candidate fixes in one line each, then choose. Prefer, in order:
smallest change that fixes the **cause** (not the symptom) → keeps existing behavior
for everyone else → does not add new per-process state → easy to read.

Write down what you rejected and why. If an open PR in `PULL_REQUESTS.md` proposes a
fix, say whether it is right, partial, or wrong — that is part of the answer.

## Step 5 — Branch and implement

- Branch from `main`: `fixN-<short-slug>` (e.g. `fix2-busy-send-errors`). The
  `fixN` prefix is how Annie finds it later — keep it exact.
- If other jobs may be running in the same checkout, use a git worktree.
- Keep the diff small. Fix the cause. Don't refactor neighbors, don't reformat.
- Add a regression test that **fails on main and passes on the branch**. Put it next to
  the existing tests, using the same runner (`node --test`, etc.).

## Step 6 — Test thoroughly (this is where fixes usually turn out to be wrong)

Run and record the output of each:

1. The reproduction from Step 2 — must now pass.
2. The new regression test, run **twice**: once on main (expect fail), once on the
   branch (expect pass). Use `git stash` / `git checkout main -- <file>` to prove it.
3. The full existing suite (`npm test` or whatever CLAUDE.md says).
4. The real app, if the bug lives in runtime behavior (cluster, sockets, timing,
   reconnect). Start it the way users run it (`npm start`, not only single-process),
   do the thing from the complaint, watch it work. Say what you actually did.
5. Neighbors: skim the other complaints. Did the fix make any of them better, worse,
   or unchanged? One line each for the ones it touches.
6. Flaky-check: if the bug was timing or load related, run the repro 5–10 times.

If any of these cannot be run (no browser, no port, no key), say **which** and why.
Never write "verified" for something you did not run.

## Step 7 — Verify on a clean checkout

Fresh eyes, fresh tree: `git stash -u` (or a new worktree of the branch), `npm install`
if needed, run the suite and the repro once more from scratch. This catches
"works because of a leftover file / db / env". Commit with a message whose first line
is `fixN: <what changed>` and whose body is the root cause in two sentences.

## Step 8 — The one-minute report

This is the deliverable. Rules: **under 250 words, no sentence over 20 words, no
jargon without a 3-word gloss, every claim next to the command that proves it.** Write
for a smart person who did not read the code. Use this exact shape:

```
# Complaint N — <title, max 8 words>

**What users saw:** one sentence, in their words.

**Root cause:** one or two sentences. `file.js:line`. The broken assumption.

**The fix:** what changed, one or two sentences. Files touched.

**Why this fix:** why it beats the alternatives, one or two sentences.
Rejected: <alt> — because ...

**Proof:**
| Check | On main | On fixN branch |
|---|---|---|
| repro script | fails (error text) | passes |
| new test `<name>` | fails | passes |
| npm test | N pass | N+1 pass |
| real app: <what I did> | bug seen | works |

**Not covered / risk:** one line. Or "nothing I know of".

**Branch:** `fixN-<slug>`, commit <sha>. Diff: +A −B lines in <files>.
```

Also save the same report to `fixes/complaint-NN.md` on the branch, so it travels
with the code. Then put the report at the end of the chat reply — it is the last thing
Annie reads, so it must stand alone.

## Honesty rules (short)

- A step you skipped is reported as skipped, with the reason.
- A test that failed is reported as failed, with the output.
- "Could not reproduce" is a valid, complete result.
- Do not widen scope: one complaint, one branch, one root cause. If you find a second
  bug, write it under "Not covered" and stop.
