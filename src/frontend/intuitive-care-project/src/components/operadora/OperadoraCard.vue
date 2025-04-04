<script setup lang="ts">
import type { Operadora } from '@/types/operadora'

defineProps<{
  operadora: Operadora
}>()
</script>

<template>
  <div class="operadora-card">
    <h3>{{ operadora.Nome_Fantasia || operadora.Razao_Social }}</h3>
    <p><strong>Registro ANS:</strong> {{ operadora.Registro_ANS }}</p>
    <p><strong>CNPJ:</strong> {{ operadora.CNPJ }}</p>
    <p><strong>Modalidade:</strong> {{ operadora.Modalidade }}</p>
    <p><strong>Localização:</strong> {{ operadora.Cidade }}/{{ operadora.UF }}</p>
  </div>
</template>

<style scoped>
.operadora-card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}
</style>