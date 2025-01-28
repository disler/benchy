import llm
from dotenv import load_dotenv
import os
from modules import ollama_llm
from modules.data_types import (
    ModelAlias,
    PromptResponse,
    PromptWithToolCalls,
    ToolCallResponse,
    ThoughtResponse,
)
from modules import openai_llm, gemini_llm, deepseek_llm
from utils import MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS
from modules.tools import all_tools_list
from modules import anthropic_llm

# Load environment variables from .env file
load_dotenv()


def simple_prompt(prompt_str: str, model_alias_str: str) -> PromptResponse:
    parts = model_alias_str.split(":", 1)
    if len(parts) < 2:
        raise ValueError("No provider prefix found in model string")
    provider = parts[0]
    model_name = parts[1]

    # For special predictive cases:
    if provider == "openai" and model_name in [
        "gpt-4o-predictive",
        "gpt-4o-mini-predictive",
    ]:
        # Remove -predictive suffix when passing to API
        clean_model_name = model_name.replace("-predictive", "")
        return openai_llm.predictive_prompt(prompt_str, prompt_str, clean_model_name)

    if provider == "openai":
        return openai_llm.text_prompt(prompt_str, model_name)
    elif provider == "ollama":
        return ollama_llm.text_prompt(prompt_str, model_name)
    elif provider == "anthropic":
        return anthropic_llm.text_prompt(prompt_str, model_name)
    elif provider == "gemini":
        return gemini_llm.text_prompt(prompt_str, model_name)
    elif provider == "deepseek":
        return deepseek_llm.text_prompt(prompt_str, model_name)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def tool_prompt(prompt: PromptWithToolCalls) -> ToolCallResponse:
    model_str = str(prompt.model)
    parts = model_str.split(":", 1)
    if len(parts) < 2:
        raise ValueError("No provider prefix found in model string")
    provider = parts[0]
    model_name = parts[1]

    if provider == "openai":
        return openai_llm.tool_prompt(prompt.prompt, model_name, all_tools_list)
    elif provider == "anthropic":
        return anthropic_llm.tool_prompt(prompt.prompt, model_name)
    elif provider == "gemini":
        return gemini_llm.tool_prompt(prompt.prompt, model_name, all_tools_list)
    elif provider == "deepseek":
        raise ValueError("DeepSeek does not support tool calls")
    elif provider == "ollama":
        raise ValueError("Ollama does not support tool calls")
    else:
        raise ValueError(f"Unsupported provider for tool calls: {provider}")


def thought_prompt(prompt: str, model: str) -> ThoughtResponse:
    """
    Handle thought prompt requests with specialized parsing for supported models.
    Fall back to standard text prompts for other models.
    """
    parts = model.split(":", 1)
    if len(parts) < 2:
        raise ValueError("No provider prefix found in model string")
    provider = parts[0]
    model_name = parts[1]

    try:
        if provider == "deepseek":
            if model_name != "deepseek-reasoner":
                # Fallback to standard text prompt for non-reasoner models
                text_response = simple_prompt(prompt, model)
                return ThoughtResponse(
                    thoughts="", response=text_response.response, error=None
                )

            # Proceed with reasoner-specific processing
            response = deepseek_llm.thought_prompt(prompt, model_name)
            return response

        elif provider == "gemini":
            if model_name != "gemini-2.0-flash-thinking-exp-01-21":
                # Fallback to standard text prompt for non-thinking models
                text_response = simple_prompt(prompt, model)
                return ThoughtResponse(
                    thoughts="", response=text_response.response, error=None
                )

            # Proceed with thinking-specific processing
            response = gemini_llm.thought_prompt(prompt, model_name)
            return response

        elif provider == "ollama":
            if "deepseek-r1" not in model_name:
                # Fallback to standard text prompt for non-R1 models
                text_response = simple_prompt(prompt, model)
                return ThoughtResponse(
                    thoughts="", response=text_response.response, error=None
                )

            # Proceed with R1-specific processing
            response = ollama_llm.thought_prompt(prompt, model_name)
            return response

        else:
            # For all other providers, use standard text prompt and wrap in ThoughtResponse
            text_response = simple_prompt(prompt, model)
            return ThoughtResponse(
                thoughts="", response=text_response.response, error=None
            )

    except Exception as e:
        return ThoughtResponse(
            thoughts=f"Error processing request: {str(e)}", response="", error=str(e)
        )
