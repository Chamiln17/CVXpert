"""A fake model: PydanticAI's FunctionModel serving canned Reviews, Tailorings and
Rewrites."""

from pydantic_ai.messages import ModelMessage, ModelResponse, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel


def review_citing(*guideline_ids: str) -> dict:
    """A Review payload with one Finding per cited Guideline ID."""
    return {
        "overall_score": 58,
        "summary": "Duties instead of results; no numbers anywhere.",
        "sections": [
            {"title": "Experience", "text": "Responsible for the website."},
            {"title": "Skills", "text": "Python, teamwork"},
        ],
        "findings": [
            {
                "id": f"F{n}",
                "guideline_id": gid,
                "section": "Experience",
                "affected_text": "Responsible for the website.",
                "problem": f"Breaks {gid}.",
                "proposed_change": "Built [what] for the website, raising [result].",
                "severity": "high",
                "uncertain": False,
            }
            for n, gid in enumerate(guideline_ids, start=1)
        ],
    }


TAILORING = {
    "job_match_score": 64,
    "summary": "Strong Python fit; cloud and Docker are not shown.",
    "matches": ["Python web services"],
    "gaps": ["Docker", "AWS"],
    "emphasis": ["Move the booking API work to the top of Experience"],
}


# No digits, so it passes the Fabrication guard for any CV.
REWRITE = {"markdown": "# Jane Doe\n\n## Experience\n\n- Built [what] for the website."}


def rewrite(markdown: str) -> dict:
    return {"markdown": markdown}


def _output_fields(info: AgentInfo) -> dict:
    return info.output_tools[0].parameters_json_schema.get("properties", {})


class FakeModel(FunctionModel):
    """Serves the given Review payloads in order to the review Step, ``tailoring`` to
    the tailor Step and ``rewrites`` in order to the rewrite Step (the last one
    repeats). Records each Step's requests and the instructions the review and rewrite
    Steps saw."""

    def __init__(
        self,
        *outputs: dict,
        tailoring: dict | None = None,
        rewrites: tuple[dict, ...] = (REWRITE,),
    ):
        self.review_requests: list[list[ModelMessage]] = []
        self.instructions: list[str | None] = []  # review Step
        self.tailor_requests: list[list[ModelMessage]] = []
        self.rewrite_requests: list[list[ModelMessage]] = []
        self.rewrite_instructions: list[str | None] = []

        def respond(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
            fields = _output_fields(info)
            if "markdown" in fields:
                self.rewrite_requests.append(messages)
                self.rewrite_instructions.append(info.instructions)
                payload = rewrites[min(len(self.rewrite_requests), len(rewrites)) - 1]
            elif "job_match_score" in fields:
                self.tailor_requests.append(messages)
                assert tailoring is not None, "unexpected tailor Step request"
                payload = tailoring
            else:
                self.review_requests.append(messages)
                self.instructions.append(info.instructions)
                payload = outputs[min(len(self.review_requests), len(outputs)) - 1]
            return ModelResponse(
                parts=[ToolCallPart(info.output_tools[0].name, payload)]
            )

        super().__init__(respond)
