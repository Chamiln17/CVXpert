"""The Pipeline's rewrite phase: kept Findings in, a guarded Rewrite out."""

import pytest
from fakes import TAILORING, FakeModel, review_citing, rewrite

from cvxpert.errors import FabricationError, StepError
from cvxpert.pipeline import review_phase, rewrite_phase

CV_TEXT = """\
Jane Doe
Software Developer, Brightfield Logistics, 2019-2021
- Responsible for the website, used by 1,200 customers.
- Cut page load time by 30%.
"""


@pytest.fixture
def reviewed(tmp_path, use_model):
    """Run the review phase on a small CV; return it with a way to set the Rewrites."""
    path = tmp_path / "cv.txt"
    path.write_text(CV_TEXT, encoding="utf-8")

    def run(*rewrites: dict, job_description: str | None = None):
        model = use_model(
            FakeModel(
                review_citing("G09", "G01"),
                tailoring=TAILORING,
                **({"rewrites": rewrites} if rewrites else {}),
            )
        )
        return review_phase(path, job_description), model

    return run


def test_only_the_kept_findings_reach_the_rewrite_step(reviewed):
    result, model = reviewed()

    rewritten = rewrite_phase(result, kept_ids={"F2"})

    assert rewritten.markdown.startswith("# Jane Doe")
    request = str(model.rewrite_requests[0])
    assert "Breaks G01." in request
    assert "Breaks G09." not in request
    assert "Responsible for the website" in request


def test_the_tailoring_reaches_the_rewrite_step_when_given(reviewed):
    result, model = reviewed(job_description="Backend Developer. Must have: Python.")

    rewrite_phase(result, kept_ids={"F1"})

    assert "Move the booking API work to the top of Experience" in str(
        model.rewrite_requests[0]
    )


def test_an_invented_percentage_is_retried_and_a_clean_retry_is_returned(reviewed):
    result, model = reviewed(
        rewrite("# Jane Doe\n\n- Cut page load time by 40%."),
        rewrite("# Jane Doe\n\n- Cut page load time by 30%, raising [result]."),
    )

    rewritten = rewrite_phase(result, kept_ids={"F1", "F2"})

    assert "by 30%" in rewritten.markdown
    assert rewritten.placeholders == ["[result]"]
    assert len(model.rewrite_requests) == 2
    assert "40%" in str(model.rewrite_requests[1][-1])


def test_a_number_invented_twice_is_a_fabrication_error(reviewed):
    result, model = reviewed(rewrite("# Jane Doe\n\n- Served 5,000 customers in 2023."))

    with pytest.raises(FabricationError, match=r"5,000, 2023"):
        rewrite_phase(result, kept_ids={"F1"})
    assert len(model.rewrite_requests) == 2


def test_a_rewrite_invalid_twice_is_a_step_error_not_a_fabrication_error(reviewed):
    result, model = reviewed({"text": "no markdown field"})

    with pytest.raises(
        StepError, match="The rewrite Step failed after one retry"
    ) as info:
        rewrite_phase(result, kept_ids={"F1"})
    assert not isinstance(info.value, FabricationError)
    assert len(model.rewrite_requests) == 2


def test_placeholders_pass_the_guard_and_are_listed(reviewed):
    result, model = reviewed(
        rewrite(
            "# Jane Doe\n\n- Cut load time by [X%] for [team size] users, 2019-2021."
        )
    )

    rewritten = rewrite_phase(result, kept_ids={"F1"})

    assert rewritten.placeholders == ["[X%]", "[team size]"]
    assert len(model.rewrite_requests) == 1


def test_known_v1_gap_an_invented_tool_passes_the_guard(reviewed):
    """Documents the accepted v1 gap: the guard checks numbers only, so a tool the CV
    never names ("Kubernetes") gets through. A proper-noun guard is v2."""
    result, model = reviewed(
        rewrite("# Jane Doe\n\n- Deployed the website on Kubernetes.")
    )

    rewritten = rewrite_phase(result, kept_ids={"F1"})

    assert "Kubernetes" in rewritten.markdown
    assert len(model.rewrite_requests) == 1


def test_the_rewrite_step_is_told_not_to_borrow_job_terms_or_raise_claims(reviewed):
    """Owner decision Q27(a): a Job Description term the CV lacks ("REST") and a
    raised claim ("worked on" to "developed") are forbidden in the instructions; no
    check in code catches them in v1."""
    result, model = reviewed(job_description="Backend Developer. Must have: REST APIs.")

    rewrite_phase(result, kept_ids={"F1"})

    instructions = model.rewrite_instructions[0]
    assert "Never use a term from the Job Description that the CV does not contain" in (
        instructions
    )
    assert "Never raise the level of a claim" in instructions
    assert '"worked on" must not become "developed"' in instructions
