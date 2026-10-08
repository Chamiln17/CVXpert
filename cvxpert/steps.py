"""LLM Steps: one PydanticAI agent per Step, each with a typed output model."""

import re
from collections.abc import Sequence
from typing import Literal, get_args

from pydantic import BaseModel, Field, computed_field
from pydantic.json_schema import SkipJsonSchema
from pydantic_ai import Agent, ModelRetry, RunContext, UnexpectedModelBehavior
from pydantic_ai.models import Model

from cvxpert.errors import FabricationError, StepError
from cvxpert.guidelines import NEEDS_JOB, guidelines_text, id_range, load_guidelines
from cvxpert.parsing import ParsedCV

Severity = Literal["high", "medium", "low"]
SEVERITIES: tuple[Severity, ...] = get_args(Severity)  # highest first


class Section(BaseModel):
    title: str
    text: str


class Finding(BaseModel):
    id: str = Field(description="Unique within the Review, e.g. F1")
    guideline_id: str = Field(description=f"The cited Guideline, {id_range()}")
    section: str = Field(description="Title of the Section the Finding is in")
    affected_text: str = Field(description="The CV text the Finding is about")
    problem: str
    proposed_change: str
    severity: Severity
    uncertain: bool = Field(
        description="True when the case is unclear, e.g. whether a role is current"
    )


class Review(BaseModel):
    overall_score: int = Field(ge=0, le=100, description="Your estimate of CV quality")
    summary: str
    sections: list[Section] = Field(description="The CV's Sections, in CV order")
    findings: list[Finding]


_REVIEW_INSTRUCTIONS = f"""\
You review a candidate's CV against the Guidelines below and return a Review.

- List the CV's Sections in CV order, each with its title and text as written.
- Each Finding is one weakness that breaks one Guideline: cite that Guideline's ID,
  quote the affected text, state the problem, propose a change, and give a severity.
- Give each Finding an ID unique within the Review (F1, F2, ...).
- Praise is not a Finding. Report only things the candidate can act on.
- When a case is unclear (for example whether a role is current), set uncertain
  to true instead of guessing.
- Proposed changes use only facts in the CV. Never invent a number, employer,
  title, tool, skill, date or outcome. Where a fact is missing, write a bracketed
  Placeholder such as [X%], [result], [team size] or [dates].
- The overall score (0-100) is your estimate of the CV's quality.

{guidelines_text()}"""

review_agent = Agent(
    output_type=Review,
    instructions=_REVIEW_INSTRUCTIONS,
    deps_type=str | None,  # the Job Description, if any
    retries={"output": 1},
    name="review",
)


@review_agent.instructions
def _job_instructions(ctx: RunContext[str | None]) -> str:
    if not ctx.deps:
        return f"No Job Description is given, so do not cite {' or '.join(NEEDS_JOB)}."
    return (
        f"The candidate targets the Job Description below; {' and '.join(NEEDS_JOB)} "
        "apply.\n\n"
        f"# Job Description\n\n{ctx.deps}"
    )


@review_agent.output_validator
def _check_review(review: Review) -> Review:
    unknown = sorted(
        {f.guideline_id for f in review.findings} - load_guidelines().keys()
    )
    if unknown:
        raise ModelRetry(f"Unknown Guideline IDs {unknown}; cite only {id_range()}")
    ids = [f.id for f in review.findings]
    if len(ids) != len(set(ids)):
        raise ModelRetry("Finding IDs must be unique within the Review")
    return review


def review(cv: ParsedCV, model: Model, job_description: str | None = None) -> Review:
    """Review Step: the CV text (and optional Job Description) in, a validated Review out.

    Without a Job Description, Findings citing a Guideline in NEEDS_JOB are dropped.
    """
    result = _run(review_agent, cv.text, model, deps=job_description)
    if not job_description:
        result.findings = [
            f for f in result.findings if f.guideline_id not in NEEDS_JOB
        ]
    return result


class Gap(BaseModel):
    label: str = Field(
        description="The skill or requirement in a few words, e.g. PostgreSQL or "
        "Python, 3+ years"
    )
    detail: str = Field(description="Why it is a gap")


