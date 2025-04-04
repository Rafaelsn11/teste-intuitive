<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  loading: boolean
}>()

defineEmits<{
  search: [query: string]
}>()

const query = ref('');
</script>

<template>
  <div class="search-container">
    <input 
      type="text"
      v-model="query"
      @keyup.enter="$emit('search', query)"
      placeholder="Digite o nome da operadora..."
      class="search-input"
    >
    <button 
      @click="$emit('search', query)"
      :disabled="loading"
      class="search-button"
    >
      {{ loading ? 'Buscando...' : 'Buscar' }}
    </button>
  </div>
</template>

<style scoped>
.search-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-button {
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-button:disabled {
  background-color: #cccccc;
}
</style>