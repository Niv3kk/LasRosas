<template>
  <main class="historial-container">
    <h1 class="main-title">{{ pageTitle }}</h1>

    <div class="search-bar">
      <div class="search-input-wrapper">
        <i class="bi bi-search"></i>
        <input
          type="text"
          placeholder="Buscar por motivo, artículo o usuario..."
          v-model="searchTerm"
        >
      </div>

      <button
        class="btn btn-secondary"
        @click="clearFilter"
        v-if="route.query.item_id"
      >
        <span>Ver todo</span>
        <i class="bi bi-x-circle"></i>
      </button>

      <!-- 🔹 Botón aparece siempre que seas Admin -->
      <button
        class="btn btn-edit"
        v-if="esAdmin"
        @click="abrirModalNuevo"
      >
        <span>Agregar Movimiento</span>
        <img src="@/assets/Edit.png" alt="agregar">
      </button>
    </div>

    <div v-if="loading" class="text-center" style="padding: 5rem">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mx-3">
      <strong>Error:</strong> {{ error }}
    </div>

    <div class="log-list" v-if="!loading && !error">
      <div
        class="log-card"
        v-for="log in filteredHistorial"
        :key="log.id"
      >
        <div class="log-date">{{ formatFecha(log.fecha) }}</div>

        <div class="log-detail">
          <strong v-if="!route.query.item_id" class="d-block">
            {{ log.nombre_articulo }}
          </strong>
          {{ log.motivo }}
          <em class="d-block text-muted mt-1">
            Usuario: {{ log.nombre_usuario }}
          </em>
        </div>

        <div
          class="log-change"
          :class="{
            'positive-change': log.tipo_movimiento === 'Entrada',
            'negative-change': log.tipo_movimiento === 'Salida',
          }"
        >
          {{ log.tipo_movimiento === 'Entrada' ? '+' : '' }}
          {{ log.tipo_movimiento === 'Salida' ? '-' : '' }}
          {{ log.cantidad }}
        </div>
      </div>

      <div
        v-if="filteredHistorial.length === 0"
        class="text-center p-5 text-muted"
      >
        No se encontraron movimientos.
      </div>
    </div>
  </main>

  <!-- 🔹 Modal sin props de item -->
  <AgregarHistorialModal
    v-if="modalNuevoVisible"
    @cerrar="cerrarModalNuevo"
    @guardar="guardarNuevoHistorial"
  />
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getHistorialInventario } from '@/services/inventarioService';
import { usuarioActual as usuarioActualRef, getUser } from '@/services/auth.js';
import AgregarHistorialModal from '@/components/AgregarHistorialModal.vue';

const route = useRoute();
const router = useRouter();

// Usuario actual (ref o localStorage)
const usuario = computed(() => {
  return usuarioActualRef.value || getUser();
});
const esAdmin = computed(
  () => usuario.value?.rol?.nombre_rol === 'Administrador'
);

console.log('DEBUG usuario en HistorialInventarioPage:', usuario.value);

// Estado
const historial = ref([]);
const loading = ref(true);
const error = ref(null);
const searchTerm = ref('');
const modalNuevoVisible = ref(false);

// Título dinámico
const pageTitle = computed(() => {
  const itemName = route.query.item_nombre;
  return itemName ? `Historial: ${itemName}` : 'Historial de Inventario';
});

// Carga de datos
const cargarHistorial = async (query) => {
  try {
    loading.value = true;
    error.value = null;

    const filtros = {};
    if (query.item_id) {
      filtros.inventario = query.item_id;
    }

    console.log('DEBUG route.query en HistorialInventarioPage:', query);

    const response = await getHistorialInventario(filtros);
    historial.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = 'Error al cargar el historial. Intente de nuevo.';
  } finally {
    loading.value = false;
  }
};

