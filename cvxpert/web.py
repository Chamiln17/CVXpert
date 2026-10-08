"""Streamlit page: upload a CV, review it, untick Findings, rewrite. Run ``cvxpert web``."""

import tempfile
from pathlib import Path

import streamlit as st

from cvxpert import pipeline
from cvxpert.errors import one_line
from cvxpert.export import (
    ESTIMATE,
    PRIVACY_NOTICE,
    finding_heading,
    gap_text,
    guideline_text,
    markdown_to_pdf,
    rewrite_lists,
)
from cvxpert.steps import SEVERITIES

_ESTIMATE = f"{ESTIMATE.capitalize()}."
_CONFIRM_KEY = "confirm-"  # the "I have this" checkbox key prefix, plus the gap index


def _review(upload, job_description: str) -> pipeline.ReviewPhaseResult:
    with tempfile.TemporaryDirectory() as folder:
        cv_path = Path(folder) / Path(upload.name).name  # keeps the suffix for parsing
        cv_path.write_bytes(upload.getvalue())
        return pipeline.review_phase(cv_path, job_description.strip() or None)


def _show_error(e: Exception) -> None:
    st.error(one_line(e))


st.title("CVXpert")
st.info(PRIVACY_NOTICE)
upload = st.file_uploader("CV", type=["pdf", "docx", "txt"])
job_description = st.text_area("Job Description (optional)")

if upload and st.button("Review", key="run-review"):
    st.session_state.pop("rewrite", None)
    for key in [k for k in st.session_state if str(k).startswith(_CONFIRM_KEY)]:
        del st.session_state[key]  # a new Tailoring starts with every gap unticked
    try:
        st.session_state["result"] = _review(upload, job_description)
    except Exception as e:  # any failure: one readable line, no traceback
        st.session_state.pop("result", None)
        _show_error(e)

result: pipeline.ReviewPhaseResult | None = st.session_state.get("result")
if result:
    review = result.review
    st.metric("Overall Score", f"{review.overall_score}/100", help=_ESTIMATE)
    if result.tailoring:
        st.metric(
            "Job Match Score", f"{result.tailoring.job_match_score}/100", help=_ESTIMATE
        )
    st.caption(f"Scores are {ESTIMATE}.")
    st.write(review.summary)

    st.header("Findings")
    st.caption(
        "Untick the Findings you reject; the Rewrite applies only the ticked ones."
    )
    kept = set()
    for severity in SEVERITIES:
        findings = [f for f in review.findings if f.severity == severity]
        if findings:
            st.subheader(f"{severity.capitalize()} severity")
        for f in findings:
            if st.checkbox(finding_heading(f), value=True, key=f"keep-{f.id}"):
                kept.add(f.id)
            st.caption(
                f'{f.section}: "{f.affected_text}"  \n'
                f"Problem: {f.problem}  \nProposed change: {f.proposed_change}"
            )
            with st.expander(f"Guideline {f.guideline_id}"):
                st.markdown(guideline_text(f.guideline_id))
    if not review.findings:
        st.write("No Findings.")

    confirmed = []
    if result.tailoring and result.tailoring.gaps:
        st.header("Gaps")
        st.caption(
            "Asked for in the Job Description but not shown in the CV. Tick a gap "
            "only if it is true of you; the Rewrite may then use it."
        )
        for i, gap in enumerate(result.tailoring.gaps):
            st.markdown(f"- {gap_text(gap)}")
            if st.checkbox("I have this", key=f"{_CONFIRM_KEY}{i}"):
                confirmed.append(gap.label)  # only the label, never the detail

    if st.button("Rewrite", key="run-rewrite"):
        try:
            st.session_state["rewrite"] = pipeline.rewrite_phase(
                result, kept, confirmed
            )
        except Exception as e:  # any failure: one readable line, no traceback
            st.session_state.pop("rewrite", None)
            _show_error(e)

rewrite = st.session_state.get("rewrite")
if rewrite:
    st.header("Rewrite")
    for heading, note, items in rewrite_lists(rewrite):
        st.subheader(heading)
        if note:
            st.caption(note)
        st.markdown("\n".join(f"- {item}" for item in items) or "None.")
    st.subheader("Rewritten CV")
    st.markdown(rewrite.markdown)
    md_column, pdf_column = st.columns(2)
    md_column.download_button(
        "Download Markdown",
        rewrite.markdown,
        file_name="cv-rewrite.md",
        mime="text/markdown",
    )
    pdf_column.download_button(
        "Download PDF",
        markdown_to_pdf(rewrite.markdown),
        file_name="cv-rewrite.pdf",
        mime="application/pdf",
    )
