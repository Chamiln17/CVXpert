"""The opt-in live smoke script, with a faked key endpoint and a fake model."""

import importlib.util
import urllib.error
from pathlib import Path

import pytest
from fakes import TAILORING, FakeModel, review_citing

SCRIPT = Path(__file__).parents[1] / "scripts" / "smoke.py"


@pytest.fixture
def smoke(monkeypatch, tmp_path):
    """The script as a module, its report redirected into tmp_path."""
    spec = importlib.util.spec_from_file_location("smoke", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "REPORT", tmp_path / "sample-report.md")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test-key")
    return module


def key_endpoint(monkeypatch, smoke, *responses):
    """Serve the given key-endpoint payloads (or raise exceptions) in order."""
    queue = list(responses)

    def fetch(api_key):
        assert api_key == "sk-or-test-key"
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    monkeypatch.setattr(smoke, "fetch_key", fetch)


def key(limit, usage, remaining=None):
    return {"data": {"limit": limit, "usage": usage, "limit_remaining": remaining}}


@pytest.mark.parametrize(
    "response",
    [
        key(None, 0.0),
        key(1.5, 0.0, 1.5),
        urllib.error.URLError("connection refused"),
    ],
    ids=["limit unset", "limit above $1", "endpoint error"],
)
def test_refuses_without_a_model_call(monkeypatch, smoke, use_model, capsys, response):
    fake = use_model(FakeModel(review_citing("G09"), tailoring=TAILORING))
    key_endpoint(monkeypatch, smoke, response)

    assert smoke.main() != 0

    err = capsys.readouterr().err
    assert len(err.strip().splitlines()) == 1
    assert "refus" in err.lower()
    assert "sk-or-test-key" not in err
    assert fake.review_requests == [] and fake.tailor_requests == []
    assert fake.rewrite_requests == []
    assert not smoke.REPORT.exists()


def test_refuses_when_no_api_key_is_set(monkeypatch, smoke, use_model, capsys):
    monkeypatch.delenv("OPENROUTER_API_KEY")
    fake = use_model(FakeModel(review_citing("G09"), tailoring=TAILORING))
    key_endpoint(monkeypatch, smoke)  # any fetch would fail: the queue is empty

    assert smoke.main() != 0

    assert "OPENROUTER_API_KEY" in capsys.readouterr().err
    assert fake.review_requests == []


def test_runs_both_phases_and_prints_the_measured_spend(
    monkeypatch, smoke, use_model, capsys
):
    fake = use_model(FakeModel(review_citing("G02", "G09"), tailoring=TAILORING))
    # The spend is the drop in `limit_remaining`; `usage` stays put to show it is unused.
    key_endpoint(monkeypatch, smoke, key(1.0, 0.25, 0.75), key(1.0, 0.25, 0.7366))

    assert smoke.main() == 0

    report = smoke.REPORT.read_text(encoding="utf-8")
    assert "Overall Score: 58/100" in report
    assert "Built [what] for the website." in report
    assert len(fake.review_requests) == 1
    assert len(fake.tailor_requests) == 1
    assert len(fake.rewrite_requests) == 1
    out = capsys.readouterr().out
    assert "Spend: $0.013400" in out
    assert "Limit remaining: $0.736600" in out
    assert "sk-or-test-key" not in out
