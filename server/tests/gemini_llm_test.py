import pytest
from modules.gemini_llm import text_prompt


def test_gemini_text_prompt():
    response = text_prompt("ping", "gemini-1.5-pro-002")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost > 0.0


def test_gemini_thought_prompt():
    from modules.gemini_llm import thought_prompt
    from modules.data_types import ThoughtResponse

    # Test with valid model
    response = thought_prompt(
        "code: python: code only: def every_n_chars(string, n) -> str",
        "gemini-2.0-flash-thinking-exp-01-21",
    )

    assert isinstance(response, ThoughtResponse)
    assert response.thoughts != ""
    assert response.response != ""
    assert not response.error
    assert "def" in response.response  # Basic sanity check


def test_gemini_thought_prompt_invalid_model():
    from modules.gemini_llm import thought_prompt
    from modules.data_types import ThoughtResponse

    # Test with invalid model
    response = thought_prompt(
        "Explain how RLHF works in simple terms", "gemini-1.5-pro-002"
    )

    assert isinstance(response, ThoughtResponse)
    assert "Error" in response.thoughts
    assert response.error
