"""Errors a candidate sees; each message is one line that says what to change."""


class CVXpertError(Exception):
    """Base class for every expected failure of the Pipeline."""


class ConfigurationError(CVXpertError):
    """Settings are missing or invalid."""


class ParsingError(CVXpertError):
    """The CV file cannot be turned into text."""


class StepError(CVXpertError):
    """An LLM Step did not return a valid result."""


class FabricationError(StepError):
    """The Rewrite kept a number, percentage or year that the CV does not contain."""


def one_line(e: Exception) -> str:
    """The error's message on one line, as every caller shows it."""
    return " ".join(str(e).split()) or type(e).__name__
