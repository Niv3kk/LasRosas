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

      <div class="actions-container">
        <button class="btn btn-edit" @click="abrirModal">
          <span>Editar</span>
          <img src="@/assets/Edit.png" alt="editar">
        </button>
      </div>
    </div>
    <EditarPreciosModal
      v-if="modalVisible"
      :lista="datosTablaActiva"
      @cerrar="cerrarModal"
      @guardar="guardarCambios" 
    />
  </main>
</template>

<script setup>
import { ref, computed } from 'vue';
// AÑADE ESTAS LÍNEAS DEBAJO DE "import { ref, computed } from 'vue';"
import EditarPreciosModal from '@/components/EditarPreciosModal.vue';

// Nuevas variables para controlar el modal
const modalVisible = ref(false);

// Variable para saber qué vista está activa: 'precios' o 'danos'
const vistaActiva = ref('precios');

// --- DATOS DE EJEMPLO ---
// Luego conectarás esto a tu base de datos

// Datos para la "Lista de Precios" normal
const listaPrecios = ref([
  { id: 1, cantidad: 12, detalle: 'Sillas', precioUnitario: 25, total: 300 },
  { id: 2, cantidad: 120, detalle: 'Mesas rectangular de plastico', precioUnitario: 2, total: 240 },
  { id: 3, cantidad: 12, detalle: 'Mesas rectangular de madera', precioUnitario: 10, total: 120 },
  { id: 4, cantidad: 121, detalle: 'Mesas redondas de madera', precioUnitario: 1, total: 121 },
  { id: 5, cantidad: 2, detalle: 'Toldos 6x4', precioUnitario: 23, total: 46 },
  { id: 6, cantidad: 5, detalle: 'Cajas de vasos Largos', precioUnitario: 234, total: 1170 },
  { id: 7, cantidad: 4, detalle: 'Cajas de vasos cerveceros', precioUnitario: 43, total: 172 },
]);

// Datos para la "Lista de Precios daño o perdida"
const listaPreciosDanos = ref([
  { id: 1, cantidad: 12, detalle: 'Sillas', precioUnitario: 50, total: 600 },
  { id: 2, cantidad: 120, detalle: 'Mesas rectangular de plastico', precioUnitario: 5, total: 600 },
  { id: 3, cantidad: 12, detalle: 'Mesas rectangular de madera', precioUnitario: 30, total: 360 },
  { id: 4, cantidad: 2, detalle: 'Toldos 6x4', precioUnitario: 100, total: 200 },
  { id: 5, cantidad: 4, detalle: 'Cajas de vasos cerveceros', precioUnitario: 80, total: 320 },
]);


// Propiedad computada que devuelve la lista de datos correcta según la vistaActiva
const datosTablaActiva = computed(() => {
  if (vistaActiva.value === 'precios') {
    return listaPrecios.value;
  } else {
    return listaPreciosDanos.value;
  }
});

// AÑADE ESTAS FUNCIONES AL FINAL DE TU SCRIPT
const abrirModal = () => {
  modalVisible.value = true;
};

const cerrarModal = () => {
  modalVisible.value = false;
};

const guardarCambios = (listaEditada) => {
  if (vistaActiva.value === 'precios') {
    listaPrecios.value = listaEditada;
  } else {
    listaPreciosDanos.value = listaEditada;
  }
  cerrarModal();

};
</script>

<style scoped>
/* Estilo General del Contenedor de la Página */
.precios-container {
  padding: 2rem;
  background-color: #f0f2f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

/* Contenedor blanco para la tabla */
.table-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Contenedor de los títulos/pestañas */
.titles-wrapper {
  display: flex;
  justify-content: center;
  gap: 15rem;
  margin-bottom: 2rem;
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
</style>