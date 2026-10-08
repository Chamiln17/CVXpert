"""The Pipeline's rewrite phase: kept Findings in, a guarded Rewrite out."""

import pytest
from fakes import PYTHON_GAP, TAILORING, FakeModel, review_citing, rewrite

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

    assert rewritten.markdown.startswith("# [Name]")
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


KUBERNETES = rewrite("# Jane Doe\n\n- Deployed the website on Kubernetes.")


def test_an_unverified_term_kept_after_the_retry_is_returned_with_the_rewrite(
    reviewed,
):
    result, model = reviewed(KUBERNETES)

    rewritten = rewrite_phase(result, kept_ids={"F1"})

    assert rewritten.unverified_terms == ["Kubernetes"]
    assert "Kubernetes" in rewritten.markdown
    assert len(model.rewrite_requests) == 2
    assert "Kubernetes" in str(model.rewrite_requests[1][-1])


def test_an_unverified_term_dropped_on_the_retry_leaves_none(reviewed):
    result, model = reviewed(
        KUBERNETES, rewrite("# Jane Doe\n\n- Deployed the website.")
    )

    rewritten = rewrite_phase(result, kept_ids={"F1"})

    assert rewritten.unverified_terms == []
    assert len(model.rewrite_requests) == 2


def test_an_invented_number_on_the_term_retry_is_still_a_fabrication_error(reviewed):
    result, model = reviewed(
        KUBERNETES, rewrite("# Jane Doe\n\n- Served 5,000 customers.")
    )

    with pytest.raises(FabricationError, match="5,000"):
        rewrite_phase(result, kept_ids={"F1"})
    assert len(model.rewrite_requests) == 2


def test_a_term_left_on_the_number_retry_is_returned_without_a_third_try(reviewed):
    result, model = reviewed(
        rewrite("# Jane Doe\n\n- Served 5,000 customers on Docker."), KUBERNETES
    )

    rewritten = rewrite_phase(result, kept_ids={"F1"})

    assert rewritten.unverified_terms == ["Kubernetes"]
    retry_prompt = str(model.rewrite_requests[1][-1])
    assert "5,000" in retry_prompt
    assert "Docker" in retry_prompt
    assert len(model.rewrite_requests) == 2


def test_the_rewrite_step_is_told_not_to_borrow_job_terms_or_raise_claims(reviewed):
    """Owner decision Q27(a): a Job Description term the CV lacks ("REST") and a
    raised claim ("worked on" to "developed") are forbidden in the instructions. The
    Unverified Term check flags "REST"; no check in code catches a lowercase claim
    upgrade."""
    result, model = reviewed(job_description="Backend Developer. Must have: REST APIs.")

    rewrite_phase(result, kept_ids={"F1"})

    instructions = model.rewrite_instructions[0]
    assert "Never use a term from the Job Description that the CV does not contain" in (
        instructions
    )
    assert "Never raise the level of a claim" in instructions
    assert '"worked on" must not become "developed"' in instructions


def test_a_term_left_after_a_schema_invalid_first_answer_is_returned(reviewed):
    result, model = reviewed({"text": "no markdown field"}, KUBERNETES)

    rewritten = rewrite_phase(result, kept_ids={"F1"})

    assert rewritten.unverified_terms == ["Kubernetes"]
    assert len(model.rewrite_requests) == 2


POSTGRES = rewrite("# Jane Doe\n\n- Built the website on PostgreSQL over 5 years.")


def test_a_confirmed_gap_reaches_the_rewrite_step_and_is_not_flagged(reviewed):
    result, model = reviewed(POSTGRES, job_description="Must have: PostgreSQL.")

    rewritten = rewrite_phase(
        result, kept_ids={"F1"}, confirmed_gaps=["PostgreSQL, 5 years"]
    )

    assert rewritten.unverified_terms == []
    assert rewritten.confirmed_gaps == ["PostgreSQL, 5 years"]
    assert len(model.rewrite_requests) == 1
    assert "PostgreSQL, 5 years" in str(model.rewrite_requests[0])
    assert (
        "Confirmed Gaps are facts the candidate supplied"
        in (model.rewrite_instructions[0])
    )


def test_an_unconfirmed_gap_is_still_flagged(reviewed):
    result, _ = reviewed(
        rewrite("# Jane Doe\n\n- Built the website on PostgreSQL."),
        job_description="Must have: PostgreSQL.",
    )

    rewritten = rewrite_phase(result, kept_ids={"F1"}, confirmed_gaps=["Docker"])

    assert rewritten.unverified_terms == ["PostgreSQL"]


def test_a_confirmed_label_allows_its_terms_and_numbers(reviewed):
    """Owner decision Q33(a): "Python" and "3" are in the label, not in the CV."""
    result, model = reviewed(
        rewrite("# Jane Doe\n\n- Built the website in Python over 3 years."),
        job_description="Must have: Python, 3+ years.",
    )
    label = result.tailoring.gaps[2].label

    rewritten = rewrite_phase(result, kept_ids={"F1"}, confirmed_gaps=[label])

    assert rewritten.unverified_terms == []
    assert rewritten.confirmed_gaps == ["Python, 3+ years"]
    assert len(model.rewrite_requests) == 1


def test_a_confirmed_gaps_detail_widens_neither_check(reviewed):
    """The detail reaches the model inside the Tailoring, but only the label joins
    the allowed text: the detail's "Kubernetes" is still an Unverified Term."""
    result, model = reviewed(
        rewrite("# Jane Doe\n\n- Ran the website in Python on Kubernetes."),
        job_description="Must have: Python, 3+ years.",
    )

    rewritten = rewrite_phase(
        result, kept_ids={"F1"}, confirmed_gaps=[result.tailoring.gaps[2].label]
    )

    assert PYTHON_GAP["detail"] in str(model.rewrite_requests[0])
    assert rewritten.unverified_terms == ["Kubernetes"]


def test_a_number_only_in_a_confirmed_gaps_detail_is_a_fabrication(reviewed):
    result, _ = reviewed(
        rewrite("# Jane Doe\n\n- Built 5 projects in Python."),
        job_description="Must have: Python, 3+ years.",
    )

    with pytest.raises(FabricationError, match=r"no Rewrite was produced: 5$"):
        rewrite_phase(
            result, kept_ids={"F1"}, confirmed_gaps=[result.tailoring.gaps[2].label]
        )
