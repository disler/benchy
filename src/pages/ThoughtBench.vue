<template>
  <div class="container">
    <h1 v-if="store.settings.modelStatDetail !== 'hide'">Thought Bench</h1>

    <div
      class="benchmark-info"
      v-if="store.settings.modelStatDetail !== 'hide'"
    >
      <p>
        Analyze models reasoning processes and response quality through thought
        visualization.
      </p>
    </div>

    <div class="controls">
      <button
        @click="runBenchmark"
        :disabled="store.apiCallInProgress || isAnyColumnLoading"
      >
        {{ runButtonText }}
      </button>
      <button @click="clickResetState">Reset</button>
      <button @click="showSettings = !showSettings">
        {{ showSettings ? "Hide" : "Show" }} Settings
      </button>

      <div v-if="showSettings" class="settings-row">
        <div class="setting">
          <label>Model Stats:</label>
          <select v-model="store.settings.modelStatDetail">
            <option value="verbose">Verbose</option>
            <option value="hide">Hide</option>
          </select>
        </div>
        <div class="setting">
          <label>Column Height:</label>
          <input
            type="range"
            v-model.number="store.settings.columnHeight"
            min="100"
            max="1500"
            class="slider"
          />
          <span>{{ store.settings.columnHeight }}px</span>
        </div>
        <div class="setting">
          <label>Column Width:</label>
          <input
            type="range"
            v-model.number="store.settings.columnWidth"
            min="200"
            max="1500"
            class="slider"
          />
          <span>{{ store.settings.columnWidth }}px</span>
        </div>
        <div class="setting">
          <label>Display:</label>
          <select v-model="store.settings.columnDisplay">
            <option value="both">Both Sections</option>
            <option value="thoughts">Only Thoughts</option>
            <option value="response">Only Response</option>
          </select>
        </div>
      </div>
    </div>

    <div class="prompt-area">
      <textarea
        v-model="store.prompt"
        @keydown.ctrl.enter.prevent="runBenchmark"
        @keydown.meta.enter.prevent="runBenchmark"
        placeholder="Enter your reasoning prompt..."
        class="prompt-input"
      ></textarea>

      <div class="model-input-container">
        <div class="model-pills">
          <div
            v-for="model in store.dataColumns"
            :key="model.model"
            class="model-pill"
            :style="{
              backgroundColor: stringToColor(model.model),
              borderColor: isSoloed(model.model) ? '#0e4491' : 'transparent',
            }"
          >
            <span class="model-name">{{ model.model }}</span>
            <div class="pill-controls">
              <span
                class="solo-icon"
                @click="toggleSolo(model.model)"
                :title="
                  isSoloed(model.model) ? 'Show all models' : 'Solo this model'
                "
              >
                {{ isSoloed(model.model) ? "👀" : "👁️" }}
              </span>
              <span
                class="delete-icon"
                @click="removeModel(model.model)"
                title="Remove model"
              >
                🗑️
              </span>
            </div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem">
          <input
            v-model="store.newModel"
            @keyup.enter="addModel"
            placeholder="Add model (provider:model-name)"
            class="model-input"
          />
          <button @click="addModel" class="add-model-button">Add</button>
        </div>
      </div>
    </div>

    <div class="response-grid">
      <ThoughtColumn
        v-for="(column, index) in filteredColumns"
        :key="index"
        :columnData="column"
        :columnHeight="store.settings.columnHeight"
        @retry="runSingleBenchmark(column.model)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { stringToColor } from "../utils";
import { store, resetState } from "../stores/thoughtBenchStore";

// Add reset handler
function clickResetState() {
  resetState();
  soloedModels.value = [];
}
import ThoughtColumn from "../components/thought_bench/ThoughtColumn.vue";
import { runThoughtPrompt } from "../apis/thoughtBenchApi";

const showSettings = ref(false);
const soloedModels = ref<string[]>([]);
function toggleSolo(model: string) {
  const index = soloedModels.value.indexOf(model);
  if (index === -1) {
    soloedModels.value.push(model);
  } else {
    soloedModels.value = [];
  }
}

