# Remaining production queue work

This is a prepared cutover specification, not an active production configuration.
The fixture install remains scoped to this repository. Its passing safety cases
remove the installation/compatibility unknown; they do not establish macOS
throughput or authorize a production access grant.

## 1. Make admission and delivery a single operator procedure

The product's existing `delivery.py watch --observe-only` can persist a named
delivery request before a PR is admitted. The durable worker processes recorded
requests only. A bare `gh pr edit --add-label merge-queue` does not invoke the
merge-command hook and must not be the sole delivery instruction.

For each specifically reviewed cohort PR, the requesting session must first run
from the current, clean persistent deployment checkout:

```
python3 scripts/delivery.py watch --pr NUMBER --owner SESSION --observe-only
```

Verify that the intended PR and owner are durably recorded. An open PR returns
75 because it remains pending; verify the returned state and absence of an
observation error instead of treating 75 as successful completion. This records
intent without installing. Only then may the coordinator add the admission
label. Verify the installed worker's heartbeat and follow the actual merge
through a process/source receipt. A label is never delivery evidence.

An integration check must cover a session ending after admission, bot merge,
preview/capture deferral, worker recovery and a cumulative receipt completing
the admitted requests. Existing unit coverage of queued versus merged states
is useful but is not this live end-to-end check.

## 2. Prepare the product configuration and operator rules

Put the tested opt-in configuration into a normally reviewed product PR and
preserve required-check provider identity, strict freshness, administrator
enforcement and squash policy. Do not enable update-all behavior. The active
coordinator and cohort must be named. Agents must stop independently rebasing
or enabling a second auto-merge mechanism on admitted PRs.

Conflict handling must name the current head, resolution owner and missing
admission label. Resolve/review, observe fresh validation, then explicitly
re-admit. Keep both initial and re-admission timestamps. An explicit hold must
remain distinguishable from ordinary queue waiting, and API failure must be
shown as unavailable/stale.

Before cutover, retain an exact protection/configuration snapshot and a rollback
that pauses new admissions, removes admission from open queued PRs, suspends
the production app if necessary, and keeps durable delivery requests and all
required checks. Account for an already merging candidate when inspecting the
result; stopping new admissions is not an atomic cancellation of a merge.

## 3. Run a named macOS cohort

After the product configuration and delivery procedure are reviewable, a
production-only access change and a specifically approved cohort are needed.
Do not treat the old open-PR backlog as blanket shipment authorization. Use
three to six genuinely ready PRs and record initial readiness, admission,
each candidate head/base, job start/end, canceled or invalidated candidates,
actual merge, publication and local verified activation separately.

Report observed median/max for a small burst and continue collecting before
claiming a stable p95. The provisional 20-minute p95 was a workstream target,
not a property proved by this fixture. Measure runner-minutes and the waiting
of later PRs, not just the first merge or hourly completion average.

## 4. Decide from the measured bottleneck

If serialization dominates, a serial coordinator is insufficient for the
ten-agent latency goal. Prepare concurrent cumulative candidate validation and
measure available macOS capacity, including the existing parallel Intel check
and release jobs. Queue-provider eligibility, repository ownership changes and
the production access grant remain separate decisions. The earlier native
queue/transfer research is in the parent workstream; do not repeat the migration
or claim this Linux fixture has validated it.

The faster local preview route remains independent of merge and publication.
Representative warm edit-to-preview timing and sustained delivery bursts remain
in product issue 519; the original hosted hang diagnosis remains in 515. This
queue pilot does not close either issue.
