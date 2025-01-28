import pytest
from modules.ollama_llm import text_prompt, bench_prompt


def test_ollama_text_prompt():
    response = text_prompt("ping", "llama3.2:1b")
    assert response.response != ""
    assert response.runTimeMs > 0  # Now checking that timing is captured
    assert response.inputAndOutputCost == 0.0


def test_qwen_text_prompt():
    response = text_prompt("ping", "qwen2.5-coder:14b")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost == 0.0


def test_llama_3_2_latest_text_prompt():
    response = text_prompt("ping", "llama3.2:latest")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost == 0.0


def test_phi_4_text_prompt():
    response = text_prompt("ping", "phi4:latest")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost == 0.0


@pytest.mark.parametrize(
    "model",
    [
        "qwen2.5-coder:14b",
        "llama3.2:1b",
        "llama3.2:latest",
        "phi4:latest",
    ],
)
def test_bench_prompt_metrics(model):
    response = bench_prompt("ping", model)

    # Test that all metrics are being extracted correctly
    assert response.response != ""
    assert response.tokens_per_second > 0
    assert response.provider == "ollama"
    assert response.total_duration_ms > 0
    assert response.load_duration_ms > 0

    # Test that the metrics are within reasonable ranges
    assert 0 < response.tokens_per_second < 1000  # tokens/s should be in this range
    assert (
        response.load_duration_ms < response.total_duration_ms
    )  # load time should be less than total time


def test_valid_xml_parsing():
    from modules.ollama_llm import thought_prompt
    from modules.data_types import ThoughtResponse
    from utils import deepseek_r1_distil_separate_thoughts_and_response

    # Test with valid XML structure
    test_response = """<think>
This is test reasoning content
</think>

Final response here"""

    thoughts, response = deepseek_r1_distil_separate_thoughts_and_response(
        test_response
    )

    assert thoughts == "This is test reasoning content"
    assert response == "Final response here"


def test_missing_xml_handling():
    from modules.ollama_llm import thought_prompt
    from modules.data_types import ThoughtResponse
    from utils import deepseek_r1_distil_separate_thoughts_and_response

    # Test response without XML tags
    test_response = "Simple response without any XML formatting"

    thoughts, response = deepseek_r1_distil_separate_thoughts_and_response(
        test_response
    )

    assert thoughts == ""
    assert response == test_response