function isSoloed(model: string) {
  return soloedModels.value.includes(model);
}

const filteredColumns = computed(() => {
  if (soloedModels.value.length === 0) return store.dataColumns;
  return store.dataColumns.filter((c) => soloedModels.value.includes(c.model));
});

function removeModel(model: string) {
  const index = store.dataColumns.findIndex((c) => c.model === model);
  if (index !== -1) {
    store.dataColumns.splice(index, 1);
  }
  const soloIndex = soloedModels.value.indexOf(model);
  if (soloIndex !== -1) {
    soloedModels.value.splice(soloIndex, 1);
  }
}

const isAnyColumnLoading = computed(() =>
  store.dataColumns.some((c) => c.state === "loading")
);

const runButtonText = computed(() => {
  if (store.apiCallInProgress) {
    const runningCount = store.dataColumns.filter(
      (c) => c.state === "loading"
    ).length;
    return `Running (${runningCount}/${store.dataColumns.length})`;
  }
  return "Thought Prompt";
});

function addModel() {
  if (!store.newModel.trim()) return;

  // Validate model format
  if (!store.newModel.includes(":")) {
    alert('Model must be in format "provider:model-name"');
    return;
  }

  // Check for duplicates
  if (store.dataColumns.some((c) => c.model === store.newModel)) {
    alert("Model already exists in benchmark");
    return;
  }

  store.dataColumns.push({
    model: store.newModel.trim(),
    totalCorrect: 0,
    responses: [],
    state: "idle",
  });

  store.newModel = "";
}

async function runBenchmark() {
  if (store.apiCallInProgress || isAnyColumnLoading.value) return;

  store.apiCallInProgress = true;
  try {
    const promises = store.dataColumns.map((column) =>
      runSingleBenchmark(column.model)
    );
    await Promise.allSettled(promises);
  } finally {
    store.apiCallInProgress = false;
  }
}

async function runSingleBenchmark(model: string) {
  const column = store.dataColumns.find((c) => c.model === model);
  if (!column || column.state === "loading") return;

  try {
    column.state = "loading";
    store.totalExecutions++;
    const response = await runThoughtPrompt({
      prompt: store.prompt,
      model: model,
    });

    column.responses.unshift(response);
    if (!response.error) column.totalCorrect++;
    column.state = "success";
  } catch (error) {
    console.error(`Error running benchmark for ${model}:`, error);
    column.responses.unshift({
      thoughts: "",
      response: `Error: ${(error as Error).message}`,
      error: (error as Error).message,
    });
    column.state = "error";
  } finally {
    column.state = "idle";
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 95vw;
  min-width: 70vw;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #0e4491 0%, #00d4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
  margin-bottom: 1rem;
}

.benchmark-info {
  margin-bottom: 2rem;
  text-align: center;
  color: #666;
}

.prompt-area {
  margin: 2rem 0;
}

.prompt-input {
  width: calc(100% - 2rem);
  height: 150px;
  padding: 1rem;
  border: 2px solid #ccc;
  border-radius: 8px;
  font-family: monospace;
  resize: vertical;
}

.response-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}

.controls {
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.settings-row {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
  margin-top: 1rem;
}

.setting {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.slider {
  width: 100px;
}

button {
  padding: 0.5rem 1rem;
  background: #e0e0e0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #d0d0d0;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background: #f0f0f0;
}

button:disabled:hover {
  background: #f0f0f0;
}

.model-pills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.model-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  border: 2px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
}

.model-pill:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.model-name {
  font-size: 0.9rem;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.pill-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.solo-icon,
.delete-icon {
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.solo-icon:hover,
.delete-icon:hover {
  opacity: 1;
}

.delete-icon {
  color: #ff4444;
}

.prompt-input:focus {
  outline: 2px solid #0e4491;
}

/* New styles for model input */
.model-input-container {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  margin-top: 1rem;
}

.model-input {
  padding: 0.5rem;
  border: 2px solid #ccc;
  border-radius: 4px;
  width: 300px;
}

.add-model-button {
  padding: 0.5rem 1rem;
  background: #0e4491;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.add-model-button:hover {
  background: #0d3a7d;
}
</style>