// Filtro de búsqueda
const filteredHistorial = computed(() => {
  if (!searchTerm.value) {
    return historial.value;
  }
  const lowerSearch = searchTerm.value.toLowerCase();

  return historial.value.filter((log) => {
    const inMotivo =
      log.motivo && log.motivo.toLowerCase().includes(lowerSearch);
    const inArticulo =
      log.nombre_articulo &&
      log.nombre_articulo.toLowerCase().includes(lowerSearch);
    const inUsuario =
      log.nombre_usuario &&
      log.nombre_usuario.toLowerCase().includes(lowerSearch);

    return inMotivo || inArticulo || inUsuario;
  });
});

// Reaccionar a cambios en la URL
watch(
  () => route.query,
  (newQuery) => {
    cargarHistorial(newQuery);
  },
  {
    immediate: true,
    deep: true,
  }
);

// Acciones
const clearFilter = () => {
  router.push({ name: 'historial-inventario' });
};

const abrirModalNuevo = () => {
  modalNuevoVisible.value = true;
};

const cerrarModalNuevo = () => {
  modalNuevoVisible.value = false;
};

const guardarNuevoHistorial = async () => {
  cerrarModalNuevo();
  await cargarHistorial(route.query);
};

// Helper para fecha
const formatFecha = (fechaISO) => {
  if (!fechaISO) return '';
  const fecha = new Date(fechaISO);
  const options = {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  };
  return fecha.toLocaleString('es-BO', options);
};
</script>


<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css");

/* Estilo General del Contenedor */
.historial-container {
  padding: 2rem;
  background-color: #f0f2f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Título */
.main-title {
  text-align: center;
  color: #000000;
  margin-bottom: 2rem;
  font-weight: 600;
}

/* Barra de Búsqueda */
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

/* --- NUEVO: Estilos de Botones (reemplaza .filter-btn) --- */
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
  /* Ajuste para que encaje con la barra */
  padding: 0.75rem 1rem;
  font-size: 1rem;
  line-height: 1.2;
  /* Ajuste de línea */
}

.btn:hover {
  opacity: 0.85;
}

.btn-edit {
  background-color: #00BCD4;
  /* Cian */
}

.btn-edit:hover {
  background-color: #00BCD4;
}

.btn-edit img {
  height: 23px;
}

.btn-edit:active,
.btn-edit:focus {
  background-color: #00BCD4 !important;
  border-color: #00BCD4 !important;
  box-shadow: none !important;
}

.btn-secondary {
  background-color: #6c757d;
  /* Gris de Bootstrap */
}

/* -------------------------------------------------------- */


/* Tarjeta de cada registro del historial */
.log-list {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 5px;
  /* Espacio para scrollbar */
}

.log-card {
  background: white;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;

  display: grid;
  grid-template-columns: 1fr 3fr 1fr;
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

.positive-change {
  color: #4CAF50;
  /* Verde */
}

.negative-change {
  color: #E53935;
  /* Rojo */
}

/* --- NUEVO: Helpers de UI (Carga, Error) --- */
.text-center {
  text-align: center;
}

.text-muted {
  color: #6c757d;
}

.d-block {
  display: block;
}

.mt-1 {
  margin-top: 0.25rem;
}

.p-5 {
  padding: 3rem;
}

.mx-3 {
  margin-left: 1rem;
  margin-right: 1rem;
}

.alert {
  padding: 1rem;
  border: 1px solid transparent;
  border-radius: 8px;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

.spinner-border {
  display: inline-block;
  width: 2rem;
  height: 2rem;
  vertical-align: text-bottom;
  border: 0.25em solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: 0.75s linear infinite spinner-border;
}

@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
}

/* Importar iconos de bootstrap */
/* ------------------------------------------- */


/* ===== ESTILOS RESPONSIVOS ===== */
@media (max-width: 768px) {
  .historial-container {
    padding: 1rem;
  }

  .search-bar {
    flex-direction: column;
  }

  .btn {
    /* Hacemos que los botones ocupen todo el ancho en móvil */
    justify-content: center;
  }

  .log-card {
    grid-template-columns: 1fr;
    gap: 0.5rem;
    text-align: center;
  }

  .log-date,
  .log-detail,
  .log-change {
    text-align: center;
  }
}
</style>