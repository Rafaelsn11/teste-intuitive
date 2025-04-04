<script setup lang="ts">
import { ref } from 'vue'
import type { Operadora } from '@/types/operadora'
import { searchOperadoras } from '@/services/operadoraService'
import OperadoraCard from './OperadoraCard.vue'
import OperadoraSearchForm from './OperadoraSearchForm.vue'

const operadoras = ref<Operadora[]>([])
const loading = ref(false)
const error = ref('')
const query = ref('')

async function handleSearch(searchQuery: string) {
  if (!searchQuery.trim()) return

  query.value = searchQuery.trim()
  loading.value = true
  error.value = ''
  
  try {
    operadoras.value = await searchOperadoras(searchQuery)
  } catch (e) {
    error.value = 'Erro ao buscar operadoras. Tente novamente.'
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="operadora-search">
    <h2>Busca de Operadoras</h2>
    
    <OperadoraSearchForm 
      :loading="loading"
      @search="handleSearch"
    />

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="operadoras.length > 0" class="results">
      <OperadoraCard 
        v-for="operadora in operadoras"
        :key="operadora.Registro_ANS"
        :operadora="operadora"
      />
    </div>
    
    <p v-else-if="!loading && query" class="no-results">
      Nenhuma operadora encontrada.
    </p>
  </div>
</template>

<style scoped>
.operadora-search {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.error {
  color: red;
  margin: 1rem 0;
}

.no-results {
  text-align: center;
  color: #666;
}
</style>