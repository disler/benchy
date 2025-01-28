<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import AppMultiAutocomplete from "./pages/AppMultiAutocomplete.vue";
import AppMultiToolCall from "./pages/AppMultiToolCall.vue";
import IsoSpeedBench from "./pages/IsoSpeedBench.vue";
import ThoughtBench from "./pages/ThoughtBench.vue";

const routes = {
  "/autocomplete": AppMultiAutocomplete,
  "/tool-call": AppMultiToolCall,
  "/iso-speed-bench": IsoSpeedBench,
  "/thought-prompt": ThoughtBench,
};

const currentPath = ref(window.location.hash);

const currentView = computed(() => {
  if (!currentPath.value) {
    return null;
  }
  return routes[currentPath.value.slice(1) as keyof typeof routes] || null;
});

onMounted(() => {
  window.addEventListener("hashchange", () => {
    currentPath.value = window.location.hash;
  });
});

document.title = "BENCHY";
</script>

<template>
  <div class="app-container" :class="{ 'home-gradient': !currentView }">
    <div class="home-container" v-if="!currentView">
      <h1 class="title">BENCHY</h1>
      <p class="subtitle">Interactive benchmarks you can <b>feel</b></p>
      <nav class="nav-buttons">
        <a href="#/autocomplete" class="nav-button autocomplete-bg">
          <div class="nav-button-content">
            <div class="title">Multi Autocomplete</div>
            <div class="desc">Benchmark completions across multiple LLMs</div>
          </div>
        </a>

        <a href="#/tool-call" class="nav-button toolcall-bg">
          <div class="nav-button-content">
            <div class="title">Long Tool Call</div>
            <div class="desc">Simulate long tool-chaining tasks</div>
          </div>
        </a>

        <a href="#/iso-speed-bench" class="nav-button isospeed-bg">
          <div class="nav-button-content">
            <div class="title">ISO Speed Bench</div>
            <div class="desc">Compare performance on a timeline</div>
          </div>
        </a>

        <a href="#/thought-prompt" class="nav-button thoughtbench-bg">
          <div class="nav-button-content">
            <div class="title">Thought Bench</div>
            <div class="desc">Analyze model reasoning and responses</div>
          </div>
        </a>
      </nav>
    </div>
    <component :is="currentView" v-else />
  </div>
</template>

<style scoped>
.title {
  font-size: 5rem;
  font-weight: bold;
  background: linear-gradient(
    90deg,
    rgba(14, 68, 145, 1) 0%,
    rgba(0, 212, 255, 1) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(0, 212, 255, 0.8);
  margin-bottom: 1rem;
}

.home-container {
  text-align: center;
  padding: 2rem;
}

.app-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nav-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  flex-wrap: wrap;
  justify-content: center;
}

.home-gradient {
  animation: slow-gradient 15s ease-in-out infinite alternate;
}

@keyframes slow-gradient {
  0% {
    background: linear-gradient(180deg, #e0f7ff 0%, #ffffff 100%);
  }
  100% {
    background: linear-gradient(180deg, #ffffff 0%, #e0f7ff 100%);
  }
}

.nav-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  text-align: center;
}

.nav-button-content .title {
  font-size: 1.5em;
  margin-bottom: 0.5em;
}

.nav-button-content .desc {
  font-size: 0.85em;
  line-height: 1.2;
  opacity: 0.9;
}

.autocomplete-bg {
  background-color: #e6f0ff;
}
.toolcall-bg {
  background-color: #f9ffe6;
}
.isospeed-bg {
  background-color: #fffbf0;
}

.thoughtbench-bg {
  background-color: #f7e6ff;
}

.nav-button {
  padding: 1rem 2rem;
  border: 2px solid rgb(14, 68, 145);
  border-radius: 8px;
  color: rgb(14, 68, 145);
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
  width: 300px;
  height: 300px;
}

.nav-button:hover {
  background-color: rgb(14, 68, 145);
  color: white;
}

.router-link-active {
  background-color: rgb(14, 68, 145);
  color: white;
}
</style>