class Tailoring(BaseModel):
    job_match_score: int = Field(
        ge=0,
        le=100,
        description="Your estimate of how well the CV fits the Job Description",
    )
    summary: str
    matches: list[str] = Field(description="What in the CV matches the Job Description")
    gaps: list[Gap] = Field(
        description="What the Job Description asks for that the CV does not show"
    )
    emphasis: list[str] = Field(
        description="What already in the CV to move up or give more space"
    )


_TAILOR_INSTRUCTIONS = """\
You compare a candidate's CV with a Job Description and return a Tailoring.

- The Job Match Score (0-100) is your estimate of how well the CV fits the job.
- Matches: what the CV shows that the Job Description asks for.
- Gaps: what the Job Description asks for that the CV does not show. Report each
  gap; never suggest adding it to the CV. Only the candidate can decide whether
  they have that experience.
- Give each gap a label and a detail. The label names the skill or requirement in
  a few words, such as "PostgreSQL" or "Python, 3+ years"; the candidate may
  confirm it as true of them. The detail says why it is a gap.
- Emphasis: what already in the CV to move up or give more space. Use only
  content in the CV. Never propose adding a skill, tool, employer, title, number
  or outcome the CV does not contain."""

tailor_agent = Agent(
    output_type=Tailoring,
    instructions=_TAILOR_INSTRUCTIONS,
    retries={"output": 1},
    name="tailor",
)


def tailor(cv: ParsedCV, job_description: str, model: Model) -> Tailoring:
    """Tailor Step: the CV text and the Job Description in, a Tailoring out."""
    prompt = f"# CV\n\n{cv.text}\n\n# Job Description\n\n{job_description}"
    return _run(tailor_agent, prompt, model)


def _run(agent: Agent, prompt: str, model: Model, **kwargs):
    try:
        return agent.run_sync(prompt, model=model, **kwargs).output
    except UnexpectedModelBehavior as e:
        reason = e.__cause__ or e
        if isinstance(reason, _Fabricated):
            raise FabricationError(
                f"The {agent.name} Step kept writing numbers that are not in the CV, "
                f"so no Rewrite was produced: {reason.tokens}"
            ) from e
        raise StepError(
            f"The {agent.name} Step failed after one retry: {reason}"
        ) from e


# A bracketed Placeholder such as [X%]; a Markdown link's text ([text](url)) is not one.
_PLACEHOLDER = re.compile(r"\[[^\[\]]*\](?!\()")


class Rewrite(BaseModel):
    markdown: str = Field(description="The whole rewritten CV as Markdown")
    # Set by the rewrite Step's check, never by the model, so kept out of its schema.
    unverified_terms: SkipJsonSchema[list[str]] = []
    # The Confirmed Gaps (gap labels) the Rewrite was allowed to use, for the report.
    confirmed_gaps: SkipJsonSchema[list[str]] = []

    @computed_field
    @property
    def placeholders(self) -> list[str]:
        """The Placeholders in the Rewrite, in order, without repeats."""
        return list(dict.fromkeys(_PLACEHOLDER.findall(self.markdown)))


_REWRITE_INSTRUCTIONS = f"""\
You rewrite a candidate's CV in Markdown, applying the Findings given and the
Tailoring if one is given, and following the Guidelines below.

- Apply only the Findings given. Leave everything else as the candidate wrote it.
- Keep the candidate's facts, voice and specifics. Do not make the text generic.
- Never add a number, employer, title, tool, skill, date or outcome the CV does
  not contain. Copy numbers, dates and contact details exactly as the CV writes them.
- Where a fact would strengthen a line but the CV does not contain it, write a
  bracketed Placeholder such as [X%], [result], [team size] or [dates] for the
  candidate to fill in.
- Never use a term from the Job Description that the CV does not contain, even
  when a Finding or the Tailoring names it. Keep the CV's own wording.
- Confirmed Gaps are facts the candidate supplied, not in the CV yet. You may use
  them as if the CV contained them. They are the only Job Description terms you
  may add; every other term the CV does not contain stays forbidden.
- Never raise the level of a claim: "worked on" must not become "developed", and
  "the database" must not become "relational database".
- From the Tailoring, use only what to emphasise: reorder and give space to
  content already in the CV. Never add a gap from the Tailoring to the CV
  unless it is a Confirmed Gap.
- Return the whole CV, from the candidate's name to the last Section.

{guidelines_text()}"""

