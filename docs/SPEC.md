# CVXpert v1 spec

Status: implemented in v0.1.0. Vocabulary follows `GLOSSARY.md`; architecture follows ADR 0001.

## Problem Statement

A candidate has a CV and often a Job Description they want to apply to. They do not know which parts of the CV are weak, why, or how to fix them. Generic AI rewriters make it worse: they produce bland text and invent metrics, employers or skills the candidate cannot defend in an interview.

The current CVXpert repository does not solve this. Its README advertises six AI agents, PDF output and accuracy figures, but only parsing works: the review returns hardcoded scores, the "improved CV" download returns the original file, and the orchestrator is never called.

## Solution

CVXpert is a small LLM workflow the candidate runs locally, from a command line or a Streamlit page. It reads the CV, produces a Review whose every Finding cites a sourced Guideline, optionally produces a Tailoring against a Job Description, and produces a Rewrite in Markdown (optionally PDF) that applies the Findings the candidate kept. The Rewrite never contains a Fabrication: where a fact would help but the CV lacks it, the Rewrite inserts a Placeholder such as `[X%]` for the candidate to fill. The README describes only what runs.

## User Stories

### Running a Review

1. As a candidate, I want to give CVXpert my CV as a PDF, DOCX or TXT file, so that I don't have to convert it first.
2. As a candidate, I want a clear error when my PDF is a scanned image with no extractable text, so that I know to supply a text-based file instead of getting an empty Review.
3. As a candidate, I want a clear error when the file type is unsupported or the file is larger than 10 MB, so that I know what to change.
4. As a candidate, I want an Overall Score from 0 to 100, clearly labelled as the model's estimate, so that I get a rough sense of quality without mistaking it for a measurement.
5. As a candidate, I want a short summary of the Review, so that I understand the main message before reading the details.
6. As a candidate, I want the Review to list the Sections it found in my CV, so that I can see the model read my CV correctly.
7. As a candidate, I want a list of Findings, each naming the weakness, quoting or pointing to the affected text, proposing a change, and giving a severity (high, medium, low), so that I know what to fix first.
8. As a candidate, I want every Finding to cite the Guideline it is based on (for example "G02 Quantify only with numbers the candidate supplied"), so that I understand why it matters and can trust it is not the model's taste.
9. As a candidate, I want to read the full text and sources of any cited Guideline, so that I can check the advice myself.
10. As a candidate, I want the Review to contain no praise-only items, so that every Finding is something I can act on.
11. As a candidate, I want the Review to flag unclear cases (such as whether a role is current) as uncertain rather than guessing, so that I am not told to change something that is already right.

### Tailoring

12. As a candidate, I want to optionally give a Job Description as a text file or pasted text, so that the Review considers the job I am applying to.
13. As a candidate, I want a Job Match Score from 0 to 100, labelled as the model's estimate, when I give a Job Description, so that I can compare how well my CV fits different postings.
14. As a candidate, I want the Tailoring to list what in my CV matches the Job Description, so that I know my strengths for this job.
15. As a candidate, I want the Tailoring to list what the Job Description asks for that my CV does not show, so that I can decide whether I have that experience and add it myself.
16. As a candidate, I want the Tailoring to suggest what to move up or emphasise, so that the most relevant experience is read first.
17. As a candidate, I want CVXpert to never add a skill or tool to my Rewrite just because the Job Description asks for it, so that my CV stays truthful.
18. As a candidate who gives no Job Description, I want no Tailoring and no Job Match Score, and no Findings for Guidelines that need a target job (G05, G06), so that the output does not pretend to know my target.

### Rewrite

19. As a candidate, I want a Rewrite of my CV in Markdown, so that I can paste it anywhere or edit it before applying.
20. As a candidate, I want the Rewrite to apply only the Findings I kept, so that I stay in control of my CV.
21. As a candidate, I want the Rewrite to keep my own facts, voice and specifics, so that it does not read like generic AI text.
22. As a candidate, I want every missing fact in the Rewrite shown as a Placeholder like `[X%]`, `[result]`, `[team size]` or `[dates]`, so that I can see exactly what to fill in.
23. As a candidate, I want CVXpert to refuse to return a Rewrite that contains a number or date absent from my CV, so that I never send a CV with an invented metric.
24. As a candidate, I want a clear error, not a silently degraded Rewrite, when the model keeps inventing numbers, so that I know the result could not be trusted.
25. As a candidate, I want the Rewrite as a PDF too, so that I can attach it to an application directly.

