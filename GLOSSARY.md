# CVXpert

CVXpert reads a candidate's CV, critiques it, optionally aligns it to a target job, and rewrites it without inventing anything the candidate did not write.

## Language

### Process

**Pipeline**:
The fixed sequence of Steps that turns a CV (and optional Job Description) into a Review, Tailoring and Rewrite.
_Avoid_: Workflow graph, multi-agent system, orchestrator

**Step**:
One stage of the Pipeline: parse, review, tailor or rewrite.
_Avoid_: Agent, node

### Inputs

**CV**:
The candidate's own document (PDF, DOCX or TXT) as uploaded; the single source of truth about the candidate.
_Avoid_: Resume, document, file

**Job Description**:
The text of a job posting the candidate wants to apply to; optional.
_Avoid_: JD, job posting, job offer

**Section**:
A titled part of the CV as the candidate wrote it, such as Experience or Skills.

### Outputs

**Review**:
The critique of a CV: an overall score, the CV's Sections, and a list of Findings.
_Avoid_: Analysis, feedback report

**Guideline**:
A numbered, sourced rule of good CV writing (such as "quantify impact") that Reviews and Rewrites are judged against.
_Avoid_: Best practice, tip, rule of thumb

**Finding**:
One weakness in the CV that breaks a Guideline, paired with a proposed change and a severity. Praise is not a Finding.
_Avoid_: Feedback item, suggestion, recommendation

**Overall Score**:
The model's 0–100 estimate of the CV's quality; an opinion, not a measurement.

**Job Match Score**:
The model's 0–100 estimate of how well the CV fits the Job Description; exists only when a Job Description was given.

**Tailoring**:
The comparison of a CV against a Job Description: what matches, what is missing, and what to emphasise. Each missing item, a gap, has a short label (the skill or requirement in a few words, such as "Python, 3+ years") and a detail saying why it is a gap.
_Avoid_: Job match analysis, optimisation

**Rewrite**:
A new version of the CV that applies the Findings the candidate kept and Tailoring, using only facts present in the CV or Confirmed Gaps.
_Avoid_: Enhanced CV, improved CV

**Placeholder**:
A bracketed gap in the Rewrite, such as `[X%]`, where a fact would strengthen a line but the CV does not contain it; the candidate fills it in.

**Confirmed Gap**:
The label of a Tailoring gap that the candidate states is true of them; the Rewrite may then use it as a fact. The gap's detail is never part of it.
_Avoid_: Added skill, accepted gap

**Unverified Term**:
A name, tool, acronym or title in the Rewrite that neither the CV nor a Confirmed Gap contains; shown to the candidate to check rather than silently kept.
_Avoid_: Suspicious word, flagged term

**Fabrication**:
Any number, employer, title, tool, date or achievement in the Rewrite that neither the CV nor a Confirmed Gap contains. Never allowed.
_Avoid_: Embellishment, enhancement