rewrite_agent = Agent(
    output_type=Rewrite,
    instructions=_REWRITE_INSTRUCTIONS,
    deps_type=str,  # the CV text, for the Fabrication guard
    retries={"output": 1},
    name="rewrite",
)


@rewrite_agent.output_validator
def _check_rewrite(ctx: RunContext[str], result: Rewrite) -> Rewrite:
    """Invented numbers always retry, then fail. Unverified Terms retry once; any
    left on the last attempt are returned with the Rewrite. Both share one retry."""
    terms = unverified_terms(result.markdown, ctx.deps)
    invented = fabricated_numbers(result.markdown, ctx.deps)
    if invented:
        raise _Fabricated(invented, terms)
    if terms and not ctx.last_attempt:
        raise ModelRetry(_terms_reason(terms))
    result.unverified_terms = terms
    return result


def _terms_reason(terms: list[str]) -> str:
    return (
        f"Unverified Terms: {', '.join(terms)} not in the CV. Remove them or keep "
        "the CV's own wording."
    )


class _Fabricated(ModelRetry):
    """The guard's retry reason, keeping the offending tokens for the final error."""

    def __init__(self, tokens: list[str], terms: list[str]):
        self.tokens = ", ".join(tokens)
        super().__init__(
            f"Fabrication: {self.tokens} not in the CV. Use only numbers the CV "
            "contains, or a bracketed Placeholder such as [X%]."
            + (f" {_terms_reason(terms)}" if terms else "")
        )


def rewrite(
    cv: ParsedCV,
    findings: list[Finding],
    tailoring: Tailoring | None,
    model: Model,
    confirmed_gaps: Sequence[str] = (),
) -> Rewrite:
    """Rewrite Step: the CV text, the kept Findings, the Tailoring and the Confirmed
    Gaps in, a Rewrite out. Confirmed Gaps are gap labels, never their details; they
    count as CV text for both checks.

    Raises FabricationError when the retry still holds a number absent from the CV;
    Unverified Terms still there after the retry come back in ``unverified_terms``.
    """
    kept = "\n".join(f.model_dump_json() for f in findings) or "None."
    prompt = f"# CV\n\n{cv.text}\n\n# Findings to apply\n\n{kept}"
    if tailoring:
        prompt += f"\n\n# Tailoring\n\n{tailoring.model_dump_json()}"
    if confirmed_gaps:
        prompt += "\n\n# Confirmed Gaps\n\n" + "\n".join(
            f"- {g}" for g in confirmed_gaps
        )
    allowed = "\n".join([cv.text, *confirmed_gaps])
    result = _run(rewrite_agent, prompt, model, deps=allowed)
    result.confirmed_gaps = list(confirmed_gaps)
    return result


# The guard's tokens: "1,200" (thousands separators), "3.5", "2019". A hyphen or
# dash is never part of a token, so "2019-2021" yields the years 2019 and 2021, and
# "06/2018" yields 06 and 2018. A trailing percent sign is kept for the retry message
# but dropped for comparison, so "40%" and "40" compare equal.
_NUMBER = re.compile(r"(?:\d{1,3}(?:,\d{3})+(?!\d)|\d+)(?:\.\d+)?%?")
# A numbered-list marker ("1. ", "2) ") at the start of a line is Markdown
# structure, not a fact, so the Rewrite may add one.
_LIST_MARKER = re.compile(r"^[ \t]*\d+[.)][ \t]", re.MULTILINE)


def _number_key(token: str) -> str:
    """Drop thousands separators, the percent sign and trailing decimal zeros
    ("3.80" is "3.8"). Leading zeros stay: "06" and "6" differ."""
    key = token.replace(",", "").rstrip("%")
    return key.rstrip("0").rstrip(".") if "." in key else key


