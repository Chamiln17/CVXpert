"""Parse Step: deterministic text and metadata extraction from a PDF, DOCX or TXT CV."""

from pathlib import Path

import docx
import pypdf
from pydantic import BaseModel

from cvxpert.errors import ParsingError

MAX_BYTES = 10 * 1024 * 1024


class ParsedCV(BaseModel):
    text: str
    metadata: dict[str, str]


def _pdf_text(path: Path) -> str:
    return "\n\n".join(
        page.extract_text() or "" for page in pypdf.PdfReader(path).pages
    )


def _docx_text(path: Path) -> str:
    return "\n".join(
        paragraph.text for paragraph in docx.Document(str(path)).paragraphs
    )


def _txt_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


_READERS = {".pdf": _pdf_text, ".docx": _docx_text, ".txt": _txt_text}


def parse_cv(path: Path) -> ParsedCV:
    """Return the CV's text; raise ParsingError with a one-line reason otherwise."""
    reader = _READERS.get(path.suffix.lower())
    if reader is None:
        raise ParsingError(
            f"Unsupported file type '{path.suffix}' for {path.name}; use PDF, DOCX or TXT"
        )
    if not path.is_file():
        raise ParsingError(f"CV not found: {path}")
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise ParsingError(f"{path.name} is larger than 10 MB")
    try:
        text = reader(path)
    except Exception as e:
        raise ParsingError(f"Could not read {path.name}: {e}") from e
    if not text.strip():
        if path.suffix.lower() == ".pdf":
            raise ParsingError(
                f"{path.name} has no extractable text (a scanned PDF?); supply a text-based PDF, DOCX or TXT"
            )
        raise ParsingError(f"{path.name} contains no text")
    return ParsedCV(
        text=text,
        metadata={
            "file_name": path.name,
            "file_type": path.suffix.lower().lstrip("."),
            "file_size": str(size),
        },
    )
