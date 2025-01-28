import pytest
from server import app
from modules.data_types import ModelAlias


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "model",
    [
        "anthropic:claude-3-5-haiku-latest",
        "anthropic:claude-3-haiku-20240307",
        "anthropic:claude-3-5-sonnet-20241022",
        "gemini:gemini-1.5-pro-002",
        "gemini:gemini-1.5-flash-002",
        "gemini:gemini-1.5-flash-8b-latest",
        "openai:gpt-4o-mini",
        "openai:gpt-4o",
        "openai:gpt-4o-predictive",
        "openai:gpt-4o-mini-predictive",
    ],
)
def test_prompt(client, model):
    response = client.post("/prompt", json={"prompt": "ping", "model": model})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


@pytest.mark.parametrize(
    "prompt,expected_tool_calls,model",
    [
        (
            "Write code in main.py. Next, git commit that change.",
            ["run_coder_agent", "run_git_agent"],
            "openai:gpt-4o",
        ),
        ("Write some code", ["run_coder_agent"], "openai:gpt-4o-mini"),
        ("Document this feature", ["run_docs_agent"], "openai:gpt-4o"),
    ],
)
def test_tool_prompt(client, prompt, expected_tool_calls, model):
    response = client.post(
        "/tool-prompt",
        json={
            "prompt": prompt,
            "expected_tool_calls": expected_tool_calls,
            "model": model,
        },
    )

    assert response.status_code == 200
    data = response.get_json()

    # Verify response structure
    assert "tool_calls" in data
    assert "runTimeMs" in data
    assert "inputAndOutputCost" in data

    # Verify tool calls
    assert isinstance(data["tool_calls"], list)
    assert len(data["tool_calls"]) == len(expected_tool_calls)

    # Verify each tool call
    for tool_call in data["tool_calls"]:
        assert isinstance(tool_call, dict)
        assert "tool_name" in tool_call
        assert "params" in tool_call
        assert tool_call["tool_name"] in expected_tool_calls
        assert isinstance(tool_call["params"], dict)
        assert len(tool_call["params"]) > 0

    # Verify timing and cost
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


def test_thought_bench_ollama(client):
    """Test thought bench endpoint with Ollama DeepSeek model"""
    response = client.post(
        "/thought-prompt",
        json={
            "prompt": "What is the capital of France?",
            "model": "ollama:deepseek-r1:8b",
        },
    )

    assert response.status_code == 200
    data = response.get_json()

    assert "thoughts" in data
    assert "response" in data
    assert data["model"] == "ollama:deepseek-r1:8b"
    assert "paris" in data["response"].lower()
    assert not data["error"]


def test_thought_bench_deepseek(client):
    """Test thought bench endpoint with DeepSeek Reasoner model"""
    response = client.post(
        "/thought-prompt",
        json={
            "prompt": "What is the capital of France?",
            "model": "deepseek:deepseek-reasoner",
        },
    )

    assert response.status_code == 200
    data = response.get_json()

    assert "thoughts" in data
    assert "response" in data
    assert data["model"] == "deepseek:deepseek-reasoner"
    assert "paris" in data["response"].lower()
    assert not data["error"]
