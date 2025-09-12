<template>
  <div>
    <div class="d-flex align-items-center mb-3">
      <h2 
        class="section-title mb-0 flex-grow-1"
        :class="{ 'active-title': vistaActiva === 'pendientes' }"
        @click="vistaActiva = 'pendientes'">
        Pedidos Pendientes
      </h2>
      
      <h2 
        class="section-title mb-0 flex-grow-1"
        :class="{ 'active-title': vistaActiva === 'porRecoger' }"
        @click="vistaActiva = 'porRecoger'">
        <span class="alt">Pedidos Por Recoger</span>
      </h2>
    </div>

    <div class="card card-soft mb-3 p-4" v-for="(p, i) in pedidosFiltrados" :key="i">
      <div class="row g-0 align-items-center">
        <div class="col-md-3">
          <div class="fw-semibold">Pedido de: {{ p.cliente }}</div>
          <div>Ubicación: {{ p.ubicacion }}</div>
          <div class="mt-2 text-muted small">{{ p.fecha }}</div>
          <div class="mt-2">
            <span class="fw-semibold">Estado:</span>
            <span class="badge" :class="p.pagado ? 'badge-success' : 'badge-danger'">
              {{ p.pagado ? 'Pagado' : 'Por Pagar' }}
            </span>
          </div>
        </div>
        <div class="col-md-3 small detalles-borde">
          <div class="row">
            <div class="col-4 fw-semibold">Cant.</div>
            <div class="col-8 fw-semibold">Detalle</div>
            <template v-for="(d, idx) in p.detalle" :key="idx">
              <div class="col-4">{{ d.cant }}</div>
              <div class="col-8">{{ d.item }}</div>
            </template>
          </div>
        </div>
        <div class="col-md-6 text-center">
          <button class="btn btn-green">
            Revisar
            <img src="@/assets/Revisar.png" alt="Revisar pedido">
          </button>
        </div>
      </div>
    </div>

    <div v-if="pedidosFiltrados.length === 0" class="text-center text-muted mt-5">
      <p>No hay pedidos en esta sección.</p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// 1. Variable para saber qué vista está activa
const vistaActiva = ref('pendientes'); // Inicia mostrando los pendientes

// 2. Datos separados para cada lista
const pedidosPendientes = [
  {
    cliente: 'Andrea Garnica',
    ubicacion: 'Urb. Del Valle #12',
    fecha: '14/09/2024',
    pagado: true,
    detalle: [
      { cant: 50, item: 'Mesas' },
      { cant: 600, item: 'Sillas' },
    ],
  },
   {
    cliente: 'Juan Perez',
    ubicacion: 'Av. Heroínas #456',
    fecha: '15/09/2024',
    pagado: false,
    detalle: [
      { cant: 20, item: 'Manteles' },
    ],
  },
];

const pedidosPorRecoger = [
  {
    cliente: 'Maria Lopez',
    ubicacion: 'Calle Lanza #789',
    fecha: '12/09/2024',
    pagado: true,
    detalle: [
      { cant: 100, item: 'Vasos' },
      { cant: 100, item: 'Platos' },
    ],
  },
];

// 3. Propiedad computada: una lista "inteligente" que cambia según la vistaActiva
const pedidosFiltrados = computed(() => {
  if (vistaActiva.value === 'pendientes') {
    return pedidosPendientes;
  } else {
    return pedidosPorRecoger;
  }
});
</script>

<style scoped>
.section-title {
  text-align: center;
  padding-bottom: 10px;
  cursor: pointer; /* Indica que se puede hacer clic */
  border-bottom: 3px solid transparent; /* Borde invisible por defecto */
  transition: border-color 0.3s;
  color: black;
}

/* Estilo para el título que está activo */
.active-title {
  color: #c9434d; /* Un color de acento, puedes cambiarlo */
  border-bottom-color: #c9434d; /* Muestra el borde del color de acento */
}

.detalles-borde {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 12px;
}

.btn {
  background-color: #2ABB68;
  color: white;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 80px;
}

img {
  height: 22px;
}
.btn-green:hover {
  background-color: #24a05c;
  border-color: #24a05c;
  color: white;
}


</style>