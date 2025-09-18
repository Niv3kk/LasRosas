<template>
  <main class="historial-container">
    <h1 class="main-title">Historial de Alquileres</h1>

    <div class="search-bar">
      <div class="search-input-wrapper">
        <i class="bi bi-search"></i>
        <input type="text" placeholder="Buscar..." />
      </div>
      <button class="filter-btn">
        <span>Filtrar</span>
        <img src="@/assets/Filtro.png" alt="Filtrar" />
      </button>
    </div>

    <div class="historial-list">
      <div class="historial-card" v-for="alquiler in historiales" :key="alquiler.id">
        <div class="card-content">
          <div class="fw-semibold">Alquiler de: {{ alquiler.cliente }}</div>
          <div>Ubicación: {{ alquiler.ubicacion }}</div>
          <div class="text-muted small mt-auto">{{ alquiler.fecha }}</div>
        </div>

        <div class="card-details small">
          <div class="row">
            <div class="col-4 fw-semibold">Cant.</div>
            <div class="col-8 fw-semibold">Detalle</div>
            <template v-for="(item, index) in alquiler.detalle" :key="index">
              <div class="col-4">{{ item.cant }}</div>
              <div class="col-8">{{ item.item }}</div>
            </template>
          </div>
        </div>

        <div class="card-actions">
          <button class="btn btn-edit" @click="abrirModal(alquiler)">
            <span>Editar</span>
            <img src="@/assets/Edit.png" alt="editar" />
          </button>
          <button class="btn btn-delete" @click="abrirModal(alquiler)">
            <span>Borrar</span>
            <img src="@/assets/Delete.png" alt="eliminar" />
          </button>
        </div>
      </div>
    </div>

    <EditarAlquilerModal
      v-if="modalVisible"
      :alquiler="alquilerSeleccionado"
      @cerrar="cerrarModal"
      @borrar="borrarAlquiler"
      @guardar="guardarAlquiler" 
    />
  </main>
</template>

<script setup>
import { ref } from 'vue';
// ===== ADICIÓN: Importar el nuevo componente =====
import EditarAlquilerModal from '@/components/EditarAlquilerModal.vue';

// ===== ADICIÓN: Variables para controlar el modal =====
const modalVisible = ref(false);
const alquilerSeleccionado = ref(null);

// Datos de ejemplo (sin cambios)
const historiales = ref([
  {
    id: 1,
    cliente: 'Andrea Garnica',
    ubicacion: 'Urb. Del Valle #12',
    fecha: '14/09/2024',
    detalle: [ { cant: 50, item: 'Mesas' }, { cant: 600, item: 'Sillas' } ],
  },
  {
    id: 2,
    cliente: 'Carlos Soliz',
    ubicacion: 'Av. América #555',
    fecha: '12/09/2024',
    detalle: [ { cant: 2, item: 'Carpas Grandes' }, { cant: 150, item: 'Sillas' } ],
  },
]);

// ===== ADICIÓN: Funciones para manejar la lógica del modal =====
const abrirModal = (alquiler) => {
  alquilerSeleccionado.value = alquiler;
  modalVisible.value = true;
};

const cerrarModal = () => {
  modalVisible.value = false;
  alquilerSeleccionado.value = null;
};

const borrarAlquiler = (idAlquiler) => {
  if (confirm('¿Estás seguro de que quieres borrar este registro del historial?')) {
    historiales.value = historiales.value.filter(h => h.id !== idAlquiler);
    cerrarModal();
  }
};

const guardarAlquiler = (alquilerEditado) => {
  const index = historiales.value.findIndex(h => h.id === alquilerEditado.id);
  if (index !== -1) {
    historiales.value[index] = alquilerEditado;
  }
  cerrarModal();
};
</script>

<style scoped>
.historial-container {
  padding: 2rem;
  background-color: #f0f2f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.main-title {
  text-align: center;
  color: #000;
  margin-bottom: 2rem;
  font-weight: 600;
}

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

.filter-btn img {
  height: 23px;
  align-items: center;
}

.filter-btn:hover {
  background-color: #f7f7f7;
}

.historial-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 1.5rem;
  display: flex;
  gap: 2rem;
}

.card-content {
  flex: 1.2;
  display: flex;
  flex-direction: column;
}

.card-details {
  flex: 1.5;
  border-left: 1px solid #eee;
  border-right: 1px solid #eee;
  padding: 0 2rem;
}

.card-actions {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.75rem;
}

.fw-semibold {
  font-weight: 600;
}

.text-muted {
  color: #6c757d;
}

.small {
  font-size: 0.9rem;
}

.mt-auto {
  margin-top: auto;
}

.btn {
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1rem;
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
  background-color: #00BCD4;
}

.btn-edit:hover {
  background-color: #00BCD4;
}

.btn-delete {
  background-color: #E53935;
}

.btn-delete:hover {
  background-color: #E53935;
}

.btn-edit img,
.btn-delete img {
  height: 23px;
}
/* Para los botones de "Editar" */
.btn-edit:active,
.btn-edit:focus {
  background-color: #00BCD4 !important; 
  border-color: #00BCD4 !important;
  box-shadow: none !important;
}

/* Para los botones de "Borrar" */
.btn-delete:active,
.btn-delete:focus {
  background-color: #E53935 !important; 
  border-color: #E53935 !important;
  box-shadow: none !important;
}

.row {
  display: flex;
  flex-wrap: wrap;
}

.col-4 {
  flex: 0 0 auto;
  width: 33.33333333%;
}

.col-8 {
  flex: 0 0 auto;
  width: 66.66666667%;
}

/* ===== NUEVO: ESTILOS RESPONSIVOS PARA LA PÁGINA ===== */
@media (max-width: 768px) {
  .historial-container {
    padding: 1rem; /* Menos padding en móvil */
  }
  .search-bar {
    flex-direction: column; /* Apila el buscador y el filtro */
  }
  .historial-card {
    flex-direction: column; /* Apila las secciones de la tarjeta */
    gap: 1rem;
  }
  .card-details {
    padding: 1rem 0; /* Ajusta el padding */
    border-left: none;
    border-right: none;
    border-top: 1px solid #eee;
    border-bottom: 1px solid #eee;
  }
  .card-actions {
    flex-direction: row; /* Botones en fila en móvil */
    justify-content: center;
  }
}
</style>
