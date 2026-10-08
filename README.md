# CVXpert

CVXpert is an LLM workflow, run locally, that reviews a CV against 24 cited Guidelines, optionally tailors it to a Job Description, and rewrites it without inventing facts. It is a fixed Pipeline of four Steps, written as plain Python functions:

1. **parse**: read the CV text from a PDF, DOCX or TXT file (up to 10 MB). No model call.
2. **review**: an OpenRouter model returns a Review: an Overall Score, a summary, the CV's Sections and Findings that each cite a Guideline.
3. **tailor** (only with a Job Description): the model compares the CV with the Job Description and returns a Tailoring.
4. **rewrite**: the model rewrites the whole CV in Markdown, applying the kept Findings and the Tailoring; a check in code refuses a Rewrite with invented numbers.

The review, tailor and rewrite Steps are PydanticAI agents with typed outputs. There is no agent loop and no orchestration framework (see `docs/adr/`).

> **Privacy:** a CV is personal data. Every run sends the CV text (and the Job Description, if given) to OpenRouter and the chosen model's provider, using your own OpenRouter API key. Nothing else leaves your machine, and CVXpert stores nothing beyond the report files you ask it to write.

## Install

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/Chamiln17/CVXpert.git
cd CVXpert
uv sync
```

## Configure

Set these in the environment or in a `.env` file in the working directory (see `.env.example`):

- `OPENROUTER_API_KEY`: your OpenRouter API key. Required; the command checks it before any Step runs.
- `CVXPERT_MODEL`: the OpenRouter model to use. Default: `deepseek/deepseek-v4.1-flash`.

Each run makes two paid OpenRouter requests, one for the review Step and one for the rewrite Step, and `--job` adds one more for the tailor Step; each Step may retry once if the model returns invalid output or, for the rewrite Step, an invented number.

## Command line

One command reviews and rewrites a CV and writes a Markdown or PDF report:

```sh
uv run cvxpert review examples/cv.txt
uv run cvxpert review examples/cv.txt --job examples/job-description.txt
uv run cvxpert review path/to/cv.pdf --out review.md
uv run cvxpert review path/to/cv.pdf --format pdf
```

The report holds the Review, the Tailoring (with `--job`) and the Rewrite. The Review has:

- an Overall Score from 0 to 100, labelled as the model's estimate, not a measurement;
- a short summary;
- the CV's Sections as the model found them;
- the Findings, high severity first. Each names the Section, the affected text, the problem, a proposed change and the Guideline it cites, and may be marked uncertain;
- the title, full Rule and sources of every Guideline cited.

### Tailoring to a Job Description

`--job <file>` takes a Job Description as a UTF-8 text file. The review Step then sees the Job Description and may cite G05 and G06, the Guidelines that need a target job. A tailor Step compares the CV text with the Job Description, and the report gains a Tailoring section:

- a Job Match Score from 0 to 100, labelled as the model's estimate;
- a short summary;
- matches: what in the CV the Job Description asks for;
- gaps: what the Job Description asks for that the CV does not show. Gaps are reported, never added to the CV; only you know whether you have that experience;
- what to emphasise: content already in the CV to move up or give more space.

Without `--job`, the tailor Step does not run, the report has no Tailoring and no Job Match Score, and any Finding citing G05 or G06 is dropped.

### The Rewrite

The rewrite Step sees the CV text, the Findings, the Tailoring (if any) and the Guidelines, and returns the whole CV in Markdown. The command keeps every Finding; in Python, `cvxpert.pipeline.rewrite_phase(result, kept_ids)` rewrites applying only the Findings whose IDs you keep. Its instructions tell the model to keep your facts, voice and specifics, and to take only what to emphasise from the Tailoring, never its gaps. They also forbid any Job Description term your CV does not contain and any raised claim: "worked on" must not become "developed", and "the database" must not become "relational database". A G06 Finding is advice for you ("if accurate, consider the posting's term X"); the Rewrite never applies a posting term itself.

**No Fabrication.** The Rewrite may not add a number, employer, title, tool, skill, date or outcome that your CV does not contain. Where a fact would strengthen a line but your CV lacks it, the Rewrite shows a Placeholder in brackets, such as `[X%]`, `[result]`, `[team size]` or `[dates]`, for you to fill in. The report lists every Placeholder above the rewritten CV.

A check in code enforces the rule for numbers: every number, percentage and year in the Rewrite must appear in the CV text. Thousands separators, percent signs and trailing decimal zeros are ignored when comparing (`1,200` matches `1200`, `40%` matches `40`, `3.80` matches `3.8`); leading zeros are not (`06/2018` does not match `6/2018`). Placeholders and numbered-list markers such as `1.` at the start of a line are skipped. If the Rewrite holds a number your CV does not, the model gets one retry with the offending numbers named; if the retry still holds one, the command fails with a Fabrication error and writes no report.

**Known gaps.** The check covers numbers written in digits only, and it compares each number against every number in the CV. These are forbidden by the rewrite Step's instructions but not caught in code in v1:

- an invented tool, employer or title (say, "Kubernetes" when your CV never mentions it); a proper-noun guard is planned for v2;
- a Job Description term your CV does not contain, or a raised claim (say, "Develop REST APIs" for "Worked on various tasks related to the API");
- a number written as a word (say, "led a team of five" when your CV gives no team size);
- a number from your CV reused in a new context (say, your "30%" cut in load time turned into a 30% rise in sales), because the check only asks whether the number appears anywhere in the CV.

Read the Rewrite before you send it.

`--format md` (the default) writes the report as Markdown; `--format pdf` writes the same report as a PDF. Without `--out`, the report is written next to the CV as `<CV name>.cvxpert.md` or `<CV name>.cvxpert.pdf`. The PDF is plain: Markdown is converted to HTML with `markdown`, then to PDF with `fpdf2`, in a bundled Noto Sans font that covers Latin scripts, dashes, curly quotes and currency signs. Characters outside that set (emoji, non-Latin scripts) are left out of the PDF with a warning. When the run fails, the command prints one `cvxpert: error: ...` line to stderr and exits with code 1 (bad arguments print argparse usage and exit with code 2). Failures include a missing API key, a missing, unreadable or empty Job Description file, an unsupported file type, a file over 10 MB, a scanned PDF with no extractable text, a review, tailor or rewrite Step that returns invalid output twice, and a Rewrite that invents a number twice.

`examples/` holds a fictional CV with deliberate weaknesses and a fictional Job Description.

## The web page

```sh
uv run cvxpert web
```

opens a Streamlit page in your browser (it runs `streamlit run` on `cvxpert/web.py` with the current Python). Upload a CV (PDF, DOCX or TXT), optionally paste a Job Description, and press Review. The page shows the Overall Score and, with a Job Description, the Job Match Score, both labelled as the model's estimate, then the Findings grouped by severity, each with the ID and title of the Guideline it cites and an expander with that Guideline's full Rule and sources. Every Finding has a tick box, ticked by default; untick the ones you reject and press Rewrite. The Rewrite applies only the ticked Findings (plus the Tailoring, if any). The page lists its Placeholders, shows the rewritten CV with the Placeholders in place, and offers it as a Markdown or PDF download. Errors, such as a missing API key, a scanned PDF or a refused Fabrication, appear as a one-line message on the page. Review makes the review request (and the tailor request with a Job Description); each Rewrite makes one more.

## Guidelines

Every Finding cites one of 24 Guidelines, G01 to G24, kept in one Markdown document inside the package: [`cvxpert/guidelines.md`](cvxpert/guidelines.md). Each Guideline has a title, the rule, the check applied to the CV text, and its sources (Harvard, MIT, Duke, Illinois, South Florida, Dundee and Imperial career services, the UK National Careers Service and the Europass CV instructions). The whole document goes into the review and rewrite Steps' instructions. A Finding that cites any other ID is sent back to the model once with the reason; if the second answer is still invalid, the command fails. The research behind the Guidelines is in `docs/research/cv-guidelines.md`.

| Group | Guidelines |
|---|---|
| Content and impact | G01 Describe achievements and results, not duties · G02 Quantify only with numbers the candidate supplied · G03 Be specific about what was done and how · G04 Evidence skills; don't just list them · G05 Tailor by selecting and ordering, never by adding · G06 Mirror job-posting terms only where the CV truthfully supports them · G07 Cut irrelevant, repetitive or out-of-date content |
| Language and style | G08 Start each bullet with a strong action verb · G09 Remove duty phrases · G10 Use no personal pronouns · G11 Match verb tense to whether the role is current · G12 Prefer active voice · G13 Remove self-praise; let the facts show quality · G14 Write concise phrases, not narrative · G15 Avoid slang, jargon and repetition |
| Structure and sections | G16 Include contact details at the top · G17 Give every entry an organisation, a title and dates, newest first · G18 Order sections by relevance to the reader · G19 Keep content in parseable text (limited check) |
| Consistency and accuracy | G20 Format dates, styles and grammar consistently · G21 Eliminate spelling, grammar and punctuation errors · G22 Spell out acronyms on first use · G23 Flag unexplained gaps; do not explain them · G24 Keep every claim honest and verifiable |

## Example

Real output from one live run (`deepseek/deepseek-v4.1-flash`, 2026-10-08, about $0.02) on the fictional `examples/cv.txt` with `examples/job-description.txt`. The full report is in [`examples/sample-report.md`](examples/sample-report.md).

Before (from the CV):

```
Software Developer, Brightfield Logistics (fictional)
March 2021 - Present
- Responsible for the company website and the internal booking tool.
- Worked on various tasks related to the API.
- Helped with projects for the warehouse team.
- Reports were prepared for management every month.
```

After (from the Rewrite):

```
### Software Developer, Brightfield Logistics (fictional)
March 2021 - Present
- Develop REST APIs for the internal booking tool using [language/tool], delivering [feature/result]
- Maintain the company website and internal booking tool, achieving [result]
- Prepare monthly reports for management, [result]
- Deliver [project] for the warehouse team, [result]
```

The Review behind it had 22 Findings (Overall Score 38/100), for example G09 for "Responsible for…", G12 for the passive "Reports were prepared", and G23 for the unexplained 13-month gap. The Tailoring gave a Job Match Score of 48/100 and listed PostgreSQL, CI/CD and Kubernetes as gaps rather than adding them.

This run also shows a weakness: "REST" comes from the Job Description, not the CV, and "Develop" claims more than "worked on various tasks". After this run, the rewrite Step's instructions were changed to forbid Job Description terms the CV does not contain and raised claims, and the tailor Step no longer suggests describing content in the Job Description's wording. That change has not yet been checked with a live run; the excerpt above is the record of the run before it. The number guard still cannot catch this in code, so check every Rewrite before you send it.

## Limitations

- The Overall Score and Job Match Score are the model's estimates, not measurements.
- The Fabrication check catches invented numbers in digits only (see Known gaps).
- Scanned PDFs with no extractable text are refused; there is no OCR.
- English CVs and Job Descriptions only.
- The PDF report is plain, and characters outside the bundled font (emoji, non-Latin scripts) are left out.
- Rewrite quality is not scored or iterated on; one rewrite request, plus one retry on an invented number.
- Every run sends the CV text to OpenRouter and the chosen model's provider.

## Development

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Tests use a fake model and never call OpenRouter: real model requests are disabled in `tests/conftest.py`, so no test needs network access or an API key.

### Live smoke run

`scripts/smoke.py` is an opt-in live check that makes paid requests. pytest and CI do not run it. From the repository root:

```sh
uv run python scripts/smoke.py
```

It needs an OpenRouter key with a credit limit of at most $1, set on the key in OpenRouter. Before any model call it reads the key's `limit` and `limit_remaining` from `GET https://openrouter.ai/api/v1/key`, and it refuses with one line and exit code 1 if the limit is unset or above $1, or if that request fails. It then runs both phases, keeping every Finding, on `examples/cv.txt` with `examples/job-description.txt` on the configured model, writes `examples/sample-report.md`, reads the key again and prints the spend (limit remaining before minus limit remaining after) and the limit remaining.

## Roadmap (v2, not implemented)

Out of scope for v1 (see `docs/SPEC.md`):

- DOCX output, styled PDF templates, and region-specific Guidelines.
- An evaluator-optimizer loop for Rewrite quality, and a proper-noun Fabrication guard.
- OCR for scanned PDFs.
- An HTTP API, authentication, a database, CV history, user accounts, a hosted demo, PyPI publishing, and a Docker image.
- Languages other than English.

## License

MIT, see `LICENSE`.

The bundled font, Noto Sans Regular and Bold subset to Latin, punctuation and currency characters (`cvxpert/fonts/`), is licensed under the SIL Open Font License 1.1; see `cvxpert/fonts/OFL.txt`. Runtime dependencies keep their own licences; among them, `markdown` is BSD-3-Clause and `fpdf2` is LGPL-3.0.
