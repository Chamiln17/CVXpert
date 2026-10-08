# Agentic architecture for the CVXpert pipeline

Retrieved 2026-10-08. All sources are primary: official docs, PyPI pages, or source on GitHub `master`/`main` as of that date. LangChain and PydanticAI source was read from the default branch, not a tagged release.

## Question

The v1 pipeline is a fixed linear chain: parse (pypdf/python-docx, no LLM), then review (LLM), then tailor (LLM, only if a JD is given), then rewrite (LLM). Each LLM step returns a typed Pydantic object, the provider is OpenRouter, the rewriter must never invent facts, and tests must run with fake model responses. Should the pipeline use a LangGraph `StateGraph`, plain async function calls, the OpenAI Agents SDK, PydanticAI, or something else?

## Summary recommendation

Write the pipeline as plain async Python functions, one per step, and use a PydanticAI `Agent` with `output_type=<PydanticModel>` for each LLM step. Remove `langgraph`, `langchain` and `langchain-openai` from `pyproject.toml` and add `pydantic-ai-slim[openrouter]` (2.54.0 on PyPI). Call OpenRouter through `OpenRouterModel`/`OpenRouterProvider` with `openrouter_provider={'require_parameters': True}`. Testing uses PydanticAI's `FunctionModel`, which returns hand-written outputs, so rewrite tests control the exact text, plus `Agent.override(model=...)` and `models.ALLOW_MODEL_REQUESTS = False` so a test can never reach the paid API. Anthropic's guidance calls this pattern "prompt chaining" and says to start with direct API calls and add frameworks only when needed. LangGraph describes itself as built for "long-running, stateful agents", and this pipeline is neither. If the project keeps LangChain, the minimum change is to swap `ChatOpenAI(base_url=...)` for `langchain-openrouter`'s `ChatOpenRouter`, which the `ChatOpenAI` source itself recommends. Under that option, the stock LangChain fake chat models cannot exercise `.with_structured_output()`.

## Findings per source

### 1. Anthropic, "Building effective agents"
URL: https://www.anthropic.com/engineering/building-effective-agents
- **Workflows vs agents.** Workflows are "systems where LLMs and tools are orchestrated through predefined code paths". In agents, "LLMs dynamically direct their own processes and tool usage". CVXpert's fixed review, tailor and rewrite chain matches the first definition.
- **Complexity.** The article advises finding "the simplest solution possible, and only increasing complexity when needed", and adds: "This might mean not building agentic systems at all."
- **Frameworks.** Frameworks "often create extra layers of abstraction that can obscure the underlying prompts". The article says: "We suggest that developers start by using LLM APIs directly."
- **Prompt chaining** "decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one". It is "ideal for situations where the task can be easily and cleanly decomposed into fixed subtasks." This describes the v1 pipeline.
- **Routing** "classifies an input and directs it to a specialized followup task". The tailor step's condition, whether a JD was given, is a plain `if` on the input and needs no LLM router.
- **Evaluator-optimizer.** In this pattern, "one LLM call generates a response while another provides evaluation and feedback in a loop". It is "particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value." This is the v2 candidate described below.

