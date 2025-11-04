<template>
  <!-- 
    SOLUCIÓN:
    Envolvemos todo el <main> en un <template v-if="usuarioActual">.
    Esto previene que se intente leer 'usuarioActual.rol' cuando
    'usuarioActual' todavía es 'null', solucionando el error de "timing".
  -->
  <template v-if="usuarioActual">
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
            <!-- Estas líneas ahora son seguras porque 'usuarioActual' existe -->
            <template v-if="usuarioActual.rol === 'Administrador'">
              <button class="btn btn-edit" @click="abrirModal(alquiler)">
                <span>Editar</span>
                <img src="@/assets/Edit.png" alt="editar" />
              </button>
              <button class="btn btn-delete" @click="solicitarBorrado(alquiler)">
                <span>Borrar</span>
                <img src="@/assets/Delete.png" alt="eliminar" />
              </button>
            </template>
            
            <template v-else-if="usuarioActual.rol === 'Propietaria'">
              <button class="btn btn-revisar" @click="abrirModal(alquiler)">
                <span>Revisar</span>
                <img src="@/assets/Revisar.png" alt="revisar" />
              </button>
            </template>
          </div>
        </div>
      </div>
  
      <EditarAlquilerModal
        v-if="modalVisible"
        :alquiler="alquilerSeleccionado"
        :rol="usuarioActual.rol" 
        @cerrar="cerrarModal"
        @borrar="borrarAlquilerDesdeModal"
        @guardar="guardarAlquiler" 
      />
    </main>
  </template>

  <!-- Opcional: Mensaje de carga mientras 'usuarioActual' es null -->
  <template v-else>
    <div class="text-center p-5">
      Cargando historial...
    </div>
  </template>
</template>

<script setup>
import { ref } from 'vue';
import { usuarioActual } from '@/services/auth.js'; // Asegúrate que la ruta sea correcta
import EditarAlquilerModal from '@/components/EditarAlquilerModal.vue';

const modalVisible = ref(false);
const alquilerSeleccionado = ref(null);

const historiales = ref([
  {
    id: 1,
    cliente: 'Andrea Garnica',
    celular1: '123456789',
    celular2: '76839233',
    numeroPedido: 'HIST-001',
    ubicacion: 'Urb. Del Valle #12',
    direccion: 'Pronto Gas, Av. Villazon Km2 acera sud',
    fecha: '14/09/2024',
    fechaEntrega: '10/09/2024',
    fechaRecojo: '14/09/2024',
    garantia: true,
    granTotal: 350,
    detalle: [ 
      { cant: 50, item: 'Mesas', precioUnitario: 5, total: 250 }, 
      { cant: 100, item: 'Sillas', precioUnitario: 1, total: 100 } 
    ],
  },
  {
    id: 2,
    cliente: 'Carlos Soliz',
    celular1: '77778888',
    celular2: 'N/A',
    numeroPedido: 'HIST-002',
    ubicacion: 'Av. América #555',
    direccion: 'Salón de Eventos "El Paraíso", Av. América #555',
    fecha: '12/09/2024',
    fechaEntrega: '11/09/2024',
    fechaRecojo: '12/09/2024',
    garantia: false,
    granTotal: 450,
    detalle: [ 
      { cant: 2, item: 'Carpas Grandes', precioUnitario: 150, total: 300 }, 
      { cant: 150, item: 'Sillas', precioUnitario: 1, total: 150 }
    ],
  },
]);

// Función para abrir el modal (para Editar y Revisar)
const abrirModal = (alquiler) => {
  alquilerSeleccionado.value = alquiler;
  modalVisible.value = true;
};

const cerrarModal = () => {
  modalVisible.value = false;
  alquilerSeleccionado.value = null;
};

// ===== ACTUALIZACIÓN: Nueva función para borrar desde la tarjeta =====
const solicitarBorrado = (alquilerABorrar) => {
  if (confirm(`¿Estás seguro de que quieres borrar el historial de "${alquilerABorrar.cliente}"?`)) {
    historiales.value = historiales.value.filter(h => h.id !== alquilerABorrar.id);
  }
};

// Función para borrar desde DENTRO del modal
const borrarAlquilerDesdeModal = (idAlquiler) => {
  historiales.value = historiales.value.filter(h => h.id !== idAlquiler);
  cerrarModal();
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
/* Tu CSS no necesita cambios */
.historial-container {
  padding: 2rem;
  background-color: #f0f2f5;
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
  justify-content: center;
}
.filter-btn img {
  height: 23px;
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
}
.btn-edit { background-color: #00BCD4; }
.btn-delete { background-color: #E53935; }
.btn-revisar { background-color: #2ABB68; }
.btn-edit img,
.btn-delete img,
.btn-revisar img {
  height: 23px;
}
.btn-edit:active,
.btn-edit:focus {
  background-color: #00BCD4 !important; 
  border-color: #00BCD4 !important;
  box-shadow: none !important; 
}
.btn-delete:active,
.btn-delete:focus {
  background-color: #E53935 !important; 
  border-color: #E53935 !important;
  box-shadow: none !important; 
}
.btn-revisar:active,
.btn-revisar:focus {
  background-color: #2ABB68 !important; 
  border-color: #2ABB68 !important;
  box-shadow: none !important; 
}
@media (max-width: 768px) {
  .historial-container { padding: 1rem; }
  .search-bar { flex-direction: column; }
  .historial-card { flex-direction: column; gap: 1rem; }
  .card-details { padding: 1rem 0; border-left: none; border-right: none; border-top: 1px solid #eee; border-bottom: 1px solid #eee; }
  .card-actions { flex-direction: row; justify-content: center; }
}
</style>