<template>
  <main class="precios-container">
    <div class="table-container">
      
      <div class="titles-wrapper">
        <h2 
          class="section-title"
          :class="{ 'active-title': vistaActiva === 'precios' }"
          @click="vistaActiva = 'precios'">
          Lista de Precios
        </h2>
        <h2 
          class="section-title"
          :class="{ 'active-title': vistaActiva === 'danos' }"
          @click="vistaActiva = 'danos'">
          Lista de Precios daño o perdida
        </h2>
      </div>

      <!-- 🔄 Loader dentro de la tarjeta blanca -->
      <div v-if="loading" class="loader-wrapper">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
        <p class="mt-2">Cargando lista de precios...</p>
      </div>

      <!-- 📋 Tabla solo cuando ya cargó -->
      <div v-else class="table-scroll-wrapper">
        <table class="prices-table">
          <thead>
            <tr>
              <th>Cant.</th>
              <th>Detalle</th>
              <th>Precio Unit.</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in datosTablaActiva" :key="item.id">
              <td class="text-right">{{ item.cantidad }}</td>
              <td>{{ item.detalle }}</td>
              <td class="text-right">{{ item.precioUnitario }} Bs.</td>
              <td class="text-right fw-bold">{{ item.total }} Bs.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        class="actions-container"
        v-if="usuarioActual?.rol?.nombre_rol === 'Administrador'"
      >
        <button class="btn btn-edit" @click="abrirModal">
          <span>Editar</span>
          <img src="@/assets/Edit.png" alt="editar">
        </button>
      </div>

      <!-- Toast centrado en la parte baja de la tarjeta -->
      <transition name="fade">
        <div
          v-if="toastVisible"
          class="toast-notification"
          :class="toastType === 'success' ? 'toast-success' : 'toast-error'"
        >
          {{ toastMessage }}
        </div>
      </transition>
    </div>

    <EditarPreciosModal
      v-if="modalVisible"
      :lista="datosTablaActiva"
      :guardando="guardando"
      @cerrar="cerrarModal"
      @guardar="guardarCambios"
    />
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { usuarioActual } from '@/services/auth';
import EditarPreciosModal from '@/components/EditarPreciosModal.vue';

import {
  fetchListaPreciosAlquiler,
  fetchListaPreciosDanos,
  saveListaPreciosAlquiler,
  saveListaPreciosDanos,
} from '@/services/prices';

/* Estado general */
const modalVisible = ref(false);
const vistaActiva = ref('precios');
const guardando = ref(false);
const loading = ref(true);

/* Listas principales */
const listaPrecios = ref([]);
const listaPreciosDanos = ref([]);

/* Toast */
const toastVisible = ref(false);
const toastMessage = ref('');
const toastType = ref('success');
let toastTimeoutId = null;

const mostrarToast = (message, type = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  toastVisible.value = true;

  if (toastTimeoutId) {
    clearTimeout(toastTimeoutId);
  }

  toastTimeoutId = setTimeout(() => {
    toastVisible.value = false;
  }, 3000);
};

/* Cargar datos desde API */
const cargarDatos = async () => {
  loading.value = true;
  try {
    const [alq, dan] = await Promise.all([
      fetchListaPreciosAlquiler(),
      fetchListaPreciosDanos(),
    ]);

    // Lista de precios de ALQUILER
    listaPrecios.value = alq.data.map(i => ({
      id: i.precio_alquiler_id,
      cantidad: i.unidades_incluidas,
      detalle: i.nombre_articulo || i.nombre_tarifa,
      precioUnitario: Number(i.precio_tarifa),
      total: Number(i.unidades_incluidas) * Number(i.precio_tarifa),
      inventario_id: i.inventario_id,
      nombre_tarifa: i.nombre_tarifa,
    }));

    // Lista de precios de DAÑOS
    listaPreciosDanos.value = dan.data.map(i => {
      const unidades = i.unidades_incluidas ?? 1;
      return {
        id: i.precio_dano_id,
        cantidad: unidades,
        detalle: i.nombre_articulo || i.nombre_tarifa,
        precioUnitario: Number(i.precio_tarifa),
        total: unidades * Number(i.precio_tarifa),
        inventario_id: i.inventario_id,
        nombre_tarifa: i.nombre_tarifa,
      };
    });

  } catch (err) {
    console.error(err);
    mostrarToast('Error al cargar las listas de precios.', 'error');
  }
  loading.value = false;
};

onMounted(cargarDatos);

/* Lógica de tabla activa */
const datosTablaActiva = computed(() =>
  vistaActiva.value === 'precios'
    ? listaPrecios.value
    : listaPreciosDanos.value
);

