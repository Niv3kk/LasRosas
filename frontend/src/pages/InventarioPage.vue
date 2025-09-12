<template>
  <main class="inventario-container">
    <h1 class="main-title">Inventario</h1>

    <div class="table-container">
      <div class="table-scroll-wrapper">
        <table class="inventory-table">
          <thead>
            <tr>
              <th>Cant.</th>
              <th>Detalle</th>
              <th>Stock Inicial</th>
              <th>Salidas</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in inventario" :key="item.id">
              <td class="text-right">{{ item.cantidad }}</td>
              <td>{{ item.detalle }}</td>
              <td class="text-right">{{ item.stockInicial }}</td>
              <td class="text-right">{{ item.salidas }}</td>
              <td class="text-right fw-bold">{{ item.total }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="actions-container">
        <button class="btn btn-edit">
          <span>Editar</span>
          <img src="@/assets/Edit.png" alt="editar">
        </button>
      </div>
    </div>
  </main>
</template>
<script setup>
import { ref } from 'vue';

// Datos de ejemplo para el inventario.
// Esta es la información que luego conectarás con tu base de datos.
const inventario = ref([
  { id: 1, cantidad: 350, detalle: 'Sillas', stockInicial: 350, salidas: 25, total: 325 },
  { id: 2, cantidad: 10, detalle: 'Mesas rectangular de plastico', stockInicial: 10, salidas: 2, total: 8 },
  { id: 3, cantidad: 20, detalle: 'Mesas rectangular de madera', stockInicial: 20, salidas: 10, total: 10 },
  { id: 4, cantidad: 3, detalle: 'Toldos 6x4', stockInicial: 3, salidas: 1, total: 2 },
  { id: 5, cantidad: 40, detalle: 'Cajas de vasos Largos', stockInicial: 42, salidas: 4, total: 38 },
  { id: 6, cantidad: 4, detalle: 'Cajas de vasos cerveceros', stockInicial: 5, salidas: 2, total: 3 },
  { id: 7, cantidad: 5, detalle: 'Tenedores metalicos', stockInicial: 50, salidas: 13, total: 37 },
  { id: 8, cantidad: 53, detalle: 'Tenedores con mango de madera', stockInicial: 60, salidas: 7, total: 53 },
  { id: 9, cantidad: 4, detalle: 'Cuchillos con mando de madera', stockInicial: 40, salidas: 32, total: 8 },
  { id: 10, cantidad: 423, detalle: 'Cucharas metalicas', stockInicial: 450, salidas: 45, total: 405 },
  { id: 11, cantidad: 23, detalle: 'Sobremantel guindo', stockInicial: 25, salidas: 2, total: 23 },
  { id: 12, cantidad: 23, detalle: 'Sobremantel azul', stockInicial: 30, salidas: 7, total: 23 },
]);
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
  padding: 0.8rem 1rem;
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
</style>