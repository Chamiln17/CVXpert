"""Markdown to PDF: the text a reader sees survives, including non-Latin-1 characters."""

# ruff: noqa: RUF001 (en dashes and curly quotes are the point of this test)

import io

from pypdf import PdfReader

from cvxpert.export import markdown_to_pdf


def pdf_text(data: bytes) -> str:
    return "\n".join(page.extract_text() for page in PdfReader(io.BytesIO(data)).pages)


def test_non_latin_1_text_and_placeholders_survive_into_the_pdf():
    markdown = (
        "# José Núñez\n\n"
        "**Experience**\n\n"
        "- Led the 2021–2023 rollout\n"
        "- Cut costs by [X%] for “Acme”\n"
        "- Kept *the café’s* `on–call` rota\n"
    )

    data = markdown_to_pdf(markdown)

    assert data.startswith(b"%PDF-")
    text = pdf_text(data)
    for needle in (
        "José Núñez",
        "Experience",
        "2021–2023",
        "[X%]",
        "“Acme”",
        "café’s",
        "on–call",
    ):
        assert needle in text
