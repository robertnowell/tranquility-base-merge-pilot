# Tranquility Base merge queue pilot

An isolated public fixture repository for [workstream #489](https://github.com/robertnowell/tranquility-base/issues/489), specifically [pilot #493](https://github.com/robertnowell/tranquility-base/issues/493).

This repository contains no product source or deployment credentials. Its short
Linux audit tests queue coordination and protection behavior. Its timings are
not evidence about Tranquility Base's macOS CI throughput.

The intended pilot uses Kodiak scoped to this repository, strict Source audit
from GitHub Actions, squash merges, FIFO service, and explicit `merge-queue`
admission. Updating every waiting branch is disabled. No ordinary agent rebases
or separately arms auto-merge on an admitted PR.

Before live adoption, exercise a burst of three ready PRs, an edited queued PR,
a failing required check, and a real merge conflict. Preserve raw admission,
workflow/job, branch-update and merge timestamps. Then measure a small live
macOS queue for admission-to-merge time and discarded runner work. The proposed
20-minute p95 waiting target belongs to that live pilot, not this fixture.

Removing the admission label pauses a PR. Uninstalling the app leaves GitHub's
required-check enforcement intact. No branch-protection bypass is part of the
pilot.

Configuration reference: https://kodiakhq.com/docs/config-reference
Permissions: https://kodiakhq.com/docs/permissions
