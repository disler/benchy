import pytest
from modules.anthropic_llm import text_prompt

def test_anthropic_text_prompt():
    response = text_prompt("ping", "claude-3-5-haiku-latest")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost > 0.0
