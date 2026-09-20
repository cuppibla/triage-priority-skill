# triage-priority

A bug triage skill. It turns "this feels bad" into a P0/P1/P2/P3 that two people
would land on independently — a fixed, decidable standard instead of a vote.

## The standard, in short

**One question:** *What breaks if nobody touches this for one week?* If that can't be
answered concretely, the triage isn't ready — go find the missing fact first.

**Score two axes.** Blast radius (All / Many / Some / Few — who is affected *now*, not
theoretically) against severity (Blocked / Degraded / Annoying / Cosmetic).

|          | Blocked | Degraded | Annoying | Cosmetic |
|----------|---------|----------|----------|----------|
| **All**  | P0      | P1       | P2       | P3       |
| **Many** | P0      | P1       | P2       | P3       |
| **Some** | P1      | P2       | P2       | P3       |
| **Few**  | P2      | P2       | P3       | P3       |

**Apply escalators**, upward only: data loss or corruption, security, money, legal/SLA,
public trust, blocking others, or decay — the fix getting more expensive the longer it
waits. Each one that applies adds a level, capped at P0, and they stack. Data and
security also carry a **floor** of P1 (P0 if actively exploited), because they are risks
rather than breakage and the grid can't see them. There are no de-escalators; if a
verdict feels too high, an axis was scored wrong.

**Nobody affected today?** Capacity headroom, tech debt, and feature requests aren't
defects — the standard says "roadmap, not triage", writes down the trigger that would
change that, and stops. A zero-impact item that *does* carry an escalator starts at P3
and only the escalators lift it.

**What the levels commit you to:**

| | Meaning | Target |
|---|---|---|
| **P0** | Stop the world. Paged, off-hours, status on a clock. | Mitigated same day — a rollback or flag counts, then it becomes a P1 for the real fix. |
| **P1** | The next thing you touch. Named owner, has a date. | This week / before the next release. |
| **P2** | Scheduled into a named cycle. Nobody is interrupted. | An upcoming cycle, not "soon". |
| **P3** | Fix it if you're already in that file, or never. | Aging out and closing is a healthy end. |

## Rules that keep the scale honest

- Priority is a schedule, not a feeling. It answers *when*, never *how much we care*.
- Severity is not priority. A total crash in a feature nobody uses is P2; a typo on the
  pricing page during a launch is P1.
- Effort never sets the level — it only orders items *within* a level.
- P0 has a budget. More than one or two open means the label has stopped carrying
  information.
- Unknowns default *down*, with the fact written out that would raise them — unless the
  unknown is itself an escalator, in which case go up and timebox an investigation.
- Mitigation downgrades an item; it doesn't close it.
- A P1 open for two weeks is lying: it's either a P2 or it needs an owner today.
- P0 and P1 without a named owner aren't triaged, just labeled.

The full standard — escalator definitions, the output format, eight calibration
examples, and the anti-patterns worth naming out loud — is in
[`triage-priority/SKILL.md`](triage-priority/SKILL.md).

## Install

Copy the skill folder into your agent's skills directory:

```sh
git clone https://github.com/cuppibla/triage-priority-skill.git
cp -r triage-priority-skill/triage-priority ~/.claude/skills/
```

It then triggers on questions like "how urgent is this?", "what should I work on
first?", or any request to triage a bug list, a set of review findings, or a backlog.

## Output

A level on its own is worthless — the reasoning is the deliverable:

```
P1 - checkout retries drop the second payment attempt
Radius x severity: Many x Degraded  (paid tier only, card works on 3rd try)
Escalator: money (charges land twice in ~2% of retries) -> would be P2, raised
If ignored a week: ~40 double-charges, each a manual refund + support ticket
Owner / by: @owner, before Friday's release cut
Raise to P0 if: double-charges exceed refund capacity, or any charge is unrefundable
Drop to P2 if: the retry path turns out to be dead code behind a disabled flag
```

For a list, it emits one table sorted P0 to P3 — ordered within a level by what
unblocks other people, what decays if delayed, then cheapest first — and states the cut
line explicitly: what gets done this week, and what is consciously not being done.

## License

MIT
