"""Tokenisation edge cases of the Unverified Term check, awkward to reach through the
Pipeline."""

import pytest

from cvxpert.steps import unverified_terms

CV = """\
Jane Doe
Software Developer, Brightfield Logistics, March 2019 - 2021
Experience
- Built the booking website in Javascript and Node.js.
"""


@pytest.mark.parametrize(
    ("rewrite", "terms"),
    [
        ("Built the REST services.", ["REST"]),
        ("Set up CI/CD for the website.", ["CI/CD"]),
        (
            "Hosted it on Amazon Web Services and Kubernetes.",
            ["Amazon Web Services", "Kubernetes"],
        ),
        ("Wrote it in C++, C# and Python3.", ["C++", "C#", "Python3"]),
        ("Used Kubernetes, then Kubernetes again.", ["Kubernetes"]),  # no repeats
        ("Promoted to Senior Developer.", ["Senior Developer"]),  # a title,
    ],
)
def test_terms_absent_from_the_cv_are_flagged(rewrite, terms):
    assert unverified_terms(rewrite, CV) == terms


@pytest.mark.parametrize(
    "rewrite",
    [
        "Built the website in JavaScript and node.js.",  # case-insensitive
        "Led a [Team Size] team, [Result].",  # Placeholders
        "Software Developer, Brightfield Logistics, Mar 2019 to Sept 2021",  # months
        "## Work Experience\n\n### Skills\n\n## Professional Summary",  # Section names
        "- Delivered the booking website. Shipped it on time.",  # first words
        "1. **Designed** the booking website.",  # list marker and emphasis
        "Software Developer at Brightfield Logistics",  # a name the CV contains
    ],
)
def test_cv_terms_and_markdown_structure_are_not_flagged(rewrite):
    assert unverified_terms(rewrite, CV) == []


def test_text_allowed_beyond_the_cv_is_not_flagged():
    assert (
        unverified_terms("Ran PostgreSQL and CI/CD.", CV + "\nPostgreSQL\nCI/CD") == []
    )