/* Modal */
const abrirModal = () => { modalVisible.value = true; };
const cerrarModal = () => { modalVisible.value = false; };

/* Guardar cambios */
const guardarCambios = async (listaEditada) => {
  guardando.value = true;

  try {
    if (vistaActiva.value === 'precios') {
      const payload = listaEditada.map(i => ({
        precio_alquiler_id: i.id,
        inventario_id: i.inventario_id,
        nombre_tarifa: i.nombre_tarifa || 'Precio por Unidad',
        unidades_incluidas: i.cantidad,
        precio_tarifa: i.precioUnitario,
      }));
      await saveListaPreciosAlquiler(payload);
      listaPrecios.value = listaEditada;

      mostrarToast('Precios de alquiler guardados correctamente.');

    } else {
      const payload = listaEditada.map(i => ({
        precio_dano_id: i.id,
        inventario_id: i.inventario_id,
        nombre_tarifa: i.nombre_tarifa || 'Daño o pérdida',
        unidades_incluidas: i.cantidad,
        precio_tarifa: i.precioUnitario,
      }));
      await saveListaPreciosDanos(payload);
      listaPreciosDanos.value = listaEditada;

      mostrarToast('Precios de daños guardados correctamente.');
    }

    cerrarModal();

  } catch (err) {
    console.error(err);
    if (vistaActiva.value === 'precios') {
      mostrarToast('Error al guardar precios de alquiler.', 'error');
    } else {
      mostrarToast('Error al guardar precios de daños.', 'error');
    }
  }

  guardando.value = false;
};
</script>

<style scoped>
.precios-container {
  padding: 2rem;
  background-color: #f0f2f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  height: 100%;
  display: flex;
}

.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: hidden;
  padding: 1.5rem 2rem;
  position: relative;
}

/* loader centrado dentro de la tarjeta */
.loader-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.titles-wrapper {
  display: flex;
  justify-content: center;
  gap: 15rem;
  margin-bottom: 2rem;
}

.table-scroll-wrapper {
  flex-grow: 1;
  overflow-y: auto;
}

.section-title {
  font-size: 2.1rem;
  font-weight: 500;
  color: #000000;
  cursor: pointer;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.active-title {
  color: #c9434d;
  font-weight: 600;
  border-bottom-color: #c9434d;
}

/* Tabla */
.prices-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

.prices-table th,
.prices-table td {
  padding: 0.8rem 1rem;
  text-align: left;
  vertical-align: middle;
}

.prices-table th {
  font-weight: 600;
  color: #000000;
  border-bottom: 2px solid #ddd;
}

.prices-table td {
  border-right: 1px solid #f0f0f0;
}
.prices-table th:last-child,
.prices-table td:last-child {
  border-right: none;
}

.prices-table tbody tr {
  border-bottom: 1px solid #f0f0f0;
}
.prices-table tbody tr:last-child {
  border-bottom: none;
}

.text-right {
  text-align: right;
}
.fw-bold {
  font-weight: 700;
}

/* Botón editar */
.actions-container {
  display: flex;
  justify-content: flex-end;
}

.btn {
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  transition: opacity 0.2s;
}
.btn:hover {
  opacity: 0.85;
}
.btn-edit {
  background-color: #00BCD4;
}
.btn-edit:hover{
  background-color: #00BCD4;
}
.btn-edit img{
  height: 23px;
}
.btn-edit:active,
.btn-edit:focus {
  background-color: #00BCD4 !important; 
  border-color: #00BCD4 !important;
  box-shadow: none !important;
}

/* Responsive */
@media (max-width: 768px) {
  .prices-table {
    border: 0;
  }

  .prices-table thead {
    display: none;
  }

  .prices-table tbody {
    display: block;
  }

  .prices-table tr {
    display: block;
    border: 1px solid #00000069;
    border-radius: 8px;
    margin-bottom: 1rem;
    padding: 1rem;
  }

  .prices-table td {
    display: block;
    text-align: right !important;
    padding-left: 50%;
    position: relative;
    border-bottom: 1px dotted #eee;
  }

  .prices-table td:last-child {
    border-bottom: none;
  }

  .prices-table td::before {
    content: attr(data-label);
    position: absolute;
    left: 10px;
    width: 45%;
    text-align: left;
    font-weight: bold;
  }
}

/* Toast */
.toast-notification {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.9rem 1.4rem;
  border-radius: 10px;
  color: white;
  font-weight: 600;
  background-color: #4caf50;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  z-index: 50;
}
.toast-success { background-color: #4caf50; }
.toast-error { background-color: #f44336; }

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
