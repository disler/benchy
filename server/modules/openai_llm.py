import openai
import os
import json
from modules.tools import openai_tools_list
from modules.data_types import SimpleToolCall, ToolsAndPrompts
from utils import parse_markdown_backticks, timeit, parse_reasoning_effort
from modules.data_types import (
    PromptResponse,
    ModelAlias,
    ToolCallResponse,
    BenchPromptResponse,
)
from utils import MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS
from modules.tools import all_tools_list
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

openai_client: openai.OpenAI = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# reasoning_effort_enabled_models = [
#     "o3-mini",
#     "o1",
# ]


def get_openai_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the cost for OpenAI API usage.

    Args:
        model: The model name/alias used
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        float: Total cost in dollars
    """
    # Direct model name lookup first
    model_alias = model

    # Only do special mapping for gpt-4 variants
    if "gpt-4" in model:
        if model == "gpt-4o-mini":
            model_alias = ModelAlias.gpt_4o_mini
        elif model == "gpt-4o":
            model_alias = ModelAlias.gpt_4o
        else:
            model_alias = ModelAlias.gpt_4o

    cost_map = MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS.get(model_alias)
    if not cost_map:
        print(f"No cost map found for model: {model}")
        return 0.0

    input_cost = (input_tokens / 1_000_000) * float(cost_map["input"])
    output_cost = (output_tokens / 1_000_000) * float(cost_map["output"])

    # print(
    #     f"model: {model}, input_cost: {input_cost}, output_cost: {output_cost}, total_cost: {input_cost + output_cost}, total_cost_rounded: {round(input_cost + output_cost, 6)}"
    # )

    return round(input_cost + output_cost, 6)


def tool_prompt(prompt: str, model: str, force_tools: list[str]) -> ToolCallResponse:
    """
    Run a chat model forcing specific tool calls.
    Now supports JSON structured output variants.
    """
    base_model, reasoning_effort = parse_reasoning_effort(model)
    with timeit() as t:
        if base_model == "o1-mini-json":
            # Manual JSON parsing for o1-mini
            completion = openai_client.chat.completions.create(
                model="o1-mini",
                messages=[{"role": "user", "content": prompt}],
            )

            try:
                # Parse raw response text into ToolsAndPrompts model
                parsed_response = ToolsAndPrompts.model_validate_json(
                    parse_markdown_backticks(completion.choices[0].message.content)
                )
                tool_calls = [
                    SimpleToolCall(
                        tool_name=tap.tool_name.value, params={"prompt": tap.prompt}
                    )
                    for tap in parsed_response.tools_and_prompts
                ]
            except Exception as e:
                print(f"Failed to parse JSON response: {e}")
                tool_calls = []

        elif "-json" in base_model:
            # Use structured output for JSON variants
            completion = openai_client.beta.chat.completions.parse(
                model=base_model.replace("-json", ""),
                messages=[{"role": "user", "content": prompt}],
                response_format=ToolsAndPrompts,
            )

            try:
                tool_calls = [
                    SimpleToolCall(
                        tool_name=tap.tool_name.value, params={"prompt": tap.prompt}
                    )
                    for tap in completion.choices[0].message.parsed.tools_and_prompts
                ]
            except Exception as e:
                print(f"Failed to parse JSON response: {e}")
                tool_calls = []

        else:
            # Original implementation for function calling
            completion = openai_client.chat.completions.create(
                model=base_model,
                messages=[{"role": "user", "content": prompt}],
                tools=openai_tools_list,
                tool_choice="required",
            )

            tool_calls = [
                SimpleToolCall(
                    tool_name=tool_call.function.name,
                    params=json.loads(tool_call.function.arguments),
                )
                for tool_call in completion.choices[0].message.tool_calls or []
            ]

    # Calculate costs
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens
    cost = get_openai_cost(model, input_tokens, output_tokens)

    return ToolCallResponse(
        tool_calls=tool_calls, runTimeMs=t(), inputAndOutputCost=cost
    )


def bench_prompt(prompt: str, model: str) -> BenchPromptResponse:
    """
    Send a prompt to OpenAI and get detailed benchmarking response.
    """
    base_model, reasoning_effort = parse_reasoning_effort(model)
    try:
        with timeit() as t:
            if reasoning_effort:
                completion = openai_client.chat.completions.create(
                    model=base_model,
                    reasoning_effort=reasoning_effort,
                    messages=[{"role": "user", "content": prompt}],
                    stream=False,
                )
            else:
                completion = openai_client.chat.completions.create(
                    model=base_model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=False,
                )
            elapsed_ms = t()

            input_tokens = completion.usage.prompt_tokens
            output_tokens = completion.usage.completion_tokens
            cost = get_openai_cost(base_model, input_tokens, output_tokens)

        return BenchPromptResponse(
            response=completion.choices[0].message.content,
            tokens_per_second=0.0,  # OpenAI doesn't provide timing info
            provider="openai",
            total_duration_ms=elapsed_ms,
            load_duration_ms=0.0,
            inputAndOutputCost=cost,
        )
    except Exception as e:
        print(f"OpenAI error: {str(e)}")
        return BenchPromptResponse(
            response=f"Error: {str(e)}",
            tokens_per_second=0.0,
            provider="openai",
            total_duration_ms=0.0,
            load_duration_ms=0.0,
            inputAndOutputCost=0.0,
            errored=True,
        )


def predictive_prompt(prompt: str, prediction: str, model: str) -> PromptResponse:
    """
    Run a chat model with a predicted output to reduce latency.

    Args:
        prompt (str): The prompt to send to the OpenAI API.
        prediction (str): The predicted output text.
        model (str): The model ID to use for the API call.

    Returns:
        PromptResponse: The response including text, runtime, and cost.
    """
    base_model, reasoning_effort = parse_reasoning_effort(model)
    # Prepare the API call parameters outside the timing block
    messages = [{"role": "user", "content": prompt}]
    prediction_param = {"type": "content", "content": prediction}

    # Only time the actual API call
    with timeit() as t:
        completion = openai_client.chat.completions.create(
            model=base_model,
            reasoning_effort=reasoning_effort,
            messages=messages,
            prediction=prediction_param,
        )

    # Process results after timing block
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens
    cost = get_openai_cost(base_model, input_tokens, output_tokens)

    return PromptResponse(
        response=completion.choices[0].message.content,
        runTimeMs=t(),  # Get the elapsed time of just the API call
        inputAndOutputCost=cost,
    )


def text_prompt(prompt: str, model: str) -> PromptResponse:
    """
    Send a prompt to OpenAI and get a response.
    """
    base_model, reasoning_effort = parse_reasoning_effort(model)
    try:
        with timeit() as t:
            if reasoning_effort:
                completion = openai_client.chat.completions.create(
                    model=base_model,
                    reasoning_effort=reasoning_effort,
                    messages=[{"role": "user", "content": prompt}],
                )
            else:
                completion = openai_client.chat.completions.create(
                    model=base_model,
                    messages=[{"role": "user", "content": prompt}],
                )
            print("completion.usage", completion.usage.model_dump())
            input_tokens = completion.usage.prompt_tokens
            output_tokens = completion.usage.completion_tokens
            cost = get_openai_cost(base_model, input_tokens, output_tokens)

        return PromptResponse(
            response=completion.choices[0].message.content,
            runTimeMs=t(),
            inputAndOutputCost=cost,
        )
    except Exception as e:
        print(f"OpenAI error: {str(e)}")
        return PromptResponse(
            response=f"Error: {str(e)}", runTimeMs=0.0, inputAndOutputCost=0.0
        )
