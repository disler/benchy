import { reactive, watch } from "vue";
import { ExecEvalBenchmarkReport } from "../types";
import { inMemoryBenchmarkReport } from "./data/isoSpeedBenchDemoOutput";

interface IsoSpeedBenchState {
    isLoading: boolean;
    benchmarkReport: ExecEvalBenchmarkReport | null;
    currentTime: number;
    intervalId: number | null;
    isReplaying: boolean;
    completedResults: Set<string>;
    settings: {
        benchMode: boolean;
        speed: number;
        scale: number;
        modelStatDetail: 'verbose' | 'simple' | 'hide';
        showProviderPrefix: boolean;
    };
}

const store = reactive<IsoSpeedBenchState>({
    isLoading: false,
    benchmarkReport: null,
    currentTime: 0,
    intervalId: null,
    isReplaying: false,
    completedResults: new Set(),
    settings: {
        benchMode: false,
        speed: 50,
        scale: 150,
        modelStatDetail: 'verbose',
        showProviderPrefix: false
    }
});

function saveSettings() {
    localStorage.setItem('isoSpeedBenchSettings', JSON.stringify(store.settings));
}

function loadSettings() {
    const savedSettings = localStorage.getItem('isoSpeedBenchSettings');
    if (savedSettings) {
        try {
            Object.assign(store.settings, JSON.parse(savedSettings));
        } catch (e) {
            console.error('Failed to load settings:', e);
        }
    }
}

// Load settings when store is initialized
loadSettings();

// Automatically save settings when they change
watch(() => store.settings, (newSettings) => {
    // saveSettings();
}, { deep: true });


function resetBenchmark() {
    store.currentTime = 0;
    store.completedResults.clear();
    store.isReplaying = false;
    if (store.intervalId) {
        clearInterval(store.intervalId);
        store.intervalId = null;
    }
}

function startBenchmark() {
    resetBenchmark();
    store.isReplaying = true;
    store.currentTime = 0;

    const tickRate = Math.min(50, store.settings.speed);

    store.intervalId = setInterval(() => {
        // Increment the global timer by tickRate
        store.currentTime += tickRate;

        // Check each model to see if it should complete its next result
        store.benchmarkReport?.models.forEach(modelReport => {
            const currentIndex = Array.from(store.completedResults)
                .filter(key => key.startsWith(modelReport.model + '-'))
                .length;

            // If we still have results to process
            if (currentIndex < modelReport.results.length) {
                // Calculate cumulative time up to this result
                const cumulativeTime = modelReport.results
                    .slice(0, currentIndex + 1)
                    .reduce((sum, result) => sum + result.prompt_response.total_duration_ms, 0);

                // If we've reached or passed the time for this result
                if (store.currentTime >= cumulativeTime) {
                    const resultKey = `${modelReport.model}-${currentIndex}`;
                    store.completedResults.add(resultKey);
                }
            }
        });

        // Check if all results are complete
        const allComplete = store.benchmarkReport?.models.every(modelReport =>
            store.completedResults.size >= modelReport.results.length * store.benchmarkReport!.models.length
        );

        if (allComplete) {
            if (store.intervalId) {
                clearInterval(store.intervalId);
                store.intervalId = null;
                store.isReplaying = false;
            }
        }
    }, tickRate);
}



export {
    store,
    resetBenchmark,
    startBenchmark,
    inMemoryBenchmarkReport,
};
