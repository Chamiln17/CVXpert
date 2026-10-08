"""The Guidelines G01-G24: one cited Markdown document shipped in the package."""

import re
from functools import cache
from importlib.resources import files
from typing import NamedTuple


class Guideline(NamedTuple):
    id: str
    title: str
    rule: str
    sources: list[str]


NEEDS_JOB = ("G05", "G06")  # Guidelines that need a target job


def guidelines_text() -> str:
    """The full Guidelines document, as injected into Step instructions."""
    return files("cvxpert").joinpath("guidelines.md").read_text(encoding="utf-8")


_ENTRY = re.compile(
    r"^\*\*(G\d{2}): (.+?)\.\*\*.*?^Rule: (.+?)$.*?^Sources: (.+?)$", re.M | re.S
)


@cache
def load_guidelines() -> dict[str, Guideline]:
    """Guidelines by ID, in document order."""
    return {
        gid: Guideline(gid, title, rule, [s.strip() for s in sources.split(";")])
        for gid, title, rule, sources in _ENTRY.findall(guidelines_text())
    }


def id_range() -> str:
    """The catalogue's ID range as text, e.g. "G01 to G24"."""
    ids = list(load_guidelines())
    return f"{ids[0]} to {ids[-1]}"
