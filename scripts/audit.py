#!/usr/bin/env python3
"""Validate the assigned queue candidate, with a controllable failure fixture."""
import json
from pathlib import Path
import subprocess
import sys
import time

expected = sys.argv[1]
assert len(expected) == 40 and all(c in "0123456789abcdef" for c in expected)
assert subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == expected
assert not subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
for path in sorted(Path("cases").glob("*.json")):
    case = json.loads(path.read_text())
    assert case.get("pass") is True, f"deliberately failing pilot case: {path}"
time.sleep(20)
assert subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == expected
print(f"Source audit passed for {expected}")
