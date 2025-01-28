import time
from contextlib import contextmanager
from typing import Generator
from modules.data_types import ModelAlias


@contextmanager
def timeit() -> Generator[None, None, float]:
    """
    Context manager to measure execution time in milliseconds.

    Usage:
        with timeit() as t:
            # code to time
        elapsed_ms = t()

    Returns:
        Generator that yields None and returns elapsed time in milliseconds
    """
    start = time.perf_counter()
    yield lambda: int((time.perf_counter() - start) * 1000)


MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS = {
    ModelAlias.gpt_4o_mini: {
        "input": 0.15,
        "output": 0.60,
    },
    ModelAlias.o1_mini_json: {
        "input": 3.00,
        "output": 15.00,
    },
    ModelAlias.haiku_3_legacy: {
        "input": 0.25,
        "output": 1.25,
    },
    ModelAlias.gpt_4o: {
        "input": 2.50,
        "output": 10.00,
    },
    ModelAlias.gpt_4o_predictive: {
        "input": 2.50,
        "output": 10.00,
    },
    ModelAlias.gpt_4o_mini_predictive: {
        "input": 0.15,
        "output": 0.60,
    },
    ModelAlias.haiku: {
        "input": 1.00,
        "output": 5.00,
    },
    ModelAlias.sonnet: {
        "input": 3.00,
        "output": 15.00,
    },
    ModelAlias.gemini_pro_2: {
        "input": 1.25,
        "output": 5.00,
    },
    ModelAlias.gemini_exp_1114_json: {
        "input": 1.25,
        "output": 5.00,
    },
    ModelAlias.gemini_flash_2: {
        "input": 0.075,
        "output": 0.300,
    },
    ModelAlias.gemini_flash_8b: {
        "input": 0.0375,
        "output": 0.15,
    },
    # JSON variants with same pricing as base models
    ModelAlias.gpt_4o_json: {
        "input": 2.50,
        "output": 10.00,
    },
    ModelAlias.gpt_4o_mini_json: {
        "input": 0.15,
        "output": 0.60,
    },
    ModelAlias.gemini_pro_2_json: {
        "input": 1.25,
        "output": 5.00,
    },
    ModelAlias.gemini_flash_2_json: {
        "input": 0.075,
        "output": 0.300,
    },
    ModelAlias.sonnet_json: {
        "input": 3.00,
        "output": 15.00,
    },
    ModelAlias.haiku_json: {
        "input": 1.00,
        "output": 5.00,
    },
    ModelAlias.llama3_2_1b: {
        "input": 0.00,
        "output": 0.00,
    },
    ModelAlias.llama_3_2_3b: {
        "input": 0.00,
        "output": 0.00,
    },
    ModelAlias.qwen_2_5_coder_14b: {
        "input": 0.00,
        "output": 0.00,
    },
    ModelAlias.qwq_3db: {
        "input": 0.00,
        "output": 0.00,
    },
    ModelAlias.phi_4: {
        "input": 0.00,
        "output": 0.00,
    },
    "deepseek-chat": {
        "input": 0.14,
        "output": 0.28,
    },
    "o1-mini": {
        "input": 3.00,
        "output": 15.00,
    },
    "o1-preview": {
        "input": 15.00,
        "output": 60.00,
    },
    "o1": {
        "input": 15.00,
        "output": 60.00,
    },
    "gemini-2.0-flash-exp": {
        "input": 0.00,
        "output": 0.00,
    },
}


def parse_markdown_backticks(str) -> str:
    if "```" not in str:
        return str.strip()
    # Remove opening backticks and language identifier
    str = str.split("```", 1)[-1].split("\n", 1)[-1]
    # Remove closing backticks
    str = str.rsplit("```", 1)[0]
    # Remove any leading or trailing whitespace
    return str.strip()


def deepseek_r1_distil_separate_thoughts_and_response(response: str, xml_tag: str = "think") -> tuple[str, str]:
    """
    Parse DeepSeek R1 responses containing <think> blocks and separate thoughts from final response.
    
    Args:
        response: Raw model response string
        xml_tag: XML tag to look for (default: 'think')
        
    Returns:
        tuple: (thoughts, response) where:
            - thoughts: concatenated content from all <think> blocks
            - response: cleaned response with <think> blocks removed
    """
    import re
    from io import StringIO
    import logging
    
    thoughts = []
    cleaned_response = response
    
    try:
        # Find all think blocks using regex (more fault-tolerant than XML parsing)
        pattern = re.compile(rf'<{xml_tag}>(.*?)</{xml_tag}>', re.DOTALL)
        matches = pattern.findall(response)
        
        if matches:
            # Extract and clean thoughts
            thoughts = [m.strip() for m in matches]
            
            # Remove think blocks from response
            cleaned_response = pattern.sub('', response).strip()
            
            # Remove any remaining XML tags if they exist
            cleaned_response = re.sub(r'<\/?[a-zA-Z]+>', '', cleaned_response).strip()
            
        return '\n\n'.join(thoughts), cleaned_response
        
    except Exception as e:
        logging.error(f"Error parsing DeepSeek R1 response: {str(e)}")
        # Fallback - return empty thoughts and full response
        return '', response.strip()
