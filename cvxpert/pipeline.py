"""The Pipeline: parse -> review -> tailor in the review phase; rewrite in the
rewrite phase, so a caller can drop Findings in between."""

from collections.abc import Collection, Sequence
from pathlib import Path

from pydantic import BaseModel

from cvxpert import config, steps
from cvxpert.parsing import ParsedCV, parse_cv


class ReviewPhaseResult(BaseModel):
    cv: ParsedCV
    review: steps.Review
    tailoring: steps.Tailoring | None = None


class PipelineResult(ReviewPhaseResult):
    rewrite: steps.Rewrite


def review_phase(
    cv_path: Path, job_description: str | None = None
) -> ReviewPhaseResult:
    """Parse the CV, review it, and tailor it when a Job Description is given.

    The API key is checked before any Step runs.
    """
    model = config.get_model()
    cv = parse_cv(Path(cv_path))
    review = steps.review(cv, model, job_description)
    tailoring = steps.tailor(cv, job_description, model) if job_description else None
    return ReviewPhaseResult(cv=cv, review=review, tailoring=tailoring)


def rewrite_phase(
    result: ReviewPhaseResult,
    kept_ids: Collection[str],
    confirmed_gaps: Sequence[str] = (),
) -> steps.Rewrite:
    """Rewrite the CV applying only the kept Findings, plus the Tailoring if any.

    Confirmed Gaps are gap labels the candidate states are true; the Rewrite
    may use them.

    Raises FabricationError rather than return a Rewrite with an invented number;
    Unverified Terms left after the retry come back in ``unverified_terms``.
    """
    kept = [f for f in result.review.findings if f.id in kept_ids]
    return steps.rewrite(
        result.cv, kept, result.tailoring, config.get_model(), confirmed_gaps
    )


def run(
    cv_path: Path,
    job_description: str | None = None,
    confirmed_gaps: Sequence[str] = (),
) -> PipelineResult:
    """Run both phases keeping every Finding; the CLI calls this."""
    result = review_phase(cv_path, job_description)
    rewrite = rewrite_phase(
        result, {f.id for f in result.review.findings}, confirmed_gaps
    )
    return PipelineResult(**dict(result), rewrite=rewrite)
