"""Command line: ``cvxpert review <CV> [--job FILE [--confirm LABEL ...]] [--out PATH]
[--format md|pdf]`` and ``cvxpert web``."""

import argparse
import subprocess
import sys
from pathlib import Path

import pydantic_ai

from cvxpert import pipeline
from cvxpert.errors import CVXpertError, one_line
from cvxpert.export import markdown_to_pdf, render_report

WEB_PAGE = Path(__file__).with_name("web.py")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cvxpert")
    commands = parser.add_subparsers(dest="command", required=True)
    review = commands.add_parser(
        "review", help="Review a CV and write a Markdown or PDF report"
    )
    review.add_argument("cv", type=Path, help="CV file: PDF, DOCX or TXT")
    review.add_argument(
        "--job", type=Path, help="Job Description text file to tailor the Review to"
    )
    review.add_argument(
        "--out",
        type=Path,
        help="Report path (default: <CV name>.cvxpert.<format> next to the CV)",
    )
    review.add_argument(
        "--format",
        choices=["md", "pdf"],
        default="md",
        help="Report format (default: md)",
    )
    review.add_argument(
        "--confirm",
        action="append",
        default=[],
        metavar="LABEL",
        help="The label of a Tailoring gap that is true of you, which the Rewrite "
        "may then use (repeatable; needs --job)",
    )
    commands.add_parser("web", help="Open the Streamlit page in a browser")
    args = parser.parse_args(argv)
    if args.command == "web":
        return subprocess.call(
            [sys.executable, "-m", "streamlit", "run", str(WEB_PAGE)]
        )

    pydantic_ai.BANNER_ENABLED = False  # keep stderr to the one error line
    try:
        if args.confirm and not args.job:
            raise CVXpertError("--confirm needs --job: gaps come from the Tailoring")
        job_description = _read_job(args.job) if args.job else None
        result = pipeline.run(args.cv, job_description, args.confirm)
        report = render_report(result)
        out = args.out or args.cv.with_name(f"{args.cv.stem}.cvxpert.{args.format}")
        if args.format == "pdf":
            out.write_bytes(markdown_to_pdf(report))
        else:
            out.write_text(report, encoding="utf-8")
    except Exception as e:  # any failure: one line, non-zero exit
        sys.stderr.write(f"cvxpert: error: {one_line(e)}\n")
        return 1
    sys.stdout.write(f"Report written to {out}\n")
    return 0


def _read_job(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise CVXpertError(f"Cannot read the Job Description file '{path}': {e}") from e
    if not text.strip():
        raise CVXpertError(f"The Job Description file '{path}' is empty")
    return text


if __name__ == "__main__":
    sys.exit(main())
