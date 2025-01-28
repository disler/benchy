import pytest
from modules.deepseek_llm import text_prompt, bench_prompt
from modules.data_types import BenchPromptResponse, PromptResponse


def test_deepseek_text_prompt():
    response = text_prompt("ping", "deepseek-chat")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost > 0.0


def test_deepseek_bench_prompt():
    response = bench_prompt("ping", "deepseek-chat")
    assert isinstance(response, BenchPromptResponse)
    assert response.response != ""
    assert response.total_duration_ms > 0
    assert response.provider == "deepseek"
    assert not response.errored


def test_deepseek_error_handling():
    # Test with invalid model name
    response = text_prompt("ping", "invalid-model")
    assert "Error" in response.response
    assert response.runTimeMs == 0
    assert response.inputAndOutputCost == 0.0

    # Test bench prompt error handling
    response = bench_prompt("ping", "invalid-model")
    assert "Error" in response.response
    assert response.total_duration_ms == 0
    assert response.errored

def test_thought_prompt_happy_path():
    from modules.deepseek_llm import thought_prompt
    from modules.data_types import ThoughtResponse
    
    # Test with valid model and mock response
    response = thought_prompt("What is the capital of France?", "deepseek-reasoner")
    
    assert isinstance(response, ThoughtResponse)
    assert response.thoughts != ""
    assert response.response != ""
    assert not response.error
    assert "Paris" in response.response  # Basic sanity check

def test_thought_prompt_missing_thoughts():
    from modules.deepseek_llm import thought_prompt
    from modules.data_types import ThoughtResponse
    
    # Test error handling for invalid model
    response = thought_prompt("test", "invalid-model")
    
    assert isinstance(response, ThoughtResponse)
    assert "Error" in response.thoughts
    assert response.error