### Command line

26. As a candidate, I want one command that runs the Pipeline on my CV and writes a single Markdown report (Review, Tailoring if any, Rewrite), so that I can use CVXpert without a browser.
27. As a candidate, I want to choose the output path and choose Markdown or PDF, so that the file lands where I need it in the format I need.
28. As a candidate, I want a non-zero exit code and a one-line error message when anything fails, so that I can script CVXpert and see what went wrong.
29. As a candidate, I want a clear message when my OpenRouter API key is missing, so that I know how to configure CVXpert.
30. As a candidate, I want a command that opens the Streamlit page, so that I don't have to remember the Streamlit invocation.

### Streamlit page

31. As a candidate, I want to upload my CV and optionally paste a Job Description on one page, so that starting a Review is one step.
32. As a candidate, I want to see the Overall Score, the Job Match Score and the Findings grouped by severity, each with its Guideline, so that I can scan the results quickly.
33. As a candidate, I want to untick Findings I disagree with before the Rewrite, so that the Rewrite applies only the advice I accept.
34. As a candidate, I want to see the Rewrite on the page with its Placeholders visible, so that I can check it before downloading.
35. As a candidate, I want to download the Rewrite as Markdown or PDF, so that I can use it immediately.
36. As a candidate, I want errors (scanned PDF, missing key, Fabrication refused) shown as readable messages on the page, so that I am not looking at a stack trace.

### Configuration and cost

37. As a candidate, I want to set my OpenRouter API key in an environment variable or a `.env` file, so that the key never lives in code.
38. As a candidate, I want to override the model by name, so that I can try a different OpenRouter model without editing code.
39. As a candidate, I want a cheap, capable default model (DeepSeek V4.1 Flash), so that a full run costs around a cent.

### Maintainer and portfolio reader

40. As a maintainer, I want every test to run without network access or an API key, so that tests are free, fast and deterministic.
41. As a maintainer, I want any accidental real model request during tests to fail loudly, so that CI can never spend money.
42. As a maintainer, I want the Guidelines kept as one versioned, cited text in the package, so that changing advice is a reviewed diff, not a prompt edit buried in code.
43. As a maintainer, I want a single opt-in live smoke run that refuses to start unless my OpenRouter key has a credit limit of at most $1, so that a live check can never overspend.
44. As a maintainer, I want CI to run lint and tests on every push and pull request, so that the branch stays green.
45. As a portfolio reader, I want the README to describe CVXpert as an LLM workflow with four Steps, with a real before-and-after example produced by the tool, so that the claims match the code.
46. As a portfolio reader, I want an ADR and a research note explaining why there is no LangGraph, so that I can see the trade-off was deliberate.
47. As a portfolio reader, I want an MIT LICENSE file, so that I know how I may reuse the code.
48. As a new user, I want fictional example CV and Job Description files in the repository, so that I can try CVXpert without using my own data.

## Implementation Decisions

### Shape

- The Pipeline is plain Python functions; there is no LangGraph, LangChain, FastAPI or orchestrator class (ADR 0001). The public Python API is synchronous, because both callers (CLI and Streamlit) are synchronous and the Steps run one after the other; LLM Steps use PydanticAI's synchronous run. ADR 0001's "async" wording is amended to "plain functions".
- The Pipeline has two phases so the Streamlit page can let the candidate untick Findings in between:
  - **review phase**: CV file path and optional Job Description in; parsed CV, Review and optional Tailoring out.
  - **rewrite phase**: the review-phase result and the set of kept Finding IDs in; Rewrite out.
  - A convenience function runs both phases, keeping every Finding; the CLI uses it.
