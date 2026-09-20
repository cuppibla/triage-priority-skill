---
name: triage-priority
description: Assign and defend a P0/P1/P2/P3 priority for any bug, incident, regression, or review finding using a fixed, decidable standard (blast radius x severity + escalators with floors), and sort mixed lists into a work order. Use when asked how urgent something is, what to fix first, or to triage a bug list, review findings, an incident, or a defect backlog - and whenever P0/P1/P2/P3 needs to be applied consistently. Not for feature requests or roadmap planning, not for estimating effort, and not for writing the fix itself.
---

# Priority triage standard — P0 / P1 / P2 / P3

One job: turn "this feels bad" into a level that two different people would land on
independently. Everything below is written so the answer is *derived*, not voted on.

## The one question

> **What breaks if nobody touches this for one week?**

Answer that in concrete terms first. If the answer is vague, the triage is not ready —
go get the missing fact (how many users? is there a workaround? is data still being
written wrong?) before naming a level. If you *can't* get it — you're triaging a pasted
list, the reporter is offline — score under a stated assumption, mark the level
provisional, and write the fact that would change it. Never stall on a missing fact;
never hide that it's missing.

## Step 1 — Score two axes

**Blast radius** — who is affected *right now*, not who theoretically could be:

| | |
|---|---|
| **All** | every user / the whole team / production is down |
| **Many** | a whole segment, tier, region, or a named large customer |
| **Some** | a minority path, one team, one integration |
| **Few** | rare edge case, one internal user, only reproducible on purpose |

**Nobody?** If no one is affected today — capacity headroom, tech debt, a feature
request, a refactor — it is not a defect and this standard does not triage it. Say
"roadmap, not triage", write the trigger that would turn it into a defect, and stop.
The one exception: an item with no current user impact but an escalator (below) starts
at **P3** and only the escalators can lift it. That is how a risk with zero breakage
still gets an honest number.

**Severity** — how bad is it for someone in that radius:

| | |
|---|---|
| **Blocked** | cannot complete the core job at all, no workaround |
| **Degraded** | can finish, but slow / lossy / manual workaround required |
| **Annoying** | works, but wrong-feeling, confusing, or needs a second try |
| **Cosmetic** | visible imperfection, no behavior change |

## Step 2 — Read the grid

|              | **Blocked** | **Degraded** | **Annoying** | **Cosmetic** |
|--------------|-------------|--------------|--------------|--------------|
| **All**      | P0          | P1           | P2           | P3           |
| **Many**     | P0          | P1           | P2           | P3           |
| **Some**     | P1          | P2           | P2           | P3           |
| **Few**      | P2          | P2           | P3           | P3           |

## Step 3 — Apply escalators (these override the grid, upward only)

**Each escalator that applies raises the level by one, capped at P0.** They stack: two
escalators on a P3 make it a P1. Two of them also carry a **floor** — a minimum level
that applies regardless of what the axes said, because these are risks, not breakage,
and the grid can't see them.

- **Data**: data is being lost, corrupted, or silently written wrong — and every hour adds more.
  *Floor: P1 while it is still being written wrong.*
- **Security**: exploitable without insider access, or credentials/PII are exposed (even
  internally). *Floor: P1. P0 if actively exploited, or the exposure is external.*
- **Money**: charges, payouts, or billing are wrong in either direction.
- **Legal / compliance**: a contractual SLA, audit, or regulatory deadline is at stake.
- **Trust**: publicly visible and embarrassing (status page, front page, customer demo tomorrow).
- **Blocking others**: someone else's work is stopped until this lands.
- **Decay**: the fix gets materially more expensive or impossible if delayed (migration
  window closing, logs about to roll off, release cut tomorrow).

Never *lower* a level with a "de-escalator". If it feels too high, the radius or
severity was scored wrong — go fix the score, not the verdict.

## The four levels, and what each actually commits you to

**P0 — stop the world.**
Drop what you're holding. Someone is paged, work continues outside normal hours, and
the status is communicated on a clock. A P0 is not "very important" — it is
"important enough to wreck someone's day for", and calling it P0 spends that.
*Done* = the bleeding has stopped, even by a hack, rollback, or feature flag. Then it
becomes a P1 for the real fix. Target: acknowledged in minutes, mitigated same day.

**P1 — next thing I touch.**
No pager, but it goes to the front of the current work, ahead of whatever is in flight
once that's at a safe stopping point. It has a named owner and a date. Target: this
week / this sprint / before the next release, whichever comes first.

**P2 — scheduled.**
Real, worth fixing, will be done in an upcoming cycle. It gets a backlog entry with
enough detail that a stranger could pick it up. Nobody is interrupted for it. Target:
a named upcoming cycle, not "soon".

**P3 — opportunistic.**
Fix it if you're already in that file, or never. A P3 is an explicit statement that
shipping without this is fine. Aging out and being closed is a normal, healthy end for
a P3 — not a failure.

