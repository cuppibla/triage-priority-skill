# PR review and triage skills

Reusable skills for prioritizing PR queues, reviewing pull requests, prioritizing defects, and fixing reported problems.

| Skill | Purpose |
| --- | --- |
| [`pr-review`](pr-review/SKILL.md) | Review one PR or branch, verify important behavior, and produce findings backed by evidence. |
| [`pr-triage`](pr-triage/SKILL.md) | Scan a PR queue, explain the review order, and recommend the next useful action. |
| [`triage-priority`](triage-priority/SKILL.md) | Assign P0/P1/P2/P3 to defects and backlog items using impact, severity, and escalators. |
| [`fix-complaint`](fix-complaint/SKILL.md) | Reproduce and fix one numbered complaint, verify the result, and deliver a focused change. |

## Install pr-review in Claude Code

The same installer sets up **both `pr-review` and `pr-triage`**.

Run these commands in a **terminal inside the repository you want to review**. Requirements: Git, Python 3.8+, and Claude Code. This public download needs no GitHub login; accessing a private PR may still require authentication.

```sh
pr_review_source="$(mktemp -d)"
git clone --depth 1 https://github.com/cuppibla/triage-priority-skill.git "$pr_review_source" &&
python3 "$pr_review_source/install.py" --project "$PWD"
```

The installer copies both skills to:

```text
your-project/
  .claude/
    skills/
      pr-review/
        SKILL.md
        references/
          ai-changes.md
      pr-triage/
        SKILL.md
```

An identical installation is safe to repeat. If you already installed `pr-review` from this repository, rerun these commands to download the current version and add `pr-triage`. A different existing skill folder is preserved and reported before either skill is copied; compare or back up that folder before replacing it.

Then, **inside Claude Code**:

```text
/reload-skills
/pr-triage open PRs in this repository
```

After choosing a PR, use `/pr-review review #42`. For an already assigned PR, go directly to that review command.