- Modules, by responsibility:
  - **Parsing**: deterministic text and metadata extraction for PDF (pypdf), DOCX (python-docx) and TXT; size and type validation; a scanned-PDF error when extracted text is empty or whitespace. Section detection is not done here (it is part of the Review).
  - **Guidelines**: the 24 Guidelines G01–G24 from the research note, stored as one Markdown document shipped inside the package, plus a loader that returns their IDs and titles. The full document is injected into the Review and Rewrite instructions.
  - **Steps**: one PydanticAI agent per LLM Step (review, tailor, rewrite), each with a typed output model and instructions that state the no-Fabrication rule and the Placeholder convention.
  - **Fabrication guard**: a deterministic function that lists numbers, percentages and years in a text that do not appear in the CV text; bracketed Placeholders are ignored. It runs as the rewrite agent's output validator.
  - **Export**: Markdown report rendering, and Markdown-to-PDF conversion: Markdown to HTML with `markdown` (BSD-3), then HTML to PDF with `fpdf2` (LGPL-3.0). `markdown-pdf` was rejected because it and its PyMuPDF dependency are AGPL-3.0, which conflicts with CVXpert's MIT licence.
  - **Configuration**: environment-driven settings.
  - **CLI** and **Streamlit page**: thin callers of the Pipeline.

### Data shapes (typed output models)

- **Review**: overall score (0–100), summary, Sections (title and text, in CV order), Findings.
- **Finding**: an ID unique within the Review, Guideline ID, Section title, the affected text, the problem, the proposed change, severity (`high`, `medium`, `low`), and an "uncertain" flag.
- **Tailoring**: Job Match Score (0–100), summary, matches, gaps (asked for but not shown in the CV), and emphasis suggestions.
- **Rewrite**: the full CV as Markdown, plus the list of Placeholders it contains.

### Rules enforced in code, not only in prompts

- A Finding whose Guideline ID is not one of G01–G24 fails validation; the model gets one retry with the reason, then the Step errors.
- Without a Job Description, Findings citing G05 or G06 are dropped and the tailor Step does not run.
- The Fabrication guard: any number, percentage or year in the Rewrite that does not appear in the CV text triggers one retry with the offending tokens named; if the retry still fails, the rewrite phase raises a Fabrication error and returns no Rewrite. Bracketed Placeholders are exempt. Number matching normalises thousands separators, percent signs and trailing decimal zeros.
- Known v1 gap, accepted: an invented tool, employer or title is forbidden by the instructions but not caught by the guard; a proper-noun guard is v2.

### Model and provider

- OpenRouter through PydanticAI's OpenRouter model and provider, with "require parameters" routing so only endpoints that support the request are used.
- Default model `deepseek/deepseek-v4.1-flash` (supports tools and structured outputs; $0.035 per million input tokens and $1.00 per million output tokens on 2026-10-08). Override with `CVXPERT_MODEL`.
- API key from `OPENROUTER_API_KEY` (environment or `.env`). A missing key is reported before any Step runs. A `.env.example` lists the variables with no values.

### CLI contract

- `cvxpert review <CV> [--job <file>] [--out <path>] [--format md|pdf]` runs both phases with all Findings kept and writes one report: Review, Tailoring (if any), Rewrite. Default output is next to the CV, named after it. Exit code 0 on success, non-zero with a one-line message on any error.
- `cvxpert web` starts the Streamlit page.

### Repository and packaging

- `uv` with `pyproject.toml` as the only dependency manifest; Python 3.11 or newer; ruff for lint and format.
- Dependencies after v1: pydantic-ai-slim with the OpenRouter extra, pydantic, pydantic-settings, pypdf, python-docx, streamlit, markdown, fpdf2. Removed: markdown-pdf, langgraph, langchain, langchain-openai, fastapi, uvicorn, pytesseract, pillow, requests usage in the UI, and the sphinx and other unused dev tools.
- Deleted: the API layer, the orchestrator, the base agent class, the LangChain helper module, `run.py`, `setup.py`, both requirements files, the Dockerfile, and the stale docs (`Planning.md`, `Task.md`, `project_structure.md`, `SETUP.md`). Setup instructions move into the README.
- CI: install with uv, ruff check, pytest; no Docker job.
- `examples/` holds a fictional CV with deliberate weaknesses (vague bullets, no metrics, mixed tenses, "Responsible for…", pronouns) and a fictional Job Description.
- README is rewritten last-but-one and updated per ticket: what CVXpert is (an LLM workflow with four Steps), install, configure, CLI and Streamlit usage, the Guidelines and their sources, the no-Fabrication rule and its known gap, a before-and-after excerpt from the live smoke run, limitations, roadmap (v2). It names nothing that does not run.
- LICENSE: MIT, copyright 2026 Chamel Nadir Bouacha.

