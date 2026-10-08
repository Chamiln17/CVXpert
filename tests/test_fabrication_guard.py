"""Edge cases of the Fabrication guard that are awkward to reach through the Pipeline."""

import pytest

from cvxpert.steps import fabricated_numbers

CV = """\
Software Developer, Brightfield Logistics, 2019-2021
Junior Developer, 06/2018 - 02/2020
- Served 1,200 customers; cut costs by 30 %; GPA 3.80.
"""


@pytest.mark.parametrize(
    "rewrite",
    [
        "Served 1200 customers.",  # thousands separator dropped
        "Cut costs by 30%.",  # percent sign normalised
        "Brightfield Logistics, 2019 \N{EN DASH} 2021",  # year range re-spaced
        "Junior Developer, 06/2018 - 02/2020",  # dates as the CV writes them
        "GPA 3.8",  # trailing decimal zero dropped
        "1. Served customers.\n2. Cut costs.\n10) Fixed bugs.",  # numbered-list markers
        "Led a [team of 5] for [3] years.",  # digits inside Placeholders
    ],
)
def test_the_cvs_own_numbers_and_markdown_structure_pass(rewrite):
    assert fabricated_numbers(rewrite, CV) == []


def test_a_cv_number_with_a_thousands_separator_matches_the_rewrite_without_one():
    assert fabricated_numbers("Served 1,200 customers.", "Served 1200 customers.") == []


@pytest.mark.parametrize(
    ("rewrite", "invented"),
    [
        ("Served 12,000 customers.", ["12,000"]),
        ("Developer, 2019-2022", ["2022"]),
        ("Cut costs by 40% in 3 months.", ["40%", "3"]),
        ("Ranked 1. in the team", ["1"]),  # a marker only counts at a line start
        ("Junior Developer, 6/2018 - 2/2020", ["6", "2"]),  # leading zeros are kept
        ("GPA 3.08", ["3.08"]),
    ],
)
def test_numbers_absent_from_the_cv_are_reported(rewrite, invented):
    assert fabricated_numbers(rewrite, CV) == invented