If `/reload-skills` is unavailable, restart Claude Code from the project directory. Install in the same environment where Claude runs: a local installation does not install the skill in a remote workspace. Skill discovery and reload behavior are documented in [Claude Code's skills guide](https://code.claude.com/docs/en/skills).

### Install for all your local projects

After the clone above, use this command instead of `--project`:

```sh
python3 "$pr_review_source/install.py" --user
```

This installs to `~/.claude/skills/pr-review/` and `~/.claude/skills/pr-triage/`. You only need one installation scope.

### Download without Git

Download the [repository ZIP](https://github.com/cuppibla/triage-priority-skill/archive/refs/heads/main.zip), extract it, and run the installer with the path to your target repository:

```sh
python3 /path/to/triage-priority-skill-main/install.py --project /path/to/your-project
```

The installer uses only Python's standard library and works offline after downloading. Without Python, manually copy the entire `pr-review` and `pr-triage` folders into your project's `.claude/skills/` directory, keeping the directory structure above. You can also copy just one of those folders to install that skill alone.

### Troubleshoot an unknown command

- Confirm `.claude/skills/<skill-name>/SKILL.md` exists in the project where Claude runs, or in `~/.claude/skills/<skill-name>/SKILL.md` for a personal install. Replace `<skill-name>` with `pr-review` or `pr-triage`.
- Run `/reload-skills`, or restart Claude Code from that project.
- Use `/pr-review` or `/pr-triage`; adding a PR number cannot make an uninstalled skill discoverable.
- If the wrong version loads, check for another installation of that skill. A personal skill takes precedence over a project skill with the same name; see the [official precedence rules](https://code.claude.com/docs/en/skills#resolve-skills-that-share-a-name).

## Use pr-review

| Command | Result |
| --- | --- |
| `/pr-review review #42` | Complete private review of the PR in the current repository. |
| `/pr-review review <PR URL>` | Review a specific PR with an unambiguous repository and target. |
| `/pr-review review current branch against main` | Review a local branch against the specified base. |
| `/pr-review scout #42` | Initial analysis: behavior, callers, risks, and proposed checks. Stops before deeper verification. |
| `/pr-review draft-comments #42` | Draft unpublished comments from verified findings at the current revision. |

For a normal review, go directly to `review`. `scout` is optional when you want to agree on the investigation scope first. There is **no fixed time budget**: add a time limit only when you have one, for example `/pr-review review #42; initial pass, up to 5 minutes`. The report must identify incomplete verification.

You do not need to repeat the built-in defaults. The skill already asks for focused checks, evidence, explicit uncertainty, no application-code changes, and private output. It does not post comments, submit a GitHub review, or merge unless you separately request that action. Skill instructions guide the agent; they do not replace the tool's permission controls.

## How it evaluates a PR

The review starts with the intended behavior, actual diff, and affected callers. It applies the relevant checks below, with more depth where the change introduces risk.

| Angle | What it checks |
| --- | --- |
| Correctness and scope | Requirements, boundaries, error cases, caller behavior, and hidden changes in refactors. |
| Security and privacy | Authorization, tenant isolation, input validation, sensitive data, and existing safeguards. |
| State and reliability | Concurrency, retries, cancellation, duplicate side effects, partial failures, and cleanup. |
| Compatibility and operations | API/schema changes, migration order, rollout/rollback, resource limits, and failure signals. |
| Test quality | Assertions against expected behavior, boundary/failure cases, realistic integration, and misleading mocks. |
| Clarity and description | Maintainability, local conventions, documentation, and whether the PR's claims match the code. |
| Applied AI, when relevant | Message/tool protocols, agent limits, untrusted content, caching, latency metrics, and model-quality evaluation. |

### What counts as testing evidence?

A green CI badge or many tests cannot establish complete correctness. The skill connects important requirements to scenarios and actual evidence:

```text
Requirement or risk | Scenario | Test/check | Result or gap
```

It inspects assertions, identifies the revision tested by CI, distinguishes passing from skipped or pending checks, and runs relevant tests or a small reproducer. For a suspected regression, it compares base and head when practical. For a bug fix, it checks whether a regression test would fail before the fix and pass afterward. Unavailable services, missing credentials, and unrun checks remain explicit gaps.

Before retaining a finding, it checks alternative explanations such as an existing guard or an intentional contract change. Each confirmed finding includes a location, concrete trigger, expected versus actual behavior, user impact, evidence, and a proportionate fix direction. Zero findings is a valid outcome.

The final report contains a short behavior summary, findings ordered by impact, the test-evidence table, remaining uncertainty, and a recommendation: approve, request changes, or seek clarification. The reviewer owns the final decision.

## Reviewing a queue

Use [`pr-triage`](pr-triage/SKILL.md) to choose the order, then use `pr-review` for the selected PR:

```text
/pr-triage open PRs in this repository
/pr-review review #42
```

To restrict the queue, use `/pr-triage #12 #18 #42` or specify a repository and filter in plain language. The triage skill returns a ranked plan and stops; it continues into review only if you also ask it to. It does not impose a fixed time budget.

If a specific PR is assigned, review it directly. If choosing the order is part of the task, do one shallow pass over the queue before deep review. Use metadata, descriptions, changed files, CI status, and explicit dependencies; inspect selected diffs where those signals are ambiguous. A high-risk change deserves attention, but risk alone does not prove a defect or urgency.

Order the next useful actions by:

1. **Known urgency:** active incidents, known security/data issues, or a real release deadline.
2. **Dependencies:** changes that unblock other work; inspect prerequisite PRs before their dependents.
3. **Review risk:** changes to permissions, data, payments, state, or widely used contracts that need early investigation.
4. **Readiness and effort:** decide whether the useful next step is review, CI diagnosis, a clarification, or waiting on the author. Failing CI does not erase an urgent issue.
5. **Age:** avoid starvation; use oldest-first among otherwise comparable items and consider long waits explicitly.

The skill returns a short table: `Order | PR | Why now | Evidence/unknowns | Ready for what? | Next action`, plus the first PR to inspect and the deferred work. It separates verified urgency from suspected change risk, notes missing metadata, and reports if only part of the queue was inspected. You can add context to the command:

```text
/pr-triage open PRs in this repository; release is Friday;
prioritize release blockers and dependency chains, then explain what can wait.
```

`pr-triage` orders PR reviews; `pr-review` evaluates individual changes; `triage-priority` assigns work priority to defects and backlog items. Defect priority and PR review order answer different questions.

Do not start a session for every PR at once. Begin with one review. If independent reviews would help, use a small number of sessions you can supervise, each with a clearly identified PR and isolated checkout. Avoid concurrent branch changes or tests sharing mutable state. The skill does not automatically launch parallel agents.

## Other skills

Install `triage-priority` or `fix-complaint` by copying that skill's complete folder into `.claude/skills/` for one project, or `~/.claude/skills/` for personal use. The `install.py` script installs `pr-review` and `pr-triage`.

The [triage-priority standard](triage-priority/SKILL.md) defines its blast-radius/severity grid, escalators, calibration examples, and output format. The [fix-complaint workflow](fix-complaint/SKILL.md) covers reproduction, root cause, implementation, verification, and delivery for numbered complaints.

## License

[MIT](LICENSE)