### 2. LangGraph
- **Version.** PyPI lists `langgraph` 1.2.14, released Oct 6, 2026, requiring Python >=3.10 (https://pypi.org/project/langgraph/). The repo currently pins `langgraph>=0.0.15`.
- **Positioning.** PyPI describes LangGraph as "a low-level orchestration framework for building, managing, and deploying long-running, stateful agents", with durable execution, streaming, human-in-the-loop and persistence. The overview (https://docs.langchain.com/oss/python/langgraph/overview) calls it "very low-level, and focused entirely on agent orchestration" and sends beginners to LangChain agents. It also states that LangGraph "can be used without LangChain".
- **StateGraph API** (https://docs.langchain.com/oss/python/langgraph/graph-api): `from langgraph.graph import END, START, StateGraph`. The state schema can be a `TypedDict` ("the main documented way"), a `dataclass`, or a Pydantic `BaseModel`, but "Pydantic is less performant than a `TypedDict` or `dataclass`". The builder methods are `add_node(name, fn)`, `add_edge(START, ...)`, and `add_conditional_edges(node, router, mapping)`, and `compile()` is mandatory ("You **MUST** compile your graph before you can use it"). The page shows `invoke`. `ainvoke` belongs to the Runnable interface and is not covered on that page.
- **Testing** (https://docs.langchain.com/oss/python/langgraph/test): the page recommends a fresh graph per test, compiling with `MemorySaver`/`InMemorySaver`, testing single nodes via `compiled_graph.nodes["node1"].invoke(...)`, and partial runs with `update_state(as_node=...)`. It does not mention fake models.
- **LangChain fake chat models and structured output** (source, `master`). `langchain_core/language_models/fake_chat_models.py` defines `FakeMessagesListChatModel`, `FakeListChatModel`, `FakeChatModel`, `GenericFakeChatModel` and `ParrotFakeChatModel`. None of them override `bind_tools`. `BaseChatModel.with_structured_output` in `chat_models.py` begins with `if type(self).bind_tools is BaseChatModel.bind_tools:` and raises `NotImplementedError("with_structured_output is not implemented for this model.")`. As a result, **`GenericFakeChatModel(...).with_structured_output(Schema)` raises**, and testing that path needs a custom fake subclass or a seam above the LLM call.

### 3. PydanticAI
- **Version.** PyPI lists `pydantic-ai` 2.54.0, released Oct 3, 2026, with Python >=3.10 (https://pypi.org/project/pydantic-ai/). `pydantic-ai-slim` is also 2.54.0 (PyPI JSON API).
- **OpenRouter** (https://pydantic.dev/docs/ai/models/openrouter/). Install with `pip install "pydantic-ai-slim[openrouter]"`. The classes are `OpenRouterModel` (`pydantic_ai.models.openrouter`) and `OpenRouterProvider` (`pydantic_ai.providers.openrouter`), the key comes from the `OPENROUTER_API_KEY` env var, and the shorthand is `Agent('openrouter:<model>')`. In the source, `OpenRouterProviderConfig` has `require_parameters: bool`, passed as `OpenRouterModelSettings(openrouter_provider=...)` (pydantic-ai `main`, `pydantic_ai_slim/pydantic_ai/models/openrouter.py`).
- **Structured output** (https://pydantic.dev/docs/ai/core-concepts/output/). The default mode is Tool Output: the schema is sent as an output tool, which the docs say "has been shown to work very well" and is supported by virtually all models. `NativeOutput` uses the provider's JSON-schema response format, and `PromptedOutput` puts the schema in the prompt and is the least reliable. `@agent.output_validator` can raise `ModelRetry` to request a new output. The retry budget defaults to 1 and is set with `Agent(retries={'output': N})`.
- **Testing** (https://pydantic.dev/docs/ai/guides/testing/). `TestModel` produces schema-valid data; its output "won't look pretty or relevant, but it should pass Pydantic's validation in most cases". `FunctionModel` is a user function that returns a `ModelResponse`. `Agent.override(model=...)` swaps the model without touching call sites, `ALLOW_MODEL_REQUESTS = False` exists so tests don't "accidentally make real requests to the LLM", and `capture_run_messages()` records the exchange.

### 4. OpenRouter
- **Structured outputs** (https://openrouter.ai/docs/features/structured-outputs). Requests use `response_format: {type: "json_schema", json_schema: {name, strict, schema}}`. With "`strict: true`", "providers with a native strict mode enforce your schema exactly". Support is "determined per endpoint, not just per model", so the same model can behave differently by host. Setting "`require_parameters: true` in your provider preferences" restricts routing to endpoints that support the parameters sent. The page does not describe a tool-calling fallback.
- **Finding models** (https://openrouter.ai/docs/guides/overview/models). `GET https://openrouter.ai/api/v1/models` returns `supported_parameters`, documented as the "Array of supported API parameters for this model". Listed values include `tools`, `tool_choice`, `structured_outputs` and `response_format`. The documented filter example is `?supported_parameters=tools`.
- **Tool-calling fallback.** Any fallback happens on the client side. PydanticAI's default `ToolOutput` needs only `tools` support, and LangChain offers `method="function_calling"`. The OpenRouter tool-calling URL tried (`/docs/features/tool-calling`) returned 404.
- **Spending ceiling.** Per the provisioning docs (https://openrouter.ai/docs/guides/overview/auth/provisioning-api-keys), API keys carry an optional `limit` ("Optional credit limit") with `limit_reset` (daily, weekly or monthly). `GET https://openrouter.ai/api/v1/key` returns `limit` and `limit_remaining`, and `null` means unlimited (https://openrouter.ai/docs/api/reference/limits). Create the CVXpert key with a `limit` set.
- **LangChain against OpenRouter.** The `ChatOpenAI` docstring (langchain `master`, `libs/partners/openai/langchain_openai/chat_models/base.py`) says it targets "official OpenAI API specifications only" and that when "pointing `base_url` at a provider such as OpenRouter ... use the corresponding provider-specific LangChain package instead (e.g., ... `ChatOpenRouter`)". `ChatOpenAI.with_structured_output` (class `ChatOpenAI`, line ~3858) defaults to `method="json_schema"`. The same file's error text suggests `method="function_calling"` when a model rejects `json_schema`. `langchain-openrouter` 0.2.9 (Sep 22, 2026, maintained by "langchain", https://pypi.org/project/langchain-openrouter/) provides `from langchain_openrouter import ChatOpenRouter`, and its structured output defaults to `function_calling`, with `json_schema` available (https://docs.langchain.com/oss/python/integrations/chat/openrouter).

### 5. OpenAI Agents SDK
URL: https://openai.github.io/openai-agents-python/models/
- Non-OpenAI models are reached through `OpenAIChatCompletionsModel` with a custom `AsyncOpenAI(base_url=...)`, or through LiteLLM and Any-LLM (both beta).
- Caveats:
  - Tracing uploads to OpenAI, so without an OpenAI key you get 401s unless tracing is disabled.
  - Many providers lack the Responses API, so Chat Completions has to be forced.
  - Some providers reject a JSON schema and accept only basic JSON mode.
- Fit: the SDK is built around agent loops, handoffs and tools, and a linear pipeline on OpenRouter would use none of them while taking on these caveats. It is not a fit.

## Comparison

| Option | Deps added (net) | Structured output on OpenRouter | Testability with fakes | Fit for linear 3-step chain |
|---|---|---|---|---|
| Plain async + PydanticAI | `pydantic-ai-slim[openrouter]`; drop langgraph, langchain, langchain-openai | First-class `OpenRouterModel`. Default ToolOutput needs `tools`; `NativeOutput` needs `structured_outputs`; `require_parameters` supported | Strong: `FunctionModel`, `TestModel`, `Agent.override`, `ALLOW_MODEL_REQUESTS=False` | Best. Matches Anthropic "prompt chaining" with direct-call simplicity |
| LangGraph StateGraph + ChatOpenAI(base_url) (current plan) | langgraph, langchain-core, langchain-openai | The `ChatOpenAI` docstring itself says to use `ChatOpenRouter` for OpenRouter; defaults to `json_schema` | Weak: stock fakes raise on `with_structured_output`; needs a custom fake or a seam | Over-built. Graph, checkpointer and persistence go unused |
| LangGraph + `langchain-openrouter` | langgraph, langchain-core, langchain-openrouter | `ChatOpenRouter`, default `function_calling` | Same fake-model gap as above | Works, but the extra layers add little |
| OpenAI Agents SDK | openai-agents (+ litellm optional) | Via Chat Completions; docs warn schema support varies | Not researched | Poor. Agent loop and tracing caveats |
| Raw `openai` SDK `.parse()` against OpenRouter | openai | UNVERIFIED (not researched) | Fake by stubbing the client | Viable, but needs hand-written retries and validation |

## Recommendation for this repo

1. **Orchestration.** Replace `cvxpert/app/core/orchestrator.py` (currently `from langgraph.graph import END, StateGraph`) with an `async def run_pipeline(cv_path, jd=None)` that awaits review, then tailor if `jd` is set, then rewrite. The function is about 15 lines and contains no graph. Anthropic's definitions call this a workflow.
2. **LLM layer.** Replace `cvxpert/app/utils/llm.py` (`langchain_openai.ChatOpenAI` + `ChatPromptTemplate`) with module-level PydanticAI agents, one per step, e.g. `Agent(model, output_type=ReviewResult, instructions=...)`. The `pydantic` output models in `cvxpert/app/agents/*.py` can stay.
3. **Dependencies** (`pyproject.toml`). Remove `langgraph`, `langchain` and `langchain-openai`, and add `pydantic-ai-slim[openrouter]>=2.54`.
4. **Model choice.** Pick a model whose `supported_parameters` includes `tools`, which the default ToolOutput needs, and set `openrouter_provider={'require_parameters': True}`. Use `NativeOutput` only if the model also lists `structured_outputs`.
5. **Tests.** Set `models.ALLOW_MODEL_REQUESTS = False` in `conftest.py`. Use `FunctionModel` to return controlled review, tailor and rewrite outputs, including a rewrite that invents a number, so the guard is exercised. Use `TestModel` only for schema smoke tests.
6. **Spend.** Create the OpenRouter key with a credit `limit`, and check `GET /api/v1/key` before any live smoke run.

## v2 patterns

- **Evaluator-optimizer** (Anthropic, above): after the rewrite, a second agent scores the rewrite against a rubric and returns typed feedback, and the rewriter retries with that feedback. Cap the loop at N iterations. The pattern fits only when the rubric is clear, which matches Anthropic's stated condition.
- **Fact-preservation guard.** This design is our proposal; no source states it. A deterministic function extracts numbers, percentages, years and capitalised tokens and phrases from the rewrite, allows placeholders matching `\[[^\]]+\]` (e.g. `[X%]`), and fails if any token is missing from the parsed source CV (and the JD for tailoring). The mechanism for wiring it in is documented: register it as `@agent.output_validator` and raise `ModelRetry("Invented: ...")` so the model gets one corrective retry (PydanticAI output docs). If the retry also fails, surface the error instead of returning the text. The guard runs on every output, costs nothing, and is unit-testable without a model. It also gives the evaluator loop its "clear evaluation criteria".

## Open risks / unverified claims

- UNVERIFIED: whether OpenRouter's `/api/v1/models?supported_parameters=structured_outputs` filter works. Only the `tools` example is documented.
- UNVERIFIED: end-to-end behaviour of PydanticAI ToolOutput and `require_parameters` against a specific OpenRouter model. No live calls were made (no paid API calls were authorised).
- UNVERIFIED: `langchain-openrouter`'s `ChatOpenRouter` structured output against OpenRouter in practice. It is documented but was not run.
- UNVERIFIED: whether `ChatOpenAI(base_url=openrouter)` with the default `json_schema` method fails for specific models. The source only warns that it targets the OpenAI spec.
- UNVERIFIED: the OpenRouter docs page on tool calling (the URL tried returned 404).
- Risk: the proper-noun heuristic will produce false positives, such as capitalised words at the start of sentences or rephrased job titles. Start with numbers and dates, and add a source-derived allowlist for names.
- Risk: PydanticAI ships often (2.54.0 on 2026-10-03). Pin a minimum version and re-run tests on upgrade.
- Decision for the user: README.md describes CVXpert as an "intelligent multi-agent system ... using LangGraph". By Anthropic's definitions the v1 design is a workflow, so for an honest portfolio the README should be reworded if LangGraph is dropped.
