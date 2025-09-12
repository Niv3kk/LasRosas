<template>
  <main class="historial-container">
    <h1 class="main-title">Historial de Inventario</h1>

    <div class="search-bar">
      <div class="search-input-wrapper">
        <i class="bi bi-search"></i>
        <input type="text" placeholder="Buscar...">
      </div>
      <button class="filter-btn">
        <span>Filtrar</span>
        <img src="@/assets/Filtro.png" alt="">
      </button>
    </div>

    <div class="log-list">
      <div class="log-card" v-for="log in historial" :key="log.id">
        
        <div class="log-date">{{ log.fecha }}</div>

        <div class="log-detail">{{ log.detalle }}</div>

        <div 
          class="log-change" 
          :class="{
            'positive-change': log.cambio > 0, 
            'negative-change': log.cambio < 0
          }">
          {{ log.cambio > 0 ? '+' : '' }}{{ log.cambio }}
        </div>

      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';

// Datos de ejemplo para el historial de inventario.
// Esto lo conectarás luego con tu base de datos.
const historial = ref([
  { id: 1, fecha: '14/09/2024', detalle: 'Se realizó la reducción de platos por perdida', cambio: -4 },
  { id: 2, fecha: '14/09/2024', detalle: 'Se realizó la reducción de sillas por daño', cambio: -1 },
  { id: 3, fecha: '14/09/2024', detalle: 'Se realizó la reposición de una caja de vasos champaneros', cambio: 12 },
  { id: 4, fecha: '13/09/2024', detalle: 'Compra de 50 manteles nuevos', cambio: 50 },
  { id: 5, fecha: '13/09/2024', detalle: 'Se realizó la reducción de tenedores por perdida', cambio: -10 },
  { id: 6, fecha: '12/09/2024', detalle: 'Salida de 2 toldos para evento', cambio: -2 },
]);
</script>

<style scoped>
/* Estilo General del Contenedor */
.historial-container {
  padding: 2rem;
  background-color: #f0f2f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

/* Título */
.main-title {
  text-align: center;
  color: #000000;
  margin-bottom: 2rem;
  font-weight: 600;
}

/* Barra de Búsqueda (reutilizamos estilos de la vista anterior para consistencia) */
.search-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.search-input-wrapper {
  flex-grow: 1;
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0 0.75rem;
}

.search-input-wrapper i {
  color: #888;
}

.search-input-wrapper input {
  width: 100%;
  border: none;
  outline: none;
  padding: 0.75rem 0.5rem;
  font-size: 1rem;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}
.filter-btn img{
  height: 23px;
  align-items: center;
}
.filter-btn:hover {
  background-color: #f7f7f7;
}

/* Tarjeta de cada registro del historial */
.log-card {
  background: white;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;
  
  /* Usamos Grid para alinear las 3 columnas */
  display: grid;
  grid-template-columns: 1fr 3fr 1fr; /* Columna de detalle es 3 veces más ancha */
  align-items: center;
  gap: 1.5rem;
  font-size: 1rem;
}

.log-date {
  text-align: left;
  color: #666;
}

.log-detail {
  text-align: left;
}

.log-change {
  text-align: right;
  font-weight: 700;
  font-size: 1.1rem;
}

/* Estilos para los números positivos y negativos */
.positive-change {
  color: #4CAF50; /* Verde */
}

.negative-change {
  color: #E53935; /* Rojo */
}
</style>