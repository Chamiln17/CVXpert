"""The CLI entry point, called in-process with an argument list."""

import io
import shutil
from pathlib import Path

from fakes import TAILORING, FakeModel, review_citing, rewrite
from pypdf import PdfReader

from cvxpert.cli import main

EXAMPLE_CV = Path(__file__).parents[1] / "examples" / "cv.txt"
EXAMPLE_JOB = EXAMPLE_CV.with_name("job-description.txt")


def test_review_of_the_example_cv_writes_a_markdown_report(tmp_path, use_model):
    use_model(FakeModel(review_citing("G02", "G09")))
    out = tmp_path / "report.md"

    assert main(["review", str(EXAMPLE_CV), "--out", str(out)]) == 0

    report = out.read_text(encoding="utf-8")
    assert "Overall Score: 58/100" in report
    assert "the model's estimate" in report
    assert "Duties instead of results; no numbers anywhere." in report
    assert "Experience" in report
    assert "Skills" in report
    assert "G02 Quantify only with numbers the candidate supplied" in report
    assert "G09 Remove duty phrases" in report
    assert "Built [what] for the website, raising [result]." in report


def test_the_report_goes_next_to_the_cv_by_default(tmp_path, use_model):
    cv = tmp_path / "cv.txt"
    shutil.copy(EXAMPLE_CV, cv)
    use_model(FakeModel(review_citing("G09")))

    assert main(["review", str(cv)]) == 0

    assert (tmp_path / "cv.cvxpert.md").is_file()


def test_format_pdf_writes_the_report_as_a_pdf_next_to_the_cv(tmp_path, use_model):
    cv = tmp_path / "cv.txt"
    shutil.copy(EXAMPLE_CV, cv)
    use_model(FakeModel(review_citing("G09")))

    assert main(["review", str(cv), "--format", "pdf"]) == 0

    data = (tmp_path / "cv.cvxpert.pdf").read_bytes()
    assert data.startswith(b"%PDF-")
    text = "\n".join(p.extract_text() for p in PdfReader(io.BytesIO(data)).pages)
    assert "Duties instead of results; no numbers anywhere." in text
    assert "Built [what] for the website, raising [result]." in text
    assert not (tmp_path / "cv.cvxpert.md").exists()


def test_a_missing_api_key_exits_non_zero_with_one_line(tmp_path, capsys):
    out = tmp_path / "report.md"

    assert main(["review", str(EXAMPLE_CV), "--out", str(out)]) != 0

    err = capsys.readouterr().err
    assert err.count("\n") == 1
    assert "OPENROUTER_API_KEY is not set" in err
    assert not out.exists()


def test_a_failed_review_step_exits_non_zero_with_one_line(tmp_path, capsys, use_model):
    use_model(FakeModel(review_citing("G99")))

    assert main(["review", str(EXAMPLE_CV), "--out", str(tmp_path / "r.md")]) != 0

    err = capsys.readouterr().err
    assert err.count("\n") == 1
    assert "G99" in err


def test_with_a_job_description_the_report_holds_the_tailoring(tmp_path, use_model):
    model = use_model(FakeModel(review_citing("G05", "G09"), tailoring=TAILORING))
    out = tmp_path / "report.md"

    assert (
        main(["review", str(EXAMPLE_CV), "--job", str(EXAMPLE_JOB), "--out", str(out)])
        == 0
    )

    report = out.read_text(encoding="utf-8")
    assert "## Tailoring" in report
    assert "Job Match Score: 64/100" in report
    assert "Strong Python fit; cloud and Docker are not shown." in report
    assert "Python web services" in report
    assert "- Docker" in report
    assert "Move the booking API work to the top of Experience" in report
    assert "G05 Tailor by selecting and ordering" in report
    assert "Harbourline Freight" in str(model.tailor_requests[0])


def test_without_a_job_description_the_report_has_no_tailoring_or_g05_g06(
    tmp_path, use_model
):
    model = use_model(FakeModel(review_citing("G05", "G06", "G09")))
    out = tmp_path / "report.md"

    assert main(["review", str(EXAMPLE_CV), "--out", str(out)]) == 0

    report = out.read_text(encoding="utf-8")
    assert "Tailoring" not in report
    assert "Job Match Score" not in report
    assert "G05" not in report
    assert "G06" not in report
    assert "G09 Remove duty phrases" in report
    assert model.tailor_requests == []


def test_the_report_ends_with_the_rewrite_and_its_placeholders(tmp_path, use_model):
    model = use_model(
        FakeModel(
            review_citing("G05", "G09"),
            tailoring=TAILORING,
            rewrites=(
                rewrite(
                    "# Alex Morgan\n\n1. Built [what] in March 2021, cutting [X%]."
                ),
            ),
        )
    )
    out = tmp_path / "report.md"

    assert (
        main(["review", str(EXAMPLE_CV), "--job", str(EXAMPLE_JOB), "--out", str(out)])
        == 0
    )

    report = out.read_text(encoding="utf-8")
    assert (
        report.index("## Review")
        < report.index("## Tailoring")
        < report.index("## Rewrite")
    )
    assert "1. Built [what] in March 2021, cutting [X%]." in report
    assert "- [what]" in report
    assert "- [X%]" in report
    request = str(model.rewrite_requests[0])
    assert "Breaks G05." in request
    assert "Breaks G09." in request


