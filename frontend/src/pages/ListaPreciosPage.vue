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

      <!-- Mensajes -->
      <div v-if="mensajeExito" class="alert alert-success">
        {{ mensajeExito }}
      </div>
      <div v-if="mensajeError" class="alert alert-error">
        {{ mensajeError }}
      </div>

      <div class="table-scroll-wrapper">
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

      <div class="actions-container" v-if="usuarioActual?.rol?.nombre_rol === 'Administrador'">
        <button class="btn btn-edit" @click="abrirModal">
          <span>Editar</span>
          <img src="@/assets/Edit.png" alt="editar">
        </button>
      </div>
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
const mensajeExito = ref('');
const mensajeError = ref('');

/* Listas principales */
const listaPrecios = ref([]);
const listaPreciosDanos = ref([]);

/* Cargar datos desde API */
const cargarDatos = async () => {
  try {
    const [alq, dan] = await Promise.all([
      fetchListaPreciosAlquiler(),
      fetchListaPreciosDanos(),
    ]);

    listaPrecios.value = alq.data.map(i => ({
      id: i.precio_alquiler_id,
      cantidad: i.unidades_incluidas,
      detalle: i.nombre_articulo || i.nombre_tarifa,
      precioUnitario: Number(i.precio_tarifa),
      total: Number(i.unidades_incluidas) * Number(i.precio_tarifa),
      inventario_id: i.inventario_id,
      nombre_tarifa: i.nombre_tarifa,
    }));

    listaPreciosDanos.value = dan.data.map(i => ({
      id: i.precio_dano_id,
      cantidad: i.unidades_incluidas,
      detalle: i.nombre_tarifa || i.nombre_articulo,
      precioUnitario: Number(i.precio_tarifa),
      total: Number(i.unidades_incluidas) * Number(i.precio_tarifa),
      inventario_id: i.inventario_id,
      nombre_tarifa: i.nombre_tarifa,
    }));

  } catch (err) {
    console.error(err);
  }
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
  mensajeError.value = '';
  mensajeExito.value = '';

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

    } else {
      const payload = listaEditada.map(i => ({
        precio_dano_id: i.id,
        inventario_id: i.inventario_id,
        nombre_tarifa: i.nombre_tarifa || i.detalle,
        unidades_incluidas: i.cantidad,
        precio_tarifa: i.precioUnitario,
      }));
      await saveListaPreciosDanos(payload);
      listaPreciosDanos.value = listaEditada;
    }

    cerrarModal();
    mensajeExito.value = 'Cambios guardados correctamente.';
    setTimeout(() => mensajeExito.value = '', 3000);

  } catch (err) {
    console.error(err);
    mensajeError.value = 'Error al guardar los cambios.';
  }

  guardando.value = false;
};
</script>

<style scoped>
/* Estilo General del Contenedor de la Página */
.precios-container {
  padding: 2rem;
  background-color: #f0f2f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  height: 100%;
  display: flex;
}

/* Contenedor blanco para la tabla */
.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: hidden;
  padding: 1.5rem 2rem;
}

/* Contenedor de los títulos/pestañas */
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

/* Tabla de Precios */
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

/* Clases de utilidad para texto */
.text-right {
  text-align: right;
}
.fw-bold {
  font-weight: 700;
}

/* Contenedor del botón Editar */
.actions-container {
  display: flex;
  justify-content: flex-end;
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

/* --- ESTILOS RESPONSIVOS (tarjetitas en móvil) --- */
/* ... todo lo que ya tienes ... */

/* Mensajes de feedback */
.alert {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
}

.alert-success {
  background-color: #e6ffed;
  color: #137333;
  border: 1px solid #b7e4c7;
}

.alert-error {
  background-color: #ffe6e6;
  color: #b00020;
  border: 1px solid #f5b5b5;
}

/* --- ESTILOS RESPONSIVOS (tarjetitas en móvil) --- */
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

</style>