## Testing Decisions

- A good test drives external behaviour through the highest seam and asserts on outputs a user would see: the Review, Tailoring and Rewrite objects, the report file, exit codes and error messages. Tests do not assert on prompt wording or internal call order.
- **Primary seam**: the Pipeline's two phases and the convenience function, called with real CV files and a fake model. The fake is PydanticAI's `FunctionModel`, swapped in with the agent override mechanism. Real model requests are globally disabled in the test configuration so an accidental call fails.
- Behaviour covered through the primary seam:
  - PDF, DOCX and TXT CVs produce a Review; fixtures are generated at test time (python-docx for DOCX; a small committed text-PDF fixture; pypdf for the empty-text PDF), and an empty-text PDF produces the scanned-PDF error.
  - Guideline validation: a fake Review whose Findings cite every Guideline G01–G24 passes; a Finding citing an unknown ID triggers a retry and then an error.
  - The Guideline catalogue loads exactly G01–G24, each with a title and at least one source.
  - Tailoring runs only when a Job Description is given; without one, G05 and G06 Findings are dropped and there is no Job Match Score.
  - Kept Findings: only the kept Finding IDs reach the rewrite Step.
  - Fabrication guard: a fake Rewrite inventing "40%" is retried; if the retry is clean the Rewrite is returned; if it invents again a Fabrication error is raised. A Rewrite using `[X%]` passes. A fake Rewrite that adds "Kubernetes" passes (documents the known v1 gap).
  - A missing API key produces the configuration error before any Step runs.
- **Thin checks over the same fake model**:
  - CLI: call the entry point in-process with an argument list; assert on the written report, the exit code and the error line.
  - Streamlit: one Streamlit `AppTest` run that uploads the example CV, unticks a Finding, requests the Rewrite, and confirms the unticked Finding did not reach the rewrite Step.
  - PDF export: Markdown in, a non-empty PDF out whose extracted text contains a known line.
- A small direct test of the Fabrication guard is allowed only for edge cases awkward to reach through the Pipeline (thousands separators, years inside date ranges).
- **Live smoke run** (not in CI, opt-in, run once after all tickets pass): runs the example CV and Job Description through both phases on the default model. Before any model call it reads the OpenRouter key's limit from the key endpoint and refuses to run if the limit is unset or above $1. It saves the report for the README excerpt.
- Prior art: the existing parsing tests (pytest, `tmp_path` fixtures, sample CV text fixture) and document-utility tests; they are kept where the behaviour survives and rewritten to the primary seam where it does not.

## Out of Scope

- DOCX output, styled PDF templates, and region-specific Guidelines (page length, photo, personal details, references line, work authorisation, address).
- An evaluator-optimizer loop for Rewrite quality, and a proper-noun Fabrication guard.
- OCR for scanned PDFs.
- An HTTP API, authentication, a database, CV history, user accounts, a hosted demo, PyPI publishing, and a Docker image.
- Languages other than English.
- Making the GitHub repository public (the owner does this).

## Further Notes

- Research: `docs/research/agentic-architectures.md` (architecture) and `docs/research/cv-guidelines.md` (Guidelines and their sources). Non-PDF source wording there is paraphrased; re-check before quoting it in product copy.
- Spending: the only paid calls are the live smoke run, within a $1 ceiling enforced as an OpenRouter key credit limit. At the default model's prices the run is expected to cost about one cent; the actual cost is read from OpenRouter after the run and reported.
- Work happens on branch `finish-mvp`, one commit per ticket, no push.
