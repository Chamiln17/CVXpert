# Plain-function workflow with PydanticAI, not LangGraph

CVXpert's Pipeline is a fixed chain (parse → review → tailor if a Job Description is given → rewrite), which Anthropic's "Building effective agents" calls prompt chaining: a workflow, not an agent. We write it as plain synchronous functions (both callers, the CLI and Streamlit, are synchronous), with one PydanticAI `Agent(output_type=...)` per LLM Step through `OpenRouterModel`, and removed `langgraph`, `langchain` and `langchain-openai`. LangGraph targets long-running, stateful agents and would add a graph, a state schema and persistence we never use. LangChain's `ChatOpenAI` docstring warns against pointing `base_url` at OpenRouter, and its stock fake chat models raise on `.with_structured_output()`. PydanticAI's `FunctionModel` and `ALLOW_MODEL_REQUESTS = False` give deterministic tests that cannot reach the paid API. Evidence: `docs/research/agentic-architectures.md`.

## Consequences

- The README describes CVXpert as an LLM workflow, not a multi-agent system.
- If v2 adds a loop (an evaluator-optimizer Rewrite), revisit this decision; a loop with a cap is still a few lines of plain Python.