def test_a_rewrite_inventing_a_number_twice_exits_non_zero_with_one_line(
    tmp_path, capsys, use_model
):
    use_model(FakeModel(review_citing("G02"), rewrites=(rewrite("Cut costs by 40%."),)))
    out = tmp_path / "report.md"

    assert main(["review", str(EXAMPLE_CV), "--out", str(out)]) != 0

    err = capsys.readouterr().err
    assert err.count("\n") == 1
    assert "40%" in err
    assert not out.exists()


def test_a_missing_job_description_file_exits_non_zero_with_one_line(
    tmp_path, capsys, use_model
):
    model = use_model(FakeModel(review_citing("G09"), tailoring=TAILORING))
    out = tmp_path / "report.md"
    job = tmp_path / "missing-job.txt"

    assert main(["review", str(EXAMPLE_CV), "--job", str(job), "--out", str(out)]) != 0

    err = capsys.readouterr().err
    assert err.count("\n") == 1
    assert "Job Description" in err
    assert "missing-job.txt" in err
    assert not out.exists()
    assert model.review_requests == []


def test_a_failed_tailor_step_exits_non_zero_with_one_line(tmp_path, capsys, use_model):
    use_model(FakeModel(review_citing("G09"), tailoring={"job_match_score": 150}))
    out = tmp_path / "report.md"

    assert (
        main(["review", str(EXAMPLE_CV), "--job", str(EXAMPLE_JOB), "--out", str(out)])
        != 0
    )

    err = capsys.readouterr().err
    assert err.count("\n") == 1
    assert "tailor Step failed" in err
    assert not out.exists()


def test_multi_line_findings_and_tailoring_items_stay_one_bullet_each(
    tmp_path, use_model
):
    review = review_citing("G09")
    review["findings"][0]["problem"] = "Duty phrase.\nNo outcome."
    tailoring = {
        **TAILORING,
        "gaps": [{"label": "Docker", "detail": "Asked for\nin production."}],
    }
    use_model(FakeModel(review, tailoring=tailoring))
    out = tmp_path / "report.md"

    assert (
        main(["review", str(EXAMPLE_CV), "--job", str(EXAMPLE_JOB), "--out", str(out)])
        == 0
    )

    report = out.read_text(encoding="utf-8")
    assert "- Problem: Duty phrase. No outcome.\n" in report
    assert "- Docker: Asked for in production.\n" in report


def test_the_report_shows_each_cited_guidelines_rule_and_sources(tmp_path, use_model):
    use_model(FakeModel(review_citing("G02", "G09")))
    out = tmp_path / "report.md"

    assert main(["review", str(EXAMPLE_CV), "--out", str(out)]) == 0

    cited = out.read_text(encoding="utf-8").split("### Guidelines cited")[1]
    assert "If the CV has no number, the Rewrite inserts a placeholder" in cited
    assert "MIT-PDF" in cited
    assert "Rule: Recommend removing" not in cited  # G07, not cited


def test_unverified_terms_left_after_the_retry_are_listed_in_the_report(
    tmp_path, use_model
):
    use_model(
        FakeModel(
            review_citing("G09"),
            rewrites=(rewrite("# Alex Morgan\n\n- Deployed the API on Kubernetes."),),
        )
    )
    out = tmp_path / "report.md"

    assert main(["review", str(EXAMPLE_CV), "--out", str(out)]) == 0

    report = out.read_text(encoding="utf-8")
    assert "### Check these terms" in report
    assert "- Kubernetes" in report
    assert report.index("## Rewrite") < report.index("### Check these terms")


def test_a_report_without_unverified_terms_has_no_check_these_terms_list(
    tmp_path, use_model
):
    use_model(FakeModel(review_citing("G09")))
    out = tmp_path / "report.md"

    assert main(["review", str(EXAMPLE_CV), "--out", str(out)]) == 0

    assert "Check these terms" not in out.read_text(encoding="utf-8")


def test_confirmed_gaps_reach_the_rewrite_and_are_listed_in_the_report(
    tmp_path, use_model
):
    model = use_model(
        FakeModel(
            review_citing("G09"),
            tailoring=TAILORING,
            rewrites=(
                rewrite("# Alex Morgan\n\n- Moved the API to PostgreSQL with CI/CD."),
            ),
        )
    )
    out = tmp_path / "report.md"
    args = ["review", str(EXAMPLE_CV), "--job", str(EXAMPLE_JOB), "--out", str(out)]

    assert main([*args, "--confirm", "PostgreSQL", "--confirm", "CI/CD"]) == 0

    report = out.read_text(encoding="utf-8")
    rewrite_section = report.split("## Rewrite")[1]
    assert "### Confirmed Gaps" in rewrite_section
    assert "- PostgreSQL\n- CI/CD\n" in rewrite_section
    assert "Check these terms" not in report
    assert "- PostgreSQL" in str(model.rewrite_requests[0])


def test_confirm_without_a_job_description_exits_non_zero_with_one_line(
    tmp_path, capsys, use_model
):
    model = use_model(FakeModel(review_citing("G09")))
    out = tmp_path / "report.md"

    assert (
        main(["review", str(EXAMPLE_CV), "--confirm", "Docker", "--out", str(out)]) != 0
    )

    err = capsys.readouterr().err
    assert err.count("\n") == 1
    assert "--confirm" in err
    assert not out.exists()
    assert model.review_requests == []
