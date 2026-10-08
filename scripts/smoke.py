"""Opt-in live smoke run: ``uv run python scripts/smoke.py`` from the repo root.

Makes paid OpenRouter requests. Before any model call it reads the key's credit
limit from OpenRouter and refuses unless the limit is set and at most $1. It runs
both phases (keeping every Finding) on examples/cv.txt with
examples/job-description.txt, writes examples/sample-report.md, and prints the
spend as the drop in the key's limit remaining from before to after. Not run by
pytest or CI.
"""

import json
import sys
import urllib.request
from pathlib import Path

import pydantic_ai

from cvxpert import pipeline
from cvxpert.config import Settings
from cvxpert.errors import one_line
from cvxpert.export import render_report

KEY_URL = "https://openrouter.ai/api/v1/key"
MAX_LIMIT_USD = 1.0
EXAMPLES = Path(__file__).parents[1] / "examples"
CV = EXAMPLES / "cv.txt"
JOB = EXAMPLES / "job-description.txt"
REPORT = EXAMPLES / "sample-report.md"


def fetch_key(api_key: str) -> dict:
    """GET the key endpoint: ``{"data": {"limit", "limit_remaining", "usage", ...}}``."""
    request = urllib.request.Request(
        KEY_URL, headers={"Authorization": f"Bearer {api_key}"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    pydantic_ai.BANNER_ENABLED = False
    api_key = Settings().openrouter_api_key.get_secret_value()
    if not api_key:
        return _fail("refusing to run: OPENROUTER_API_KEY is not set")
    try:
        before = fetch_key(api_key)["data"]
        limit, remaining_before = before["limit"], before["limit_remaining"]
    except Exception as e:
        return _fail(f"refusing to run: cannot read the key's limit: {one_line(e)}")
    if limit is None or float(limit) > MAX_LIMIT_USD:
        return _fail(
            f"refusing to run: the key's credit limit is {limit}; set one of at most $1"
        )

    try:
        result = pipeline.run(CV, JOB.read_text(encoding="utf-8"))
        REPORT.write_text(render_report(result), encoding="utf-8")
    except Exception as e:
        return _fail(f"run failed: {one_line(e)}")
    sys.stdout.write(f"Report written to {REPORT}\n")

    try:
        remaining_after = float(fetch_key(api_key)["data"]["limit_remaining"])
        spend = float(remaining_before) - remaining_after
    except Exception as e:
        return _fail(f"cannot read the spend after the run: {one_line(e)}")
    # ponytail: one read right after the run; if OpenRouter records spend late, it
    # reads low. Check the key's activity page then.
    sys.stdout.write(f"Spend: ${spend:.6f}\n")
    sys.stdout.write(f"Limit remaining: ${remaining_after:.6f}\n")
    return 0


def _fail(message: str) -> int:
    sys.stderr.write(f"smoke: {message}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
