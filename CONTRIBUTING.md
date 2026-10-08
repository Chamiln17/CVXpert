# Contributing

Thank you for helping. Small, focused pull requests are easiest to review.

## Set up

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

All four must pass before a pull request is merged; CI runs the same commands.

## Ground rules

- **Tests never call a real model.** They use PydanticAI's fake models, and real model requests are disabled in `tests/conftest.py`. Do not add tests that need an API key or network access.
- **Test behaviour, not wording.** Drive tests through the Pipeline (`cvxpert.pipeline`), the CLI or the web page, and assert on what a user sees.
- **No Fabrication.** Any change to the rewrite Step must keep the rule that a Rewrite never adds a fact the CV does not contain. See `GLOSSARY.md` for the project's terms and `docs/SPEC.md` for the v1 behaviour.
- **Guidelines need sources.** A new or changed Guideline cites at least one reputable source (university career services, official career guidance). See `docs/research/cv-guidelines.md`.
- **The README only describes what runs.**

## Pull requests

1. Open an issue first for anything larger than a bug fix, so we can agree on the approach.
2. Branch from `main`, keep one topic per pull request, and describe what changed and how you tested it.
3. Do not commit `.env`, API keys, or real CVs. Use fictional data like `examples/cv.txt`.

By contributing you agree that your contribution is licensed under the project's MIT licence and that you follow the [Code of Conduct](CODE_OF_CONDUCT.md).