def fabricated_numbers(rewrite_text: str, cv_text: str) -> list[str]:
    """Numbers, percentages and years in the Rewrite that the CV text lacks.

    Placeholders and numbered-list markers in the Rewrite are ignored.
    """
    in_cv = {_number_key(t) for t in _NUMBER.findall(cv_text)}
    text = _LIST_MARKER.sub("", _PLACEHOLDER.sub("", rewrite_text))
    invented = [t for t in _NUMBER.findall(text) if _number_key(t) not in in_cv]
    return list(dict.fromkeys(invented))


# Unverified Term candidates: a compound acronym ("CI/CD", "R&D"), else a word or a
# tech-shaped token ("Node.js", "C++", "C#", "Python3"). A trailing "." is dropped.
_TERM = re.compile(r"[A-Z][A-Z0-9]*(?:[/&][A-Z][A-Z0-9]*)+|[A-Za-z0-9][A-Za-z0-9.+#]*")
_LINE_START = re.compile(r"^\s*(?:[#>*+-]+\s*|\d+[.)]\s+)*")
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_EMPHASIS = re.compile(r"[*_`]")
# Months, their abbreviations and common Section names.
_IGNORED_WORDS = {
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
    "jan",
    "feb",
    "mar",
    "apr",
    "jun",
    "jul",
    "aug",
    "sep",
    "sept",
    "oct",
    "nov",
    "dec",
    "profile",
    "experience",
    "education",
    "skills",
    "projects",
    "summary",
    "certifications",
    "languages",
    "work",
    "contact",
    "awards",
    "publications",
    "interests",
    "references",
}


def _words(text: str) -> set[str]:
    """The text's lowercased tokens, compound acronyms also split into their parts."""
    words = set()
    for match in _TERM.findall(text):
        token = match.rstrip(".").lower()
        words.update([token, *re.split(r"[/&]", token)])
    return words


TokenKind = Literal["term", "word"]


def _kind(token: str) -> TokenKind | None:
    """'term' for an acronym or tech-shaped token, 'word' for a capitalised word,
    None for anything else."""
    letters = sum(c.isalpha() for c in token)
    if not letters:
        return None  # numbers are the Fabrication guard's job
    if any(c in ".+#/&" or c.isdigit() for c in token):
        return "term"
    if letters > 1 and token.isupper():
        return "term"
    if letters > 1 and token[0].isupper():  # not "I"
        return "word"
    return None


def unverified_terms(rewrite_text: str, allowed_text: str) -> list[str]:
    """Names, tools, acronyms and titles in the Rewrite that the allowed text (the CV
    text, plus any Confirmed Gaps) lacks, in order of appearance, without repeats.

    Adjacent candidates form one phrase, reported when any of its words is missing.
    A capitalised word starting a line, bullet or sentence, a month and a Section
    name are ignored, as are Placeholders and Markdown markers.
    """
    allowed = _words(allowed_text)
    found: dict[str, str] = {}
    text = _PLACEHOLDER.sub(" ", _EMPHASIS.sub("", rewrite_text))
    for line in text.splitlines():
        for sentence in _SENTENCE_END.split(_LINE_START.sub("", line)):
            phrase: list[str] = []
            end = 0
            for i, match in enumerate(_TERM.finditer(sentence)):
                token = match.group().rstrip(".")
                kind = _kind(token)
                if kind == "word" and (i == 0 or token.lower() in _IGNORED_WORDS):
                    kind = None
                if phrase and (not kind or sentence[end : match.start()] != " "):
                    _record_phrase(phrase, allowed, found)
                    phrase = []
                if kind:
                    phrase.append(token)
                    end = match.start() + len(token)
            _record_phrase(phrase, allowed, found)
    return list(found.values())


def _record_phrase(phrase: list[str], allowed: set[str], found: dict[str, str]) -> None:
    """Record the phrase as an Unverified Term when any of its words is not allowed."""
    if any(token.lower() not in allowed for token in phrase):
        text = " ".join(phrase)
        found.setdefault(text.lower(), text)
