global {
    export type RowStatus = 'idle' | 'loading' | 'success' | 'error';

    export interface SimpleToolCall {
        tool_name: string;
        params: any;
    }

    export interface ToolAndPrompt {
        tool_name: string;
        prompt: string;
    }

    export interface ToolsAndPrompts {
        tools_and_prompts: ToolAndPrompt[];
    }

    export interface ToolCallResponse {
        tool_calls: SimpleToolCall[];
        runTimeMs: number;
        inputAndOutputCost: number;
    }

    export interface ToolCallRowData {
        model: ModelAlias;
        status: RowStatus;
        toolCalls: SimpleToolCall[] | null;
        execution_time: number | null;
        execution_cost: number | null;
        total_cost: number;
        total_execution_time: number;
        relativePricePercent: number;
        number_correct: number;
        percent_correct: number;
    }

    export interface RowData {
        completion: string;
        model: ModelAlias;
        correct: boolean | null;
        execution_time: number | null;
        execution_cost: number | null;
        total_cost: number;
        total_execution_time: number;
        relativePricePercent: number;
        number_correct: number;
        percent_correct: number;
        status: RowStatus;
    }

    export interface SimpleToolCall {
        tool_name: string;
        params: any;
    }

    export interface ToolCallResponse {
        tool_calls: SimpleToolCall[];
        runTimeMs: number;
        inputAndOutputCost: number;
    }

    export interface ToolCallRowData {
        model: ModelAlias;
        status: RowStatus;
        toolCalls: SimpleToolCall[] | null;
        execution_time: number | null;
        execution_cost: number | null;
        total_cost: number;
        total_execution_time: number;
        relativePricePercent: number;
    }

    export type IsoBenchAward =
        'fastest' |   // model completed all prompts first
        'slowest' |   // model completed all prompts last
        'most_accurate' |   // highest accuracy
        'least_accurate' |   // lowest accuracy
        'perfection';  // 100% accuracy

    export type ModelAlias =
        | "claude-3-5-haiku-latest"
        | "claude-3-haiku-20240307"
        | "claude-3-5-sonnet-20241022"
        | "gemini-1.5-pro-002"
        | "gemini-1.5-flash-002"
        | "gemini-1.5-flash-8b-latest"
        | "gpt-4o-mini"
        | "gpt-4o"
        | "gpt-4o-predictive"
        | "gpt-4o-mini-predictive"
        | "gpt-4o-json"
        | "gpt-4o-mini-json"
        | "gemini-1.5-pro-002-json"
        | "gemini-1.5-flash-002-json"
        | "claude-3-5-sonnet-20241022-json"
        | "claude-3-5-haiku-latest-json"
        | "o1-mini-json"
        | "gemini-exp-1114-json"
        | "llama3.2:1b"
        | "llama3.2:latest"
        | "qwen2.5-coder:14b"
        | "qwq:32b"
        | "vanilj/Phi-4:latest"
        | string;

    export interface PromptRequest {
        prompt: string;
        model: ModelAlias;
    }

    export interface PromptResponse {
        response: string;
        runTimeMs: number;
        inputAndOutputCost: number;
    }
}

export interface ExecEvalBenchmarkReport {
    benchmark_name: string;
    purpose: string;
    models: ExecEvalBenchmarkModelReport[];
    overall_correct_count: number;
    overall_incorrect_count: number;
    overall_accuracy: number;
    average_tokens_per_second: number;
    average_total_duration_ms: number;
    average_load_duration_ms: number;
}

export interface ExecEvalBenchmarkModelReport {
    model: string;
    results: ExecEvalBenchmarkOutputResult[];
    correct_count: number;
    incorrect_count: number;
    accuracy: number;
    average_tokens_per_second: number;
    average_total_duration_ms: number;
    average_load_duration_ms: number;
}

export interface BenchPromptResponse {
    response: string;
    tokens_per_second: number;
    provider: string;
    total_duration_ms: number;
    load_duration_ms: number;
    errored: boolean | null;
}

export interface ExecEvalBenchmarkOutputResult {
    prompt_response: BenchPromptResponse;
    execution_result: string;
    expected_result: string;
    input_prompt: string;
    model: string;
    correct: boolean;
    index: number;
}

export interface ThoughtResponse {
    thoughts: string;
    response: string;
    error?: string;
}

export type ThoughtBenchColumnState = 'idle' | 'loading' | 'success' | 'error';

export interface ThoughtBenchColumnData {
    model: string;
    totalCorrect: number;
    responses: ThoughtResponse[];
    state: ThoughtBenchColumnState;
}

export { };
