# Protected queue acceptance

The baseline is frozen at a0fe882 while PRs 1, 2 and 3 remain ready and
unadmitted. Do not merge these measurement files into main before the baseline
burst. They can run from this branch without changing the candidate base.

The collector is read-only and hardcodes this isolated repository. Capture a
baseline and repeat snapshots every 10 seconds during each case:

```
python3 scripts/measure.py snapshot --evidence /absolute/path/burst.jsonl --prs 1 2 3
python3 scripts/measure.py report --evidence /absolute/path/burst.jsonl
```

Only after the actual Kodiak installation is confirmed as scoped to this
fixture, apply `merge-queue` to 1, 2 and 3 in one short burst. The fixture's
strict required Source audit and enforced administrators remain unchanged.
Observe bot head updates and actual merges; do not rebase admitted branches.

Then create fresh cases from the resulting main so the baseline is preserved:

1. **Edited admitted PR:** add a passing `cases/edited.json`, admit it, then
   commit another edit while its candidate check is running. Require the new
   head to pass; a stale green check must not authorize the edited source.
2. **Failed required check:** admit a fresh PR with `cases/failure.json`
   containing `{"pass": false}`. It must stay unmerged. Change the value to
   true and require fresh validation before a merge. A tolerated/neutral check
   must not substitute for Source audit success.
3. **Actual text conflict:** create two branches from the same main changing
   the same existing `cases/base.json` value differently. Keep `pass: true`
   and change a new `variant` field. Admit both. After one merges, the second
   must stop with a real conflict; resolve it explicitly, then require fresh CI.
4. **Explicit hold:** apply `queue-hold` to a fresh admitted passing PR. It
   must remain unmerged until that label is removed.

Save each case's PR numbers, raw snapshots, head identities, workflow attempts,
job start/completion, actual merge SHA and observed blocker. Fail the pilot on
an unauthorized merge, a missing required check, a stale-head merge, an ignored
hold or a bot/agent update race. Do not infer these properties from label presence.

This fixture's 20-second Linux audit proves coordination only. Report median
and maximum for the observed burst, not a reliable p95 from three samples.
Production adoption requires a separate macOS burst measuring candidate wait,
execution, invalidated candidates and publication/activation separately.
If serialization dominates, evaluate concurrent cumulative candidates with
verified macOS capacity; successful serial operation alone is not acceptance
of the ten-agent latency objective. No production settings or ownership change
is authorized by running this fixture.
