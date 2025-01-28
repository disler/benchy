import { reactive } from "vue";
import { allTools } from "../utils";

function loadDefaultState() {
    return {
        isLoading: false,
        promptResponses: [] as ToolCallResponse[],
        userInput: "# Call one tool for each task.\n\n1. Write code to update main.py with a new cli arg 'fmode'",
        expectedToolCalls: ["run_coder_agent"],
        total_executions: 0,
        activeTab: "toolcall",
        jsonPrompt: `<purpose>
    Given the tool-call-prompt, generate the result in the specified json-output-format. 
    Create a list of the tools and prompts that will be used in the tool-call-prompt. The tool_name MUST BE one of the tool-name-options.
</purpose>

<json-output-format>
{
    tools_and_prompts: [
        {
            tool_name: "tool name 1",
            prompt: "tool call prompt 1"
        },
        {
            tool_name: "tool name 2",
            prompt: "tool call prompt 2"
        },
        {
            tool_name: "tool name 3",
            prompt: "tool call prompt 3"
        }
    ]
}
</json-output-format>

<tool-name-options>
    ${allTools.map(tool => `"${tool}"`).join(", ")}
</tool-name-options>

<tool-call-prompt>
{{tool_call_prompt}}
</tool-call-prompt>`,

        rowData: [
            {
                model: "openai:gpt-4o-mini",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "openai:gpt-4o",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "anthropic:claude-3-5-sonnet-20241022",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "gemini:gemini-1.5-pro-002",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "gemini:gemini-1.5-flash-002",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "anthropic:claude-3-haiku-20240307",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "openai:gpt-4o-mini-json",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "openai:gpt-4o-json",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "anthropic:claude-3-5-sonnet-20241022-json",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "gemini:gemini-1.5-pro-002-json",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "gemini:gemini-1.5-flash-002-json",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "anthropic:claude-3-5-haiku-latest-json",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "openai:o1-mini-json",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            },
            {
                model: "gemini:gemini-exp-1114-json",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
            }
        ] as ToolCallRowData[],
    };
}


function loadState() {
    const savedState = localStorage.getItem('toolCallState');
    if (savedState) {
        try {
            return JSON.parse(savedState);
        } catch (e) {
            console.error('Failed to parse saved state:', e);
            return loadDefaultState();
        }
    }
    return loadDefaultState();
}

export function resetState() {
    const defaultState = loadDefaultState();
    setState(defaultState);
    localStorage.setItem('toolCallState', JSON.stringify(store));
}

function setState(state: any) {
    store.isLoading = state.isLoading;
    store.promptResponses = state.promptResponses;
    store.userInput = state.userInput;
    store.expectedToolCalls = state.expectedToolCalls;
    store.activeTab = state.activeTab;
    store.rowData = state.rowData;
    store.total_executions = state.total_executions;
    store.jsonPrompt = state.jsonPrompt;
}

export const store = reactive(loadState());
