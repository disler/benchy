import { reactive } from "vue";

function loadDefaultState() {


    return {
        isLoading: false,
        promptResponses: [] as PromptResponse[],
        userInput: "",
        total_executions: 0,
        activeTab: "benchmark",

        basePrompt: `# Provide an autocomplete suggestion given the following Completion Content and Input Text

## Instructions
- Respond only with your top single suggestion and nothing else.
- Your autocompletion will replace the last word of the input text.
- For example, if the input text is "We need to analy", and there is a word "analyze_user_expenses", then your autocomplete should be "analyze_user_expenses".
- If no logical completion can be made based on the last word, then return the text 'none'.

## Completion Content

def calculate_total_price(items, tax_rate):
    pass
    
def calculate_discount(price, discount_rate):
    pass

def validate_user_input(data):
    pass
    
def process_payment(amount):
    pass

def analyze_user_expenses(transactions):
    pass

def analyze_user_transactions(transactions):
    pass

def generate_invoice(order_details):
    pass

def update_inventory(product_id, quantity):
    pass

def send_notification(user_id, message):
    pass

## Input text
'{input_text}'
        `,
        rowData: [
            {
                completion: "",
                model: "anthropic:claude-3-5-haiku-latest",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "anthropic:claude-3-5-sonnet-20241022",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "gemini:gemini-1.5-pro-002",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "gemini:gemini-1.5-flash-002",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "gemini:gemini-1.5-flash-8b-latest",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "openai:gpt-4o-mini",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "openai:gpt-4o",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "openai:gpt-4o-predictive",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "openai:gpt-4o-mini-predictive",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "ollama:llama3.2:1b",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "ollama:qwen2.5-coder:14b",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "ollama:llama3.2:latest",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "ollama:vanilj/Phi-4:latest",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "gemini:gemini-2.0-flash-exp",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "openai:o1-mini",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "openai:o1-preview",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "openai:o1",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "deepseek:deepseek-chat",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "deepseek:deepseek-reasoner",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "ollama:phi4:latest",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
            {
                completion: "",
                model: "ollama:falcon3:10b",
                correct: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
                number_correct: 0,
                percent_correct: 0,
                status: 'idle',
            },
        ] as RowData[]
    };
}


function loadState() {
    const savedState = localStorage.getItem('appState');
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

// Function to reset state to default
export function resetState() {
    const defaultState = loadDefaultState();
    setState(defaultState);
    localStorage.setItem('appState', JSON.stringify(store));
}

function setState(state: any) {
    store.isLoading = state.isLoading;
    store.promptResponses = state.promptResponses;
    store.userInput = state.userInput;
    store.activeTab = state.activeTab;
    store.basePrompt = state.basePrompt;
    store.rowData = state.rowData;
    store.defaultRowData = state.rowData;
    store.total_executions = state.total_executions;
}

export function calculatePercentCorrect(numberCorrect: number): number {
    if (store.total_executions === 0 || numberCorrect === 0) return 0;
    const percent = Math.round((numberCorrect / store.total_executions) * 100);
    return Math.max(0, Math.min(100, percent));
}

export function handleCorrect(model: ModelAlias, isCorrect: boolean) {
    const rowIndex = store.rowData.findIndex((row: RowData) => row.model === model);
    if (rowIndex === -1) return;

    const row = store.rowData[rowIndex];

    // Calculate new number_correct value
    let newNumberCorrect = row.number_correct;
    if (isCorrect) {
        newNumberCorrect = Math.min(row.number_correct + 1, store.total_executions);
    } else {
        newNumberCorrect = Math.max(0, row.number_correct - 1);
    }

    console.log("newNumberCorrect", newNumberCorrect);
    console.log("calculatePercentCorrect", calculatePercentCorrect(newNumberCorrect));

    const updatedRow = {
        ...row,
        correct: isCorrect,
        number_correct: newNumberCorrect,
        percent_correct: calculatePercentCorrect(newNumberCorrect)
    };

    store.rowData.splice(rowIndex, 1, updatedRow);
}

export const store = reactive(loadState());