## Rules that keep the scale honest

1. **Priority is a schedule, not a feeling.** It answers *when*, never *how much we care*.
   "This really matters to me" is not evidence; "three customers are blocked today" is.
2. **Severity ≠ priority.** A total crash in a feature nobody uses is severity-high,
   priority-P2. A cosmetic typo on the pricing page during a launch is severity-low, P1
   (All × Cosmetic = P3, + trust + decay).
3. **Effort never sets the level.** A two-minute fix and a two-week fix with identical
   impact are the same priority. Effort decides *order within* a level, nothing more.
4. **P0 has a budget.** More than one or two open P0s means the label has stopped
   carrying information. If everything is P0, re-triage the whole list from scratch.
5. **Unknowns default down, with a trigger.** When torn between two levels, take the
   lower one and write the fact that would raise it ("P2 → P1 if this also hits the
   paid tier"). *Exception:* if the unknown is one of the escalators (could be data
   loss, could be exploitable), take the higher level and timebox an investigation —
   an hour of looking beats a week of guessing wrong.
6. **Mitigation downgrades, it doesn't close.** Rolled back, flagged off, or patched by
   hand → drop a level and keep the item open for the durable fix. Closing here is how
   the same P0 happens twice.
7. **Re-triage on a clock.** A P1 that's been open two weeks is lying: either it's a P2
   or it needs an owner today. Priority is assigned against a moment, and moments expire.
8. **Every P0 and P1 needs a named person.** P2 and P3 may sit unowned; P0/P1 without an
   owner are not triaged, just labeled.

## Output format

When triaging a single item, answer in exactly this shape — the reasoning is the
deliverable, the letter alone is worthless:

```
P1 — checkout retries drop the second payment attempt
Radius × severity: Some × Degraded  (paid tier, ~2% of retries, card works on 3rd try)
Escalator: money (charges land twice in ~2% of retries) → would be P2, raised
If ignored a week: ~40 double-charges, each a manual refund + support ticket
Owner / by: @owner, before Friday's release cut
Raise to P0 if: double-charges exceed refund capacity, or any charge is unrefundable
Drop to P2 if: the retry path turns out to be dead code behind a disabled flag
```

If the level rests on an unverified fact (rule 5), suffix it — `P1?` — and add one line:
`Provisional until: <what you will check>, by <when>`. A provisional level with no
check and no deadline is just a guess with a question mark on it.

For a **list**, emit one table with the columns
`Level | Item | Radius × Severity | Escalator | Why | Owner`, sorted P0→P3, and within
a level ordered by: (1) unblocks other people, (2) decays if delayed, (3) cheapest first.
Then state the cut line: what you'd actually do this week and what you are consciously
not doing.

## Calibration examples

Argue with these before arguing with the grid — they are the standard's real definition.

- **Every WebSocket reconnect drops messages sent during the gap; all users, chat is the product.**
  All × Degraded (users can still chat; "lossy" is the Degraded definition) = P1,
  + data escalator → **P0**.
- **Same bug, but only when the tab is backgrounded on Safari, and messages resync after 30s.**
  Some × Degraded → **P2**. Self-healing, workaround is "wait".
- **Messages arrive out of order in rooms over 50 people; the whole enterprise tier is >50.**
  Many × Degraded = P1; trust escalator (a customer demo Thursday) → **P0**.
- **Auth token in a debug log, logs are internal-only and retained 7 days.**
  Nobody is affected, so it starts at P3. Security escalator (credentials exposed) → P2,
  and its floor already says at least P1; decay (rotate before the 7-day window) → **P1**.
  Derived two ways, same answer.
- **Typing indicator sticks on after a user leaves.**
  All × Cosmetic → **P3**. Everyone sees it, nobody is harmed.
- **A helper function is duplicated in four files.**
  Nobody is affected and no escalator applies → **roadmap, not triage**. If it has
  already caused a bug, triage *that* bug and let this ride along with the fix.
- **Load test shows the server falls over at 10k concurrent; today's peak is 400.**
  Nobody is affected yet and nothing is decaying → **roadmap, not triage**, with the
  trigger written down: "becomes a P1 the day sustained load passes 3k." Future pain is
  planning, not priority.
- **One internal admin page 500s; there is a CLI that does the same thing.**
  Few × Degraded → **P2**.

## Anti-patterns to name out loud when you see them

- **The escalation ladder.** Filing P1 expecting to be negotiated down. Score the axes;
  don't bid.
- **Priority by requester.** The loudest voice or the most senior title is not a blast radius.
- **Permanent P2 purgatory.** If it's been re-scheduled three cycles, it's a P3 — close it
  and say so, or promote it.
- **Aggregating for drama.** Twelve P3s are not a P1. (Twelve P3s *that share one root
  cause* are one item — triage the root cause.)
