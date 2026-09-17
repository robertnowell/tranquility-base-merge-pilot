# Protected queue pilot: 17 September 2026

The isolated coordination pilot passed its observed acceptance cases. It does
not establish the production macOS burst-latency target.

Installation 162601389 was verified in the owner's GitHub settings at 15:04
Pacific: only `robertnowell/tranquility-base-merge-pilot` is selected. Owner
authentication and Chrome access are resolved. No product repository access,
branch-protection change, or ownership transfer was performed.

## Three-ready-PR burst

The fixed baseline was a0fe882. PRs 1–3 were already green when labeled within
four seconds. They merged in order, through the bot, with strict freshness and
the required Actions-provided Source audit still enforced.

| PR | Admission UTC | Merge UTC | Request to merge | Observed bot head updates |
| --- | --- | --- | --- | --- |
| [1](https://github.com/robertnowell/tranquility-base-merge-pilot/pull/1) | 22:07:03 | 22:07:12 | 9s | 0 |
| [2](https://github.com/robertnowell/tranquility-base-merge-pilot/pull/2) | 22:07:05 | 22:08:03 | 58s | 1 |
| [3](https://github.com/robertnowell/tranquility-base-merge-pilot/pull/3) | 22:07:07 | 22:08:51 | 104s | 1 |

Median 58s; maximum 104s. The first PR reused its valid unchanged-base audit.
Only PR 2 was updated after PR 1 merged; PR 3 remained unchanged until PR 2
merged. The two new audit jobs took 25s and 24s, respectively; run creation to
job start took 4s and 3s. This interval includes scheduling/setup, not just
runner-capacity waiting. Three short Linux samples cannot support a stable p95
or a forecast for six-minute macOS audits.

## Safety cases

| Case | Observed behavior |
| --- | --- |
| Edited admitted PR [4](https://github.com/robertnowell/tranquility-base-merge-pilot/pull/4) | The original in-flight audit was canceled after an edit. Only the new head passed and merged. |
| Failed required check [5](https://github.com/robertnowell/tranquility-base-merge-pilot/pull/5) | The PR remained open with Source audit FAILURE despite the separate neutral bot status. Two blocked observations were 29.35s apart. Repair required fresh successful validation before merge. |
| Real text conflict [6](https://github.com/robertnowell/tranquility-base-merge-pilot/pull/6) / [7](https://github.com/robertnowell/tranquility-base-merge-pilot/pull/7) | After PR 6 landed, PR 7 became DIRTY. The bot removed admission and commented. Explicit resolution preserved both variants and passed fresh CI. Re-admission was then required. |
| Explicit hold [8](https://github.com/robertnowell/tranquility-base-merge-pilot/pull/8) | A clean, green candidate stayed open with queue-hold across observations 43.96s apart. After editing, the hold was released at 22:24:34 while the current audit was running. The PR stayed open/blocked, passed at 22:24:54, and merged at 22:24:57. Earlier green heads did not authorize the final source. |

For all eight PRs, the merge actor was `kodiakhq[bot]`. The successful audit log
identified the actual synthetic merge candidate; its complete Git file tree
equals the squash merge's tree. No PR was manually merged. Final protection
still requires strict Source audit from Actions app 15368, includes
administrators, requires linear history, and allows only squash merging.

This is observed compatibility, not a proof against every race or outage. A
neutral conclusion on Source audit itself was not separately injected. A
neutral bot status alongside a failed required audit was tested.

## Operational correction found by the pilot

PR 7's conflict removed `merge-queue` at 22:16:08. Its resolved source passed at
22:17:19 but stayed open because admission was absent. Re-admitted at 22:21:44,
it merged seven seconds later. The initial admission-to-merge interval was
6m31s, including deliberate conflict resolution and operator investigation;
do not report only the seven-second recovery as its full waiting time.

The owner must resolve/review the conflict and explicitly re-admit the PR.
Monitoring needs to distinguish a conflict, a resolved PR awaiting re-admission,
an explicit hold, checking, and unavailable status. Automatically restoring a
removed label would discard the explicit admission policy.

The hold harness briefly observed GitHub's previous PR head immediately after
a push and stopped without releasing the hold. By the next attempt that audit
had finished, so a third revision was used to capture the required in-flight
release. The acceptance now describes waiting for GitHub to expose the expected
head and preserving the hold when the sampling window is missed. This was an
observer synchronization correction; no unvalidated merge occurred.

## Evidence and next boundary

Machine-readable evidence is in [evidence/2026-09-17](evidence/2026-09-17):
burst timing, all eight source/merge proofs, sampled safety states, and policy.
Winning workflow URLs are derived from the recorded run IDs. Raw snapshots,
workflow logs and local conflict reproduction remain in the workstream's local
evidence directory. The measurement branch remained separate from main for
the entire experiment.

See [PRODUCTION-READINESS.md](PRODUCTION-READINESS.md) for the remaining concrete
work. Fixture completion does not install a production queue or satisfy the
ten-agent waiting-time objective. Product issue
[493](https://github.com/robertnowell/tranquility-base/issues/493) remains open.
