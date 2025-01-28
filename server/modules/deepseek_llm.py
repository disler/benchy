from openai import OpenAI
from utils import MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS, timeit
from modules.data_types import BenchPromptResponse, PromptResponse, ThoughtResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)


def get_deepseek_cost(model: str, input_tokens: int, output_tokens: int) -> float:
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


def bench_prompt(prompt: str, model: str) -> BenchPromptResponse:
    """
    Send a prompt to DeepSeek and get detailed benchmarking response.
    """
    try:
        with timeit() as t:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=False,
            )
            elapsed_ms = t()

        return BenchPromptResponse(
            response=response.choices[0].message.content,
            tokens_per_second=0.0,  # DeepSeek doesn't provide this info
            provider="deepseek",
            total_duration_ms=elapsed_ms,
            load_duration_ms=0.0,
        )
    except Exception as e:
        print(f"DeepSeek error: {str(e)}")
        return BenchPromptResponse(
            response=f"Error: {str(e)}",
            tokens_per_second=0.0,
            provider="deepseek",
            total_duration_ms=0.0,
            load_duration_ms=0.0,
            errored=True,
        )


def text_prompt(prompt: str, model: str) -> PromptResponse:
    """
    Send a prompt to DeepSeek and get the response.
    """
    try:
        with timeit() as t:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=False,
            )
            elapsed_ms = t()
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = get_deepseek_cost(model, input_tokens, output_tokens)

        return PromptResponse(
            response=response.choices[0].message.content,
            runTimeMs=elapsed_ms,
            inputAndOutputCost=cost,
        )
    except Exception as e:
        print(f"DeepSeek error: {str(e)}")
        return PromptResponse(
            response=f"Error: {str(e)}",
            runTimeMs=0.0,
            inputAndOutputCost=0.0,
        )

def thought_prompt(prompt: str, model: str) -> ThoughtResponse:
    """
    Send a thought prompt to DeepSeek and parse structured response.
    """
    try:
        # Validate model
        if model != "deepseek-reasoner":
            raise ValueError(f"Invalid model for thought prompts: {model}. Must use 'deepseek-reasoner'")

        # Make API call with reasoning_content=True
        with timeit() as t:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                extra_body={"reasoning_content": True},  # Enable structured reasoning
                stream=False,
            )
            elapsed_ms = t()

        # Extract content and reasoning
        message = response.choices[0].message
        thoughts = getattr(message, "reasoning_content", "")
        response_content = message.content

        # Validate required fields
        if not thoughts or not response_content:
            raise ValueError("Missing thoughts or response in API response")

        # Calculate costs
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = get_deepseek_cost("deepseek-reasoner", input_tokens, output_tokens)

        return ThoughtResponse(
            thoughts=thoughts,
            response=response_content,
            error=None,
        )

    except Exception as e:
        print(f"DeepSeek thought error: {str(e)}")
        return ThoughtResponse(
            thoughts=f"Error processing request: {str(e)}",
            response="",
            error=str(e)
        )
