import { reactive, watch } from "vue";
import type { ThoughtBenchColumnData, ThoughtBenchColumnState } from "../types";

function loadDefaultState() {
    return {
        dataColumns: [
            {
                model: "ollama:deepseek-r1:1.5b",
                totalCorrect: 0,
                responses: [],
                state: "idle" as ThoughtBenchColumnState
            },
            {
                model: "ollama:deepseek-r1:8b",
                totalCorrect: 0,
                responses: [],
                state: "idle" as ThoughtBenchColumnState
            },
            {
                model: "deepseek:deepseek-reasoner",
                totalCorrect: 0,
                responses: [],
                state: "idle" as ThoughtBenchColumnState
            },
            {
                model: "openai:o1",
                totalCorrect: 0,
                responses: [],
                state: "idle" as ThoughtBenchColumnState
            },
            {
                model: "gemini:gemini-2.0-flash-thinking-exp-01-21",
                totalCorrect: 0,
                responses: [],
                state: "idle" as ThoughtBenchColumnState
            },
        ] as ThoughtBenchColumnData[],
        prompt: "",
        newModel: "", // Add new model input field
        totalExecutions: 0,
        apiCallInProgress: false,
        settings: {
            modelStatDetail: 'verbose' as 'verbose' | 'hide',
            columnWidth: 400,
            columnHeight: 300,
            columnDisplay: 'both' as 'both' | 'thoughts' | 'response'
        }
    };
}

function loadState() {
    const savedState = localStorage.getItem('thoughtBenchState');
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
    localStorage.setItem('thoughtBenchState', JSON.stringify(store));
}

function setState(state: any) {
    store.dataColumns = state.dataColumns;
    store.prompt = state.prompt;
    store.newModel = state.newModel; // Add this line
    store.totalExecutions = state.totalExecutions;
    store.apiCallInProgress = state.apiCallInProgress;
    store.settings = state.settings;
}

export const store = reactive(loadState());

// Add automatic save watcher
watch(
    store,
    (state) => {
        localStorage.setItem('thoughtBenchState', JSON.stringify(state));
    },
    { deep: true }
);
