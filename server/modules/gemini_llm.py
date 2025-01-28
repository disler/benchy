import google.generativeai as genai
from google import genai as genai2
import os
import json
from modules.tools import gemini_tools_list
from modules.data_types import (
    PromptResponse,
    SimpleToolCall,
    ModelAlias,
    ToolsAndPrompts,
    ThoughtResponse,
)
from utils import (
    parse_markdown_backticks,
    timeit,
    MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS,
)
from modules.data_types import ToolCallResponse, BenchPromptResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_gemini_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the cost for Gemini API usage.

    Args:
        model: The model name/alias used
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        float: Total cost in dollars
    """

    cost_map = MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS.get(model)
    if not cost_map:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * cost_map["input"]
    output_cost = (output_tokens / 1_000_000) * cost_map["output"]

    return round(input_cost + output_cost, 6)


def thought_prompt(prompt: str, model: str) -> ThoughtResponse:
    """
    Handle thought prompts for Gemini thinking models.
    """
    try:
        # Validate model
        if model != "gemini-2.0-flash-thinking-exp-01-21":
            raise ValueError(
                f"Invalid model for thought prompts: {model}. Must use 'gemini-2.0-flash-thinking-exp-01-21'"
            )

        # Configure thinking model
        config = {"thinking_config": {"include_thoughts": True}}

        client = genai2.Client(
            api_key=os.getenv("GEMINI_API_KEY"), http_options={"api_version": "v1alpha"}
        )

        with timeit() as t:
            response = client.models.generate_content(
                model=model, contents=prompt, config=config
            )
            elapsed_ms = t()

            # Parse thoughts and response
            thoughts = []
            response_content = []

            for part in response.candidates[0].content.parts:
                if hasattr(part, "thought") and part.thought:
                    thoughts.append(part.text)
                else:
                    response_content.append(part.text)

        return ThoughtResponse(
            thoughts="\n".join(thoughts),
            response="\n".join(response_content),
            error=None,
        )

    except Exception as e:
        print(f"Gemini thought error: {str(e)}")
        return ThoughtResponse(
            thoughts=f"Error processing request: {str(e)}", response="", error=str(e)
        )


def text_prompt(prompt: str, model: str) -> PromptResponse:
    """
    Send a prompt to Gemini and get a response.
    """
    try:
        with timeit() as t:
            gemini_model = genai.GenerativeModel(model_name=model)
            response = gemini_model.generate_content(prompt)
            elapsed_ms = t()

            input_tokens = response._result.usage_metadata.prompt_token_count
            output_tokens = response._result.usage_metadata.candidates_token_count
            cost = get_gemini_cost(model, input_tokens, output_tokens)

        return PromptResponse(
            response=response.text,
            runTimeMs=elapsed_ms,
            inputAndOutputCost=cost,
        )
    except Exception as e:
        print(f"Gemini error: {str(e)}")
        return PromptResponse(
            response=f"Error: {str(e)}", runTimeMs=0.0, inputAndOutputCost=0.0
        )


def bench_prompt(prompt: str, model: str) -> BenchPromptResponse:
    """
    Send a prompt to Gemini and get detailed benchmarking response.
    """
    try:
        with timeit() as t:
            gemini_model = genai.GenerativeModel(model_name=model)
            response = gemini_model.generate_content(prompt)
            elapsed_ms = t()

            input_tokens = response._result.usage_metadata.prompt_token_count
            output_tokens = response._result.usage_metadata.candidates_token_count

        return BenchPromptResponse(
            response=response.text,
            tokens_per_second=0.0,  # Gemini doesn't provide timing info
            provider="gemini",
            total_duration_ms=elapsed_ms,
            load_duration_ms=0.0,
        )
    except Exception as e:
        print(f"Gemini error: {str(e)}")
        return BenchPromptResponse(
            response=f"Error: {str(e)}",
            tokens_per_second=0.0,
            provider="gemini",
            total_duration_ms=0.0,
            load_duration_ms=0.0,
            errored=True,
        )


def tool_prompt(prompt: str, model: str, force_tools: list[str]) -> ToolCallResponse:
    """
    Run a chat model with tool calls using Gemini's API.
    Now supports JSON structured output variants by parsing the response.
    """
    with timeit() as t:
        if "-json" in model:
            # Initialize model for JSON output
            base_model = model.replace("-json", "")
            if model == "gemini-exp-1114-json":
                base_model = "gemini-exp-1114"  # Map to actual model name

            gemini_model = genai.GenerativeModel(
                model_name=base_model,
            )

            # Send message and get JSON response
            chat = gemini_model.start_chat()
            response = chat.send_message(prompt)

            try:
                # Parse raw response text into ToolsAndPrompts model
                parsed_response = ToolsAndPrompts.model_validate_json(
                    parse_markdown_backticks(response.text)
                )
                tool_calls = [
                    SimpleToolCall(
                        tool_name=tap.tool_name, params={"prompt": tap.prompt}
                    )
                    for tap in parsed_response.tools_and_prompts
                ]
            except Exception as e:
                print(f"Failed to parse JSON response: {e}")
                tool_calls = []

        else:
            # Original implementation using function calling
            gemini_model = genai.GenerativeModel(
                model_name=model, tools=gemini_tools_list
            )
            chat = gemini_model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(prompt)

            tool_calls = []
            for part in response.parts:
                if hasattr(part, "function_call"):
                    fc = part.function_call
                    tool_calls.append(SimpleToolCall(tool_name=fc.name, params=fc.args))

        # Extract token counts and calculate cost
        usage_metadata = response._result.usage_metadata
        input_tokens = usage_metadata.prompt_token_count
        output_tokens = usage_metadata.candidates_token_count
        cost = get_gemini_cost(model, input_tokens, output_tokens)

    return ToolCallResponse(
        tool_calls=tool_calls, runTimeMs=t(), inputAndOutputCost=cost
    )
