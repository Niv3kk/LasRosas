<template>
  <main class="inventario-container">
    <h1 class="main-title">Inventario</h1>

    <!-- UI de Carga -->
    <div v-if="loading" class="text-center" style="padding: 5rem">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-2">Cargando inventario...</p>
    </div>

    <!-- UI de Error -->
    <div v-if="error" class="alert alert-danger mx-3">
      <strong>Error:</strong> {{ error }}
    </div>

    <div class="table-container" v-if="!loading && !error">
      <div class="table-scroll-wrapper">
        <table class="inventory-table responsive-table">
          <thead>
            <tr>
              <th class="text-right">Stock Actual</th>
              <th>Artículo</th>
              <th>Detalle</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in inventario"
              :key="item.id"
            >
              <td data-label="Stock Actual" class="text-right fw-bold">
                {{ item.stock_actual }}
              </td>
              <td data-label="Artículo">{{ item.nombre_articulo }}</td>
              <td data-label="Detalle">{{ item.detalle }}</td>
            </tr>

            <tr v-if="inventario.length === 0">
              <td colspan="3" class="text-center">
                No se encontraron artículos en el inventario.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getInventario } from '@/services/inventarioService.js';

const inventario = ref([]);
const loading = ref(true);
const error = ref(null);

const cargarInventario = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await getInventario();
    inventario.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = 'Error al cargar el inventario. Intente de nuevo.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  cargarInventario();
});
</script>


<style scoped>
/* Contenedor principal de la página de inventario */
.inventario-container {
  /* Lo hacemos un contenedor flex vertical que ocupe toda la altura disponible */
  display: flex;
  flex-direction: column;
  height: 100%; 
}

.main-title {
  text-align: center;
  color: #000000;
  margin-bottom: 2rem;
  /* Hacemos que el título no se encoja */
  flex-shrink: 0;
}

/* El contenedor blanco de la tabla */
.table-container {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  
  /* Hacemos que crezca para ocupar el espacio y sea un flex container */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Importante para que el borde redondeado contenga el scroll */
}

/* --- NUEVOS ESTILOS PARA EL SCROLL --- */

/* 1. El nuevo div que tendrá la barra de scroll */
.table-scroll-wrapper {
  overflow-y: auto; /* <-- La magia del scroll vertical */
  flex-grow: 1; /* Hará que ocupe todo el espacio disponible dentro de la tarjeta */
}

/* 2. Hacemos que los encabezados de la tabla se queden fijos arriba */
.inventory-table thead th {
  position: sticky;
  top: 0;
  background-color: white; /* Necesario para que el contenido no se vea a través */
  z-index: 1; /* Asegura que esté por encima del contenido que se desplaza */
}

/* --- ESTILOS EXISTENTES (sin cambios o con pequeños ajustes) --- */

.inventory-table {
  width: 100%;
  border-collapse: collapse;
}

.inventory-table th,
.inventory-table td {
  padding: 0.8rem 5px;
  text-align: left;
  vertical-align: middle;
}

.inventory-table th {
  font-weight: 600;
  color: #000000;
  border-bottom: 2px solid #ddd;
}

.inventory-table td {
  border-right: 1px solid #f0f0f0;
}
.inventory-table th:last-child,
.inventory-table td:last-child {
  border-right: none;
}

.inventory-table tbody tr {
  border-bottom: 1px solid #f0f0f0;
}
.inventory-table tbody tr:last-child {
  border-bottom: none;
}

.actions-container {
  display: flex;
  justify-content: flex-end;
  padding: 1.5rem 1rem 1rem 1rem; /* Añadimos padding arriba */
  flex-shrink: 0; /* Evita que el contenedor del botón se encoja */
}

/* Botón de Editar */
.btn {
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  transition: opacity 0.2s;
}
.btn:hover {
  opacity: 0.85;
}
.btn-edit {
  background-color: #00BCD4; /* Cian */
}
.btn-edit:hover{
  background-color: #00BCD4;
}
.btn-edit img{
  height: 23px;
}
/* Para los botones de "Editar" */
.btn-edit:active,
.btn-edit:focus {
  background-color: #00BCD4 !important; 
  border-color: #00BCD4 !important;
  box-shadow: none !important;
}
/* TUS ESTILOS RESPONSIVOS ESTÁN CORRECTOS, AHORA FUNCIONARÁN */
@media (max-width: 768px) {
  .inventario-container {
    padding: 1rem;
  }
  .table-container {
    padding: 0.5rem;
  }
  .responsive-table thead {
    display: none;
  }
  .responsive-table tr {
    display: block;
    border: 1px solid #00000069;
    border-radius: 8px;
    margin-bottom: 1rem;
    padding: 1rem;
  }
  .responsive-table td {
    display: block;
    text-align: right !important;
    padding-left: 40%;
    position: relative;
    border-bottom: 1px dotted #eee;
  }
  .responsive-table td:last-child {
    border-bottom: none;
  }
  .responsive-table td:before {
    content: attr(data-label);
    position: absolute;
    left: 10px;
    width: 35%;
    padding-right: 10px;
    text-align: left;
    font-weight: bold;
  }
}
</style>