<template>
  <div>
    <div class="d-flex flex-column flex-md-row align-items-center mb-3">
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

    <div class="card card-soft mb-3 p-4" v-for="p in pedidosFiltrados" :key="p.numeroPedido">
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
          <button class="btn btn-green" @click="abrirModal(p)">
            Revisar
            <img src="@/assets/Revisar.png" alt="Revisar pedido">
          </button>
        </div>
      </div>
    </div>

    <div v-if="pedidosFiltrados.length === 0" class="text-center text-muted mt-5">
      <p>No hay pedidos en esta sección.</p>
    </div>

    <DetallePedidoModal 
      v-if="modalVisible" 
      :pedido="pedidoSeleccionado"
      @cerrar="cerrarModal"
      @borrar="borrarPedido"
      @guardar="guardarPedidoEditado"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import DetallePedidoModal from '@/components/DetallePedidoModal.vue';

// --- ESTADO DE LA VISTA ---
const vistaActiva = ref('pendientes');

// --- ESTADO DEL MODAL ---
const modalVisible = ref(false);
const pedidoSeleccionado = ref(null);

// --- DATOS DE EJEMPLO ---
const pedidosPendientes = ref([
  {
    cliente: 'Andrea Garnica',
    ubicacion: 'Urb. Del Valle #12',
    fecha: '14/09/2025',
    hora: '10:30 AM',
    pagado: true,
    celular1: '123456789',
    celular2: '76839233',
    numeroPedido: '2345',
    fechaEntrega: '21/09/2025',
    fechaRecojo: '22/09/2025',
    garantia: true,
    direccion: 'Pronto Gas, Av. Villazon Km2 acera sud',
    granTotal: 780,
    detalle: [
      { cant: 12, item: 'Mesas', precioUnitario: 25, total: 300 },
      { cant: 120, item: 'Sillas', precioUnitario: 2, total: 240 },
      { cant: 12, item: 'Manteles', precioUnitario: 10, total: 120 },
      { cant: 12, item: 'Sobremanteles color celeste', precioUnitario: 10, total: 120 },
    ],
  },
]);

const pedidosPorRecoger = ref([
  {
    cliente: 'Maria Lopez',
    ubicacion: 'Calle Lanza #789',
    fecha: '12/09/2025',
    hora: '04:00 PM',
    pagado: true,
    celular1: '77778888',
    celular2: '66665555',
    numeroPedido: '2346',
    fechaEntrega: '10/09/2025',
    fechaRecojo: '12/09/2025',
    garantia: false,
    direccion: 'Salón de eventos "El Molino", zona norte',
    granTotal: 250,
    detalle: [
      { cant: 100, item: 'Vasos', precioUnitario: 1, total: 100 },
      { cant: 100, item: 'Platos', precioUnitario: 1.5, total: 150 },
    ],
  },
]);

// --- LÓGICA DE FILTRADO ---
const pedidosFiltrados = computed(() => {
  return vistaActiva.value === 'pendientes' ? pedidosPendientes.value : pedidosPorRecoger.value;
});

// --- FUNCIONES DEL MODAL ---
const abrirModal = (pedido) => {
  pedidoSeleccionado.value = pedido;
  modalVisible.value = true;
};

const cerrarModal = () => {
  modalVisible.value = false;
  pedidoSeleccionado.value = null;
};

// --- FUNCIONES PARA BORRAR Y GUARDAR ---
const borrarPedido = (idPedido) => {
  if (confirm('¿Estás seguro de que quieres borrar este pedido?')) {
    if (vistaActiva.value === 'pendientes') {
      pedidosPendientes.value = pedidosPendientes.value.filter(p => p.numeroPedido !== idPedido);
    } else {
      pedidosPorRecoger.value = pedidosPorRecoger.value.filter(p => p.numeroPedido !== idPedido);
    }
    cerrarModal();
  }
};

const guardarPedidoEditado = (pedidoEditado) => {
  const actualizarLista = (lista) => {
    const index = lista.findIndex(p => p.numeroPedido === pedidoEditado.numeroPedido);
    if (index !== -1) {
      lista[index] = pedidoEditado;
    }
    return lista;
  };

  if (vistaActiva.value === 'pendientes') {
    pedidosPendientes.value = actualizarLista(pedidosPendientes.value);
  } else {
    pedidosPorRecoger.value = actualizarLista(pedidosPorRecoger.value);
  }
  
  // Cerramos el modal después de guardar
  cerrarModal();
};
</script>
<style scoped>
/* Tu CSS se mantiene exactamente igual, no necesita cambios */
.section-title {
  text-align: center;
  padding-bottom: 10px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: border-color 0.3s;
  color: black;
}
.active-title {
  color: #c9434d;
  border-bottom-color: #c9434d;
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
  padding: 5px 55px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
img {
  height: 22px;
}
.btn-green:hover {
  background-color: #24a05c;
  border-color: #24a05c;
  color: white;
}
/* Para el botón "Revisar" */
.btn-green:active,
.btn-green:focus {
  background-color: #2ABB68 !important; 
  border-color: #2ABB68 !important;
  box-shadow: none !important; 
}


</style>