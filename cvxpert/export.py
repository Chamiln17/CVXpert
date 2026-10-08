"""Export: render the Pipeline's result as one Markdown report, and Markdown as PDF."""

from pathlib import Path

import markdown
from fpdf import FPDF, FontFace, TextStyle

from cvxpert.guidelines import load_guidelines
from cvxpert.pipeline import PipelineResult
from cvxpert.steps import SEVERITIES, Finding, Gap, Rewrite, Tailoring

ESTIMATE = "the model's estimate, not a measurement"
PRIVACY_NOTICE = (
    "Your CV text (and the Job Description, if given) is sent to OpenRouter and "
    "the chosen model's provider, using your own OpenRouter API key."
)
UNVERIFIED_TERMS_NOTE = (
    "The Rewrite uses these names or terms, which your CV does not contain. Keep "
    "one only if it is true of you."
)
CONFIRMED_GAPS_NOTE = "You confirmed these gaps, so the Rewrite may use them."
# Noto Sans, subset to Latin, punctuation and currency; OFL-1.1, see fonts/OFL.txt.
# fpdf2's core fonts are Latin-1 only, and no installed dependency ships a TTF.
_FONTS = Path(__file__).with_name("fonts")
_FONT = "NotoSans"


def markdown_to_pdf(text: str) -> bytes:
    """Markdown to HTML with ``markdown``, then HTML to PDF with fpdf2."""
    pdf = FPDF()
    # ponytail: no italic files; italics render upright in the Regular face
    for style, file in (
        ("", "Regular"),
        ("I", "Regular"),
        ("B", "Bold"),
        ("BI", "Bold"),
    ):
        pdf.add_font(_FONT, style, _FONTS / f"NotoSans-{file}.ttf")
    pdf.add_page()
    pdf.write_html(
        markdown.markdown(text),
        font_family=_FONT,
        tag_styles={  # the defaults use Courier, a Latin-1 core font
            "code": FontFace(family=_FONT),
            "pre": TextStyle(font_family=_FONT),
        },
    )
    return bytes(pdf.output())


def finding_heading(finding: Finding) -> str:
    """One line naming the Finding, its severity and the Guideline it cites."""
    guideline = load_guidelines()[finding.guideline_id]
    uncertain = " (uncertain)" if finding.uncertain else ""
    return f"{finding.id} [{finding.severity}]{uncertain}: {guideline.id} {guideline.title}"


def guideline_text(guideline_id: str) -> str:
    """A Guideline's title, full Rule and sources, on one line."""
    g = load_guidelines()[guideline_id]
    return f"{g.id} {g.title}. Rule: {g.rule} Sources: {'; '.join(g.sources)}"


def gap_text(gap: Gap) -> str:
    """A Tailoring gap as "label: detail"."""
    return f"{gap.label}: {gap.detail}"


def rewrite_lists(rewrite: Rewrite) -> list[tuple[str, str | None, list[str]]]:
    """The lists shown above the rewritten CV, as (heading, note, items): the
    Placeholders always, the Confirmed Gaps and Unverified Terms when there are any."""
    lists: list[tuple[str, str | None, list[str]]] = [
        ("Placeholders to fill in", None, rewrite.placeholders)
    ]
    if rewrite.confirmed_gaps:
        lists.append(("Confirmed Gaps", CONFIRMED_GAPS_NOTE, rewrite.confirmed_gaps))
    if rewrite.unverified_terms:
        lists.append(
            ("Check these terms", UNVERIFIED_TERMS_NOTE, rewrite.unverified_terms)
        )
    return lists


def _bullet(text: str) -> str:
    """A Markdown list item; newlines in the text would split it, so they are flattened."""
    return f"- {' '.join(text.split())}"


def render_report(result: PipelineResult) -> str:
    review = result.review
    lines = [
        f"# CVXpert report: {result.cv.metadata['file_name']}",
        "",
        "## Review",
        "",
        f"**Overall Score: {review.overall_score}/100** ({ESTIMATE})",
        "",
        review.summary,
        "",
        "### Sections",
        "",
        *(_bullet(section.title) for section in review.sections),
        "",
        "### Findings",
        "",
    ]
    if not review.findings:
        lines += ["No Findings.", ""]
    for finding in sorted(review.findings, key=lambda f: SEVERITIES.index(f.severity)):
        lines += [
            f"#### {finding_heading(finding)}",
            "",
            _bullet(f"Section: {finding.section}"),
            _bullet(f"Text: {finding.affected_text}"),
            _bullet(f"Problem: {finding.problem}"),
            _bullet(f"Proposed change: {finding.proposed_change}"),
            "",
        ]
    cited = sorted({f.guideline_id for f in review.findings})
    if cited:
        lines += ["### Guidelines cited", ""]
        lines += [_bullet(guideline_text(gid)) for gid in cited]
        lines.append("")
    if result.tailoring:
        lines += _tailoring_lines(result.tailoring)
    lines += ["## Rewrite", ""]
    for heading, note, items in rewrite_lists(result.rewrite):
        lines += [
            f"### {heading}",
            "",
            *([note, ""] if note else []),
            *([_bullet(item) for item in items] or ["None."]),
            "",
        ]
    lines += [
        "### Rewritten CV",
        "",
        result.rewrite.markdown,
        "",
    ]
    return "\n".join(lines)


def _tailoring_lines(tailoring: Tailoring) -> list[str]:
    def bullets(items: list[str]) -> list[str]:
        return [*(_bullet(item) for item in items), ""] if items else ["None.", ""]

    return [
        "## Tailoring",
        "",
        f"**Job Match Score: {tailoring.job_match_score}/100** ({ESTIMATE})",
        "",
        tailoring.summary,
        "",
        "### Matches",
        "",
        *bullets(tailoring.matches),
        "### Gaps",
        "",
        "Asked for in the Job Description but not shown in the CV. Add one only if "
        "you have that experience.",
        "",
        *bullets([gap_text(gap) for gap in tailoring.gaps]),
        "### What to emphasise",
        "",
        *bullets(tailoring.emphasis),
    ]
