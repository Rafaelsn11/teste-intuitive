<script setup lang="ts">
import OperadoraSearch from './components/operadora/OperadoraSearch.vue';
</script>

<template>
  <header>
    <h1>Sistema de Busca de Operadoras</h1>
  </header>

  <main>
    <OperadoraSearch />
  </main>
</template>

<style scoped>
header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  body {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
