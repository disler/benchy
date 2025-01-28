<template>
  <dialog ref="dialogRef">
    <div class="modal-content">
      <header :class="{ correct: result.correct, incorrect: !result.correct }">
        <h2>
          {{ formatModelName(result.model) }} - Prompt #{{ result.index }}
        </h2>
        <span class="status">{{
          result.correct ? "Correct" : "Incorrect"
        }}</span>
      </header>

      <section class="metrics">
        <div class="metric">
          <span>Tokens/Second:</span>
          <span>{{ result.prompt_response.tokens_per_second.toFixed(2) }}</span>
        </div>
        <div class="metric">
          <span>Total Duration:</span>
          <span
            >{{ result.prompt_response.total_duration_ms.toFixed(2) }}ms</span
          >
        </div>
        <div class="metric">
          <span>Load Duration:</span>
          <span
            >{{ result.prompt_response.load_duration_ms.toFixed(2) }}ms</span
          >
        </div>
      </section>

      <div class="result-sections">
        <section>
          <h3>Input Prompt</h3>
          <textarea readonly>{{ result.input_prompt }}</textarea>
        </section>

        <section>
          <h3>Model Response</h3>
          <textarea readonly>{{ result.prompt_response.response }}</textarea>
        </section>

        <section class="results-comparison">
          <div class="result-col">
            <h3>Expected Result</h3>
            <textarea readonly>{{ result.expected_result }}</textarea>
          </div>
          <div class="result-col">
            <h3>Execution Result</h3>
            <textarea readonly>{{ result.execution_result }}</textarea>
          </div>
        </section>
      </div>

      <footer>
        <button @click="closeDialog" autofocus>Close</button>
      </footer>
    </div>
  </dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { store } from "../../stores/isoSpeedBenchStore";

function formatModelName(modelName: string): string {
  if (!store.settings.showProviderPrefix && modelName.includes("~")) {
    return modelName.split("~")[1];
  }
  return modelName;
}

const props = defineProps<{
  result: ExecEvalBenchmarkOutputResult;
}>();

const dialogRef = ref<HTMLDialogElement | null>(null);

function showDialog() {
  dialogRef.value?.showModal();
}

function closeDialog() {
  dialogRef.value?.close();
}

defineExpose({
  showDialog,
  closeDialog,
});
</script>

<style scoped>
dialog {
  padding: 0;
  border: none;
  border-radius: 8px;
  max-width: 90vw;
  width: 80vw;
  height: 90vh;
}

dialog::backdrop {
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

header.correct {
  background-color: #4caf5022;
}

header.incorrect {
  background-color: #f4433622;
}

header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.status {
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.correct .status {
  background-color: #4caf50;
  color: white;
}

.incorrect .status {
  background-color: #f44336;
  color: white;
}

.result-sections {
  padding: 1rem;
  overflow-y: auto;
  flex: 1;
}

section {
  margin-bottom: 1.5rem;
}

h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #666;
}

textarea {
  width: 95%;
  min-height: 200px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f8f8f8;
  font-family: monospace;
  font-size: 0.9rem;
  resize: vertical;
}

.results-comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  background-color: #f8f8f8;
  padding: 1rem;
  border-radius: 4px;
}

.metric {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}
.metric span:first-child {
  font-weight: bold;
}

footer {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

button {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  background-color: #e0e0e0;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #d0d0d0;
}
</style>
