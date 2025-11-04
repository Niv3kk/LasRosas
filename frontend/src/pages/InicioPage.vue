<template>
  <template v-if="usuarioActual">
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
        :vista="vistaActiva" 
        @cerrar="cerrarModal"
        @borrar="borrarPedido"
        @guardar="guardarPedidoEditado"
        @entregar="entregarPedido"
        @recoger="recogerPedido"
      />
  
      <!-- Esta era la línea 66 que daba el error. Ahora está protegida por el v-if padre -->
      <button v-if="usuarioActual.rol === 'Propietaria'" class="btn-crear-alquiler" @click="abrirCrearModal">
        <i class="bi bi-plus-lg"></i>
        <span>Crear Alquiler</span>
      </button>
      
      <CrearAlquilerModal
        v-if="crearModalVisible"
        :vista="vistaActiva"
        @cerrar="cerrarCrearModal"
        @guardar="guardarNuevoAlquiler"
      />
    </div>
  </template>

  <!-- Opcional: Mostrar un mensaje de "cargando" mientras 'usuarioActual' es null -->
  <template v-else>
    <div class="text-center p-5">
      Cargando datos del usuario...
    </div>
  </template>
</template>

<script setup>
import { ref, computed } from 'vue';
// Nota: Asegúrate de que esta ruta a tu store sea correcta.
// Si tu carpeta se llama 'store', la ruta es '@/store/auth.js'
import { usuarioActual } from '@/services/auth.js';
import DetallePedidoModal from '@/components/DetallePedidoModal.vue';
import CrearAlquilerModal from '@/components/CrearAlquilerModal.vue';

// --- ESTADO DE LA VISTA (TABS) ---
const vistaActiva = ref('pendientes');

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

// --- ESTADO DE LOS MODALES ---
const modalVisible = ref(false); // Para ver/editar
const pedidoSeleccionado = ref(null);
const crearModalVisible = ref(false); // Para crear

// --- LÓGICA DE FILTRADO ---
const pedidosFiltrados = computed(() => {
  return vistaActiva.value === 'pendientes' ? pedidosPendientes.value : pedidosPorRecoger.value;
});

// --- FUNCIONES PARA MODAL DE DETALLES/EDICIÓN ---
const abrirModal = (pedido) => {
  pedidoSeleccionado.value = pedido;
  modalVisible.value = true;
};

const cerrarModal = () => {
  modalVisible.value = false;
  pedidoSeleccionado.value = null;
};

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
  
  cerrarModal();
};

// --- FUNCIONES PARA MODAL DE CREACIÓN ---
const abrirCrearModal = () => {
  crearModalVisible.value = true;
};

const cerrarCrearModal = () => {
  crearModalVisible.value = false;
};

const guardarNuevoAlquiler = (nuevoPedido) => {
  // Le asignamos los datos que faltan (ID, N°, fecha y hora)
  nuevoPedido.id = `pedido_${Date.now()}`;
  nuevoPedido.numeroPedido = String(Math.floor(Math.random() * 10000));
  const hoy = new Date();
  nuevoPedido.fecha = hoy.toLocaleDateString('es-ES');
  nuevoPedido.hora = hoy.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });

  // ===== LÓGICA ACTUALIZADA =====
  // Verificamos qué pestaña está activa y guardamos en la lista correcta
  if (vistaActiva.value === 'pendientes') {
    pedidosPendientes.value.unshift(nuevoPedido);
  } else {
    pedidosPorRecoger.value.unshift(nuevoPedido);
  }
  
  // Cerramos el modal de creación
  cerrarCrearModal();
};
// ===== NUEVAS FUNCIONES PARA LA PROPIETARIA =====
const entregarPedido = (pedidoAEntregar) => {
  // 1. Quitar de la lista de pendientes
  pedidosPendientes.value = pedidosPendientes.value.filter(p => p.numeroPedido !== pedidoAEntregar.numeroPedido);
  
  // 2. Añadir a la lista por recoger
  pedidosPorRecoger.value.unshift(pedidoAEntregar);

  // 3. Cerrar el modal
  cerrarModal();
};

const recogerPedido = (pedidoARecoger) => {
  // 1. Quitar de la lista por recoger (se considera completado)
  pedidosPorRecoger.value = pedidosPorRecoger.value.filter(p => p.numeroPedido !== pedidoARecoger.numeroPedido);
  
  // (Aquí podrías añadirlo a una lista de historial si quisieras)

  // 2. Cerrar el modal
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
/* ===== ACTUALIZACIÓN 3: Estilo completo para el botón flotante ===== */
.btn-crear-alquiler {
  position: fixed; /* Lo saca del flujo normal del documento */
  bottom: 2rem;    /* Lo posiciona a 2rem del borde inferior */
  right: 2rem;     /* Lo posiciona a 2rem del borde derecho */
  z-index: 100;    /* Se asegura de que esté por encima de otro contenido */
  
  background-color: #1B4F86; /* Tu color azul oscuro */
  color: white;
  border: none;
  border-radius: 10px; /* Lo hace redondeado (forma de píldora) */
  padding: 0.8rem 1.5rem;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  transition: all 0.2s ease-in-out;
}
.btn-crear-alquiler:hover {
  transform: scale(1.05); /* Un pequeño efecto al pasar el mouse */
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}
.btn-crear-alquiler i {
  font-size: 1.2rem;
}

/* Ajuste responsivo para que no esté tan pegado a los bordes en móviles */
@media (max-width: 768px) {
  .btn-crear-alquiler {
    bottom: 1rem;
    right: 1rem;
  }
}
</style>