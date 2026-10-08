# CVXpert v1.1 spec

Status: approved for implementation. Builds on `docs/SPEC.md` (v1). Vocabulary follows `GLOSSARY.md`; architecture follows ADR 0001.

## Problem Statement

v1 guarantees that a Rewrite never invents a number, but it can still invent a name: a live run turned "Worked on various tasks related to the API" into "Develop REST APIs", borrowing "REST" from the Job Description. The rewrite instructions now forbid that, and a second live run confirmed it, but nothing in code catches an invented tool, employer, title or acronym.

At the same time, a candidate who really has a skill the Job Description asks for, but left it off their CV, has no way to tell CVXpert. The Tailoring lists it as a gap and the Rewrite must leave it out.

The smoke script also reports $0 spend because OpenRouter records usage a few seconds after a run, and the README has no picture of the product working.

## Solution

- An **Unverified Term** check: after the Rewrite, a deterministic check lists names, tools, acronyms and titles that neither the CV nor a Confirmed Gap contains. The rewrite Step gets one retry with those terms named; any that remain are shown to the candidate in a "Check these terms" list instead of failing the run.
- **Confirmed Gaps**: the candidate can confirm Tailoring gaps that are true of them (checkboxes on the web page, an option on the CLI). The Rewrite may then use them, and the check accepts them.
- The smoke script waits for OpenRouter to record the spend before reporting it.
- The README gets a demo GIF and an example from the verified live run, and a launch post is drafted.

## User Stories

1. As a candidate, I want CVXpert to tell me when the Rewrite contains a tool, employer, title or acronym my CV does not contain, so that I never send a claim I cannot defend.
2. As a candidate, I want the model to get one chance to remove such terms itself, so that I see as few false alarms as possible.
3. As a candidate, I want any remaining terms listed under "Check these terms" in the report, the CLI output file and the web page, so that I can review them before applying.
4. As a candidate, I want the Rewrite still returned when only Unverified Terms remain, so that one false alarm does not throw away a good Rewrite.
5. As a candidate, I want words that only start a bullet or sentence, Markdown headings, Placeholders, month names and standard Section names ignored by the check, so that ordinary wording is not flagged.
6. As a candidate, I want the check to ignore case when comparing with my CV, so that "Javascript" in my CV and "JavaScript" in the Rewrite are treated as the same.
7. As a candidate, I want to tick "I have this" next to any Tailoring gap on the web page before the Rewrite, so that a skill I really have but forgot to list can appear in the tailored CV.
8. As a candidate using the CLI, I want to pass the gaps I confirm as an option, so that I get the same result without the web page.
9. As a candidate, I want confirmed gaps to be the only Job Description terms the Rewrite may add, so that everything in my CV stays a claim I made myself.
10. As a candidate, I want the report to list my Confirmed Gaps, so that I can see which additions came from me.
11. As a maintainer, I want the smoke script to report the actual spend of a run, so that the cost record is correct.
12. As a portfolio reader, I want a short GIF at the top of the README showing the web page working, so that I can see the product in seconds.
13. As a portfolio reader, I want the README example to come from the run that verified the stricter rewrite rule, so that the example matches the current behaviour.

## Implementation Decisions

### Unverified Term check

- A pure function compares the Rewrite text with the allowed text (the CV text plus every Confirmed Gap) and returns the Unverified Terms, de-duplicated, in order of appearance.
- Candidate terms in the Rewrite:
  - capitalised words or multi-word capitalised phrases;
  - all-caps acronyms of two or more letters, including forms with `/` or `&` such as "CI/CD";
  - tech-shaped tokens containing `.`, `+`, `#` or digits mixed with letters, such as "Node.js", "C++", "C#", "Python3".
- Ignored:
  - the first word of each line, bullet or sentence;
  - Markdown headings and emphasis markers;
  - bracketed Placeholders;
  - month names and their abbreviations;
  - standard Section names (for example Profile, Experience, Education, Skills, Projects, Summary, Certifications, Languages).
- Comparison is case-insensitive and matches whole words.
- It runs inside the rewrite Step's output validator after the number guard: one retry naming the terms. If terms remain after the retry, the Rewrite is returned with an `unverified_terms` list instead of raising. Numbers stay strict (a Fabrication error).
- Known limits, documented in the README: lowercase claim upgrades ("developed", "relational") are not caught; a name already in the CV but used in a new context passes.

### Confirmed Gaps

- The rewrite phase takes an optional list of Confirmed Gaps (free text, one per gap).
- The rewrite instructions say that Confirmed Gaps are facts the candidate supplied and may be used; any other Job Description term stays forbidden.
- CLI: `cvxpert review ... --job <file> --confirm "PostgreSQL" --confirm "CI/CD"` (repeatable). `--confirm` without `--job` is an error.
- Web page: each Tailoring gap gets an "I have this" checkbox, unticked by default; ticked gaps are passed to the rewrite phase.
- The report lists Confirmed Gaps in the Rewrite section, and lists Unverified Terms under "Check these terms".
- Amended by the v1.1 code review (owner decision Q33(a)): each Tailoring gap has a short `label` (the skill or requirement in a few words, such as "Python, 3+ years") and a `detail` (why it is a gap). Confirming a gap passes only its label; only labels join the allowed text of the number check and the Unverified Term check, so a detail never widens what they accept. The report and the web page show label and detail. `--confirm` stays free text: the candidate types a label.

### Smoke script spend

- After the run, re-read the key endpoint up to 6 times, 5 seconds apart, until `limit_remaining` changes. Report the drop. If it never changes, print that OpenRouter has not recorded the spend yet and where to check, never `$0.000000`.

### Docs and demo

- README: a GIF near the top; the Example section uses the verified run's report; known gaps updated; the Confirmed Gaps option documented.
- The GIF is recorded by driving the web page in Chrome on the example CV and Job Description (one live run, about $0.02 under the $1 key limit). It is stored in the repository and kept under 5 MB.
- A launch post draft is written outside the repository for the owner to edit and post.

## Testing Decisions

- Same seams as v1: the Pipeline phases with PydanticAI `FunctionModel` fakes and real model requests disabled; the CLI called in-process; one Streamlit AppTest; small direct tests only for awkward tokenisation edge cases.
- Unverified Term check:
  - through the Pipeline, a fake Rewrite adding "Kubernetes" is retried; a clean retry returns no Unverified Terms; a second "Kubernetes" returns the Rewrite with "Kubernetes" listed;
  - "REST" and "CI/CD" are flagged; "Javascript" in the CV and "JavaScript" in the Rewrite are not;
  - a Placeholder, a month name, a Section heading and a capitalised verb at the start of a bullet are not flagged.
- Confirmed Gaps: a confirmed "PostgreSQL" reaches the rewrite Step's prompt and is not flagged; an unconfirmed one is; `--confirm` without `--job` exits non-zero with one line; the web page passes a ticked gap through (AppTest).
- Smoke script: with a faked key endpoint whose `limit_remaining` changes on the third read, the reported spend is the drop; when it never changes, no `$0` line is printed.
- The existing v1 Kubernetes "known gap" test is replaced by the tests above.

## Out of Scope

- Catching lowercase claim upgrades.
- An LLM-based fact checker or evaluator loop.
- Everything else on the v2 roadmap.

## Further Notes

- Live spend so far on the $1 key: about $0.049 over two runs (the second run's cost, about $0.028, was read manually from OpenRouter because the script printed $0).
- Release: after merge, export to the public repository as v0.1.1 (owner pushes).
