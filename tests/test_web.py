"""The Streamlit page, driven with AppTest, and the ``cvxpert web`` command."""

import sys
from pathlib import Path

from fakes import FakeModel, review_citing, rewrite
from streamlit.testing.v1 import AppTest

import cvxpert
from cvxpert import cli

EXAMPLE_CV = Path(__file__).parents[1] / "examples" / "cv.txt"
PAGE = Path(cvxpert.__file__).with_name("web.py")


def _page() -> AppTest:
    return AppTest.from_file(str(PAGE), default_timeout=30).run()


def _upload_and_review(at: AppTest) -> None:
    at.file_uploader[0].upload("cv.txt", EXAMPLE_CV.read_bytes(), "text/plain")
    at.run()
    at.button(key="run-review").click().run()


def test_an_unticked_finding_does_not_reach_the_rewrite(use_model):
    model = use_model(
        FakeModel(
            review_citing("G02", "G09"),
            rewrites=(rewrite("# Alex Morgan\n\n- Built [what], cutting [X%]."),),
        )
    )
    at = _page()

    _upload_and_review(at)
    assert not at.exception
    assert at.metric[0].label == "Overall Score"
    assert at.metric[0].value == "58/100"
    labels = [c.label for c in at.checkbox]
    assert any(
        "G02 Quantify only with numbers the candidate supplied" in x for x in labels
    )
    assert all(c.value for c in at.checkbox)
    rules = "".join(m.value for e in at.expander for m in e.markdown)
    assert "If the CV has no number, the Rewrite inserts a placeholder" in rules

    at.checkbox(key="keep-F1").uncheck().run()
    at.button(key="run-rewrite").click().run()

    assert not at.exception
    request = str(model.rewrite_requests[0])
    assert "Breaks G09." in request
    assert "Breaks G02." not in request
    shown = "".join(m.value for m in at.markdown)
    assert "Built [what], cutting [X%]." in shown
    assert "[X%]" in shown
    assert at.download_button[0].label == "Download Markdown"
    assert at.download_button[1].label == "Download PDF"
    assert at.session_state["rewrite"].markdown.startswith("# Alex Morgan")


def test_a_pipeline_error_shows_as_one_readable_message():
    at = _page()  # no fake model and no key: the review phase fails

    _upload_and_review(at)

    assert not at.exception
    assert len(at.error) == 1
    assert "OPENROUTER_API_KEY is not set" in at.error[0].value


def test_web_command_runs_streamlit_on_the_page(monkeypatch):
    calls = []
    monkeypatch.setattr(cli.subprocess, "call", lambda cmd: calls.append(cmd) or 0)

    assert cli.main(["web"]) == 0

    assert calls == [[sys.executable, "-m", "streamlit", "run", str(PAGE)]]


def test_the_page_says_where_the_cv_is_sent_before_upload():
    at = _page()

    assert not at.exception
    assert any("OpenRouter" in i.value for i in at.info)
