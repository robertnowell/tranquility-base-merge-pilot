#!/usr/bin/env python3
"""Read-only evidence collector for the isolated merge pilot. Never changes labels or branches."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import subprocess

REPO = "robertnowell/tranquility-base-merge-pilot"


def gh(*args):
    return json.loads(subprocess.check_output(["gh", *args], text=True, timeout=45))


def seconds(start, end):
    return (datetime.fromisoformat(end.replace("Z", "+00:00")) -
            datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds()


def collect(prs):
    result = {"checked_at": datetime.now(timezone.utc).isoformat(), "repo": REPO, "prs": [], "runs": []}
    for number in prs:
        pr = gh("pr", "view", str(number), "--repo", REPO, "--json",
                "number,state,headRefOid,headRefName,mergeCommit,mergedAt,mergeStateStatus,labels,statusCheckRollup")
        events = gh("api", f"repos/{REPO}/issues/{number}/timeline?per_page=100")
        pr["timeline"] = [{key: e.get(key) for key in ("event", "created_at", "commit_id", "label", "actor")}
                          for e in events if e.get("event") in ("labeled", "unlabeled", "committed", "merged")]
        pr["timeline_truncated"] = len(events) >= 100
        result["prs"].append(pr)
    runs = gh("api", f"repos/{REPO}/actions/runs?per_page=100")
    branches = {p["headRefName"] for p in result["prs"]}
    for run in runs["workflow_runs"]:
        if run["head_branch"] not in branches: continue
        jobs = gh("api", f"repos/{REPO}/actions/runs/{run['id']}/attempts/{run['run_attempt']}/jobs?per_page=100")
        result["runs"].append({**{k: run.get(k) for k in ("id", "run_attempt", "head_sha", "head_branch",
                                     "created_at", "run_started_at", "updated_at", "status", "conclusion")},
                               "jobs": [{k: j.get(k) for k in ("id", "name", "status", "conclusion", "started_at", "completed_at")}
                                        for j in jobs["jobs"]]})
    result["runs_truncated"] = runs["total_count"] > 100
    return result


def report(samples):
    latest = samples[-1]
    rows = []
    for pr in latest["prs"]:
        admitted = [e["created_at"] for e in pr["timeline"]
                    if e["event"] == "labeled" and (e.get("label") or {}).get("name") == "merge-queue"]
        changed_heads = list(dict.fromkeys(p["headRefOid"] for sample in samples for p in sample["prs"]
                                          if p["number"] == pr["number"]))
        rows.append({"pr": pr["number"], "state": pr["state"], "queue_request_at": admitted[-1] if admitted else None,
                     "merged_at": pr["mergedAt"], "observed_heads": changed_heads,
                     "request_to_merge_seconds": seconds(admitted[-1], pr["mergedAt"])
                     if admitted and pr["mergedAt"] else None})
    durations = [r["request_to_merge_seconds"] for r in rows if r["request_to_merge_seconds"] is not None]
    jobs = []
    for run in latest["runs"]:
        for job in run["jobs"]:
            jobs.append({"run": run["id"], "attempt": run["run_attempt"], "sha": run["head_sha"],
                         "name": job["name"], "conclusion": job["conclusion"],
                         "run_created_to_job_start_seconds": seconds(run["created_at"], job["started_at"])
                         if job["started_at"] else None,
                         "execution_seconds": seconds(job["started_at"], job["completed_at"])
                         if job["started_at"] and job["completed_at"] else None})
    return {"prs": rows, "jobs": jobs, "merged_samples": len(durations),
            "request_to_merge_median_seconds": statistics.median(durations) if durations else None,
            "request_to_merge_max_seconds": max(durations) if durations else None,
            "limits": ["Label time is an opt-in request, not evidence of bot acceptance.",
                       "Run creation to job start includes scheduling and setup; it is not a pure runner-capacity measure.",
                       "This short Linux fixture measures coordination, not macOS throughput or a stable p95.",
                       "Polling can miss intermediate heads; raw run identities and timelines remain evidence."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["snapshot", "report"])
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--prs", nargs="+", type=int, default=[1, 2, 3])
    args = parser.parse_args()
    if args.operation == "snapshot":
        sample = collect(args.prs)
        args.evidence.parent.mkdir(parents=True, exist_ok=True)
        with args.evidence.open("a") as out: out.write(json.dumps(sample) + "\n")
        print(json.dumps({"checked_at": sample["checked_at"], "prs": len(sample["prs"]), "runs": len(sample["runs"])}))
    else:
        samples = [json.loads(line) for line in args.evidence.read_text().splitlines() if line.strip()]
        print(json.dumps(report(samples), indent=2))
