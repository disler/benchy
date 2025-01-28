from typing import Optional, Union
from pydantic import BaseModel
from enum import Enum


class ModelAlias(str, Enum):
    haiku = "claude-3-5-haiku-latest"
    haiku_3_legacy = "claude-3-haiku-20240307"
    sonnet = "claude-3-5-sonnet-20241022"
    gemini_pro_2 = "gemini-1.5-pro-002"
    gemini_flash_2 = "gemini-1.5-flash-002"
    gemini_flash_8b = "gemini-1.5-flash-8b-latest"
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"
    gpt_4o_predictive = "gpt-4o-predictive"
    gpt_4o_mini_predictive = "gpt-4o-mini-predictive"

    # JSON variants
    o1_mini_json = "o1-mini-json"
    gpt_4o_json = "gpt-4o-json"
    gpt_4o_mini_json = "gpt-4o-mini-json"
    gemini_pro_2_json = "gemini-1.5-pro-002-json"
    gemini_flash_2_json = "gemini-1.5-flash-002-json"
    sonnet_json = "claude-3-5-sonnet-20241022-json"
    haiku_json = "claude-3-5-haiku-latest-json"
    gemini_exp_1114_json = "gemini-exp-1114-json"

    # ollama models
    llama3_2_1b = "llama3.2:1b"
    llama_3_2_3b = "llama3.2:latest"
    qwen_2_5_coder_14b = "qwen2.5-coder:14b"
    qwq_3db = "qwq:32b"
    phi_4 = "vanilj/Phi-4:latest"


class Prompt(BaseModel):
    prompt: str
    model: Union[ModelAlias, str]


class ToolEnum(str, Enum):
    run_coder_agent = "run_coder_agent"
    run_git_agent = "run_git_agent"
    run_docs_agent = "run_docs_agent"


class ToolAndPrompt(BaseModel):
    tool_name: ToolEnum
    prompt: str


class ToolsAndPrompts(BaseModel):
    tools_and_prompts: list[ToolAndPrompt]


class PromptWithToolCalls(BaseModel):
    prompt: str
    model: ModelAlias | str


class PromptResponse(BaseModel):
    response: str
    runTimeMs: int
    inputAndOutputCost: float


class SimpleToolCall(BaseModel):
    tool_name: str
    params: dict


class ToolCallResponse(BaseModel):
    tool_calls: list[SimpleToolCall]
    runTimeMs: int
    inputAndOutputCost: float


class ThoughtResponse(BaseModel):
    thoughts: str
    response: str
    error: Optional[str] = None


# ------------ Execution Evaluator Benchmarks ------------


class BenchPromptResponse(BaseModel):
    response: str
    tokens_per_second: float
    provider: str
    total_duration_ms: float
    load_duration_ms: float
    errored: Optional[bool] = None


class ModelProvider(str, Enum):
    ollama = "ollama"
    mlx = "mlx"


class ExeEvalType(str, Enum):
    execute_python_code_with_num_output = "execute_python_code_with_num_output"
    execute_python_code_with_string_output = "execute_python_code_with_string_output"
    raw_string_evaluator = "raw_string_evaluator"  # New evaluator type


class ExeEvalBenchmarkInputRow(BaseModel):
    dynamic_variables: Optional[dict]
    expectation: str


class ExecEvalBenchmarkFile(BaseModel):
    base_prompt: str
    evaluator: ExeEvalType
    prompts: list[ExeEvalBenchmarkInputRow]
    benchmark_name: str
    purpose: str
    models: list[str]  # List of model names/aliases


class ExeEvalBenchmarkOutputResult(BaseModel):
    prompt_response: BenchPromptResponse
    execution_result: str
    expected_result: str
    input_prompt: str
    model: str
    correct: bool
    index: int


class ExecEvalBenchmarkCompleteResult(BaseModel):
    benchmark_file: ExecEvalBenchmarkFile
    results: list[ExeEvalBenchmarkOutputResult]

    @property
    def correct_count(self) -> int:
        return sum(1 for result in self.results if result.correct)

    @property
    def incorrect_count(self) -> int:
        return len(self.results) - self.correct_count

    @property
    def accuracy(self) -> float:
        return self.correct_count / len(self.results)


class ExecEvalBenchmarkModelReport(BaseModel):
    model: str  # Changed from ModelAlias to str
    results: list[ExeEvalBenchmarkOutputResult]

    correct_count: int
    incorrect_count: int
    accuracy: float

    average_tokens_per_second: float
    average_total_duration_ms: float
    average_load_duration_ms: float


class ExecEvalBenchmarkReport(BaseModel):
    benchmark_name: str
    purpose: str
    models: list[ExecEvalBenchmarkModelReport]

    overall_correct_count: int
    overall_incorrect_count: int
    overall_accuracy: float

    average_tokens_per_second: float
    average_total_duration_ms: float
    average_load_duration_ms: float
