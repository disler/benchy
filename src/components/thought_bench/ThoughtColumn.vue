<template>
  <div
    class="thought-column"
    :class="columnData.state"
    :style="{ width: `${store.settings.columnWidth}px` }"
  >
    <div class="column-header">
      <div
        class="provider-logo-wrapper"
        style="display: flex; align-items: center; width: 100%"
      >
        <div class="provider-logo" v-if="getProviderFromModel">
          <img
            class="provider-logo-img"
            :src="getProviderLogo"
            :alt="getProviderFromModel"
          />
        </div>
        <h3
          :style="{
            margin: 0,
            width: '100%',
            lineHeight: 2,
            backgroundColor: stringToColor(columnData.model),
          }"
        >
          {{ columnData.model }}
        </h3>
      </div>
      <div class="stats">
        <span>
          <!-- optional spot for stats -->
        </span>
      </div>
    </div>

    <div class="responses-container">
      <div v-if="columnData.state === 'loading'" class="loading-indicator">
        <div class="spinner"></div>
        <span>Processing...</span>
      </div>

      <div v-else-if="columnData.state === 'error'" class="error-message">
        <span>{{ columnData.responses[0]?.error }}</span>
        <button @click="$emit('retry', columnData.model)">Retry</button>
      </div>

      <template v-else>
        <div
          v-for="(response, index) in columnData.responses"
          :key="index"
          class="response-card"
        >
          <div class="response-header">
            <span>Prompt #{{ columnData.responses.length - index }}</span>
          </div>

          <div class="thought-section" v-if="store.settings.columnDisplay !== 'response'">
            <div class="section-header">
              <h4>Thoughts</h4>
              <button
                @click="copyToClipboard(response.thoughts)"
                class="copy-button"
              >
                Copy
              </button>
            </div>
            <div class="content" :style="{ maxHeight: columnHeight + 'px' }">
              <VueMarkdown
                v-if="response.thoughts"
                :source="response.thoughts"
                class="markdown-content"
              />
              <span v-else>No thoughts provided</span>
            </div>
          </div>

          <div class="response-section" v-if="store.settings.columnDisplay !== 'thoughts'">
            <div class="section-header">
              <h4>Response</h4>
              <button
                @click="copyToClipboard(response.response)"
                class="copy-button"
              >
                Copy
              </button>
            </div>
            <div class="content" :style="{ maxHeight: columnHeight + 'px' }">
              <VueMarkdown
                :source="response.response"
                class="markdown-content"
              />
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { store } from "../../stores/thoughtBenchStore";
import type { ThoughtBenchColumnData } from "../../types";
import { copyToClipboard } from "../../utils";
import VueMarkdown from "vue-markdown-render";
import { computed } from "vue";
import { stringToColor } from "../../utils";
import anthropicLogo from "../../assets/anthropic.svg";
import ollamaLogo from "../../assets/ollama.svg";
import openaiLogo from "../../assets/openai.svg";
import googleLogo from "../../assets/google.svg";
import groqLogo from "../../assets/groq.svg";
import deepseekLogo from "../../assets/deepseek.svg";

const props = defineProps<{
  columnData: ThoughtBenchColumnData;
  columnHeight: number;
}>();

const emit = defineEmits<{
  (e: "retry", model: string): void;
}>();

const getProviderFromModel = computed(() => {
  const provider = props.columnData.model.split(":")[0];
  return provider ? provider.toLowerCase() : null;
});

const getProviderLogo = computed(() => {
  const provider = getProviderFromModel.value;
  switch (provider) {
    case "anthropic":
      return anthropicLogo;
    case "openai":
      return openaiLogo;
    case "google":
      return googleLogo;
    case "groq":
      return groqLogo;
    case "ollama":
      return ollamaLogo;
    case "deepseek":
      return deepseekLogo;
    case "gemini":
      return googleLogo;
    default:
      return null;
  }
});
</script>

<style scoped>
.thought-column {
  /* border: 1px solid #ddd; */
  border-radius: 8px;
  padding: 1rem;
  background: white;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.thought-column.loading {
  opacity: 0.7;
}

.thought-column.error {
  border-color: #ff4444;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.provider-logo {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  display: inline-block;
  vertical-align: middle;
}

.provider-logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.column-header h3 {
  display: inline-block;
  vertical-align: middle;
  margin: 0;
  font-size: 1.2rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #333;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  transition: all 0.2s ease;
}

.stats {
  font-size: 0.9rem;
  color: #666;
}

.responses-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 100%;
}

.response-card {
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
}

.thought-section {
  background: #f8fbff;
  border-left: 4px solid #0e4491;
  margin: 0.5rem 0;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.thought-section:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 8px rgba(14, 68, 145, 0.1);
}

.thought-section .section-header {
  padding: 0.5rem;
  background: rgba(14, 68, 145, 0.05);
  border-radius: 4px 4px 0 0;
}

.thought-section h4 {
  color: #0e4491;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  font-size: 0.9rem;
}

.thought-section h4::before {
  content: "💡";
  font-size: 1.1em;
}

.response-section {
  background: #fff5f8; /* Light pink background */
  border-left: 4px solid #e91e63; /* Pink accent border */
  margin: 0.5rem 0;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.response-section:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 8px rgba(233, 30, 99, 0.1);
}

.response-section .section-header {
  padding: 0.5rem;
  background: rgba(233, 30, 99, 0.05);
  border-radius: 4px 4px 0 0;
}

.response-section h4 {
  color: #e91e63; /* Pink color */
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  font-size: 0.9rem;
}

.response-section h4::before {
  content: "💬"; /* Speech bubble emoji */
  font-size: 1.1em;
}

.response-section .copy-button {
  background: rgba(233, 30, 99, 0.1);
  color: #e91e63;
}

.response-section .copy-button:hover {
  background: rgba(233, 30, 99, 0.2);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.section-header h4 {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

.content {
  overflow-y: auto;
  white-space: pre-wrap;
  font-family: monospace;
  font-size: 0.9rem;
  line-height: 1.4;
  padding: 1rem;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.copy-button {
  padding: 4px 12px;
  font-size: 0.8rem;
  background: rgba(14, 68, 145, 0.1);
  color: #0e4491;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.copy-button:hover {
  background: rgba(14, 68, 145, 0.2);
}

.response-card {
  transition: all 0.3s ease;
  overflow: hidden;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.response-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.response-card:not(:last-child) {
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
}

.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
  font-size: 0.85rem;
  color: #666;
}

.prompt-preview {
  font-style: italic;
  color: #999;
  max-width: 40%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-message {
  color: #ff4444;
  text-align: center;
  padding: 1rem;
}

.error-message button {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-message button:hover {
  background: #ff3333;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.markdown-content ul,
.markdown-content ol {
  margin: 0.5rem 0;
  padding-left: 1rem;
}

.markdown-content li {
  margin: 0.5rem 0;
}
</style>

<style>
/* Add markdown styling */
.markdown-content {
  color: #333;
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  color: #0e4491;
  margin: 1.5rem 0 1rem;
}

.markdown-content p {
  margin: 1rem 0;
}

.markdown-content code {
  background: #f5f7ff;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  color: #e91e63;
}

.markdown-content pre {
  background: #f5f7ff;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  margin: 1rem 0;
}

.markdown-content pre code {
  background: #f5f7ff;
  padding: 0;
  color: inherit;
}

.markdown-content blockquote {
  border-left: 4px solid #0e4491;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #666;
  font-style: italic;
}

.markdown-content a {
  color: #0e4491;
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}
</style>
