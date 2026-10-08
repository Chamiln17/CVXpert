"""Tailoring in the Pipeline's review phase: only with a Job Description."""

import pytest
from fakes import TAILORING, FakeModel, review_citing

from cvxpert.errors import StepError
from cvxpert.pipeline import review_phase

JOB = "Backend Developer. Must have: Python, Docker, AWS."


@pytest.fixture
def txt_cv(tmp_path):
    path = tmp_path / "cv.txt"
    path.write_text("Jane Doe\nResponsible for the website.\n", encoding="utf-8")
    return path


def test_a_job_description_yields_a_tailoring_from_the_cv_and_the_job(
    txt_cv, use_model
):
    model = use_model(FakeModel(review_citing("G09"), tailoring=TAILORING))

    result = review_phase(txt_cv, job_description=JOB)

    assert result.tailoring.job_match_score == 64
    assert result.tailoring.gaps == ["Docker", "AWS"]
    assert result.tailoring.emphasis == [
        "Move the booking API work to the top of Experience"
    ]
    assert len(model.tailor_requests) == 1
    assert "Responsible for the website." in str(model.tailor_requests[0])
    assert JOB in str(model.tailor_requests[0])


def test_without_a_job_description_there_is_no_tailoring_and_no_g05_or_g06(
    txt_cv, use_model
):
    model = use_model(FakeModel(review_citing("G05", "G09", "G06")))

    result = review_phase(txt_cv)

    assert result.tailoring is None
    assert model.tailor_requests == []
    assert [f.guideline_id for f in result.review.findings] == ["G09"]
    assert JOB not in str(model.instructions[0])


def test_with_a_job_description_the_review_sees_it_and_keeps_g05_and_g06(
    txt_cv, use_model
):
    model = use_model(
        FakeModel(review_citing("G05", "G09", "G06"), tailoring=TAILORING)
    )

    result = review_phase(txt_cv, job_description=JOB)

    assert [f.guideline_id for f in result.review.findings] == ["G05", "G09", "G06"]
    assert JOB in model.instructions[0]


def test_a_tailoring_invalid_twice_is_a_step_error(txt_cv, use_model):
    model = use_model(
        FakeModel(review_citing("G09"), tailoring={**TAILORING, "job_match_score": 150})
    )

    with pytest.raises(StepError, match="The tailor Step failed after one retry"):
        review_phase(txt_cv, job_description=JOB)
    assert len(model.tailor_requests) == 2
