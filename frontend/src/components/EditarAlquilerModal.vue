<template>
  <div class="modal-overlay" @click="onOverlayClick">
    <div
      class="modal-content"
      role="dialog"
      aria-modal="true"
      :aria-labelledby="'editar-alquiler-titulo'"
      @click.stop
    >
      <h2 id="editar-alquiler-titulo" class="modal-title">{{ tituloModal }}</h2>

      <!-- ======= VISTA SOLO LECTURA ======= -->
      <div v-if="!enModoEdicion" class="modal-body">
        <!-- Acordeón compacto en móvil -->
        <details class="accordion" :open="!isCompact">
          <summary>Datos del cliente</summary>
          <div class="modal-header-info">
            <div>
              <div class="fw-bold">Alquiler de: {{ alquiler.cliente }}</div>
              <div>Celular 1: <strong>{{ alquiler.celular1 }}</strong></div>
              <div>Celular 2: <strong>{{ alquiler.celular2 }}</strong></div>
            </div>
            <div class="text-end">
              <div>Fecha actual: <strong>{{ new Date().toLocaleDateString('es-ES') }}</strong></div>
              <div>N° <strong>{{ alquiler.numeroPedido }}</strong></div>
            </div>
          </div>
        </details>

        <div class="modal-dates">
          Fecha de entrega: <strong>{{ alquiler.fechaEntrega }}</strong> /
          Fecha de recojo: <strong>{{ alquiler.fechaRecojo }}</strong>
        </div>

        <div class="table-scroll-wrapper">
          <table class="modal-table responsive-table">
            <thead>
              <tr>
                <th>Cant.</th><th>Detalle</th><th>P/Unit</th><th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in alquiler.detalle" :key="idx">
                <td data-label="Cant." class="text-center">{{ item.cant }}</td>
                <td data-label="Detalle">{{ item.item }}</td>
                <td data-label="P/Unit" class="text-end">{{ item.precioUnitario }} Bs.</td>
                <td data-label="Total" class="text-end fw-bold">{{ item.total }} Bs.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <details class="accordion" :open="!isCompact">
          <summary>Totales y dirección</summary>
          <div class="modal-footer-info">
            <div class="garantia">
              <input type="checkbox" :checked="alquiler.garantia" disabled>
              <label>Garantía:</label>
            </div>
            <div class="total-final">
              Total: <strong>{{ alquiler.granTotal }} Bs.</strong>
            </div>
          </div>
          <div class="direccion">
            Dirección: <strong>{{ alquiler.direccion }}</strong>
          </div>
        </details>
      </div>

      <!-- ======= VISTA EDICIÓN ======= -->
      <div v-else class="modal-body">
        <!-- Acordeón compacto en móvil -->
        <details class="accordion" :open="!isCompact">
          <summary>Datos del cliente y fechas</summary>
          <div class="modal-header-info editable-section">
            <div>
              <label>Alquiler de:</label>
              <input type="text" v-model="alquilerEditable.cliente" autocomplete="name">
              <label>Celular 1:</label>
              <input type="tel" inputmode="numeric" v-model="alquilerEditable.celular1" autocomplete="tel">
              <label>Celular 2:</label>
              <input type="tel" inputmode="numeric" v-model="alquilerEditable.celular2" autocomplete="tel">
            </div>
            <div class="text-end">
              <label>Fecha de entrega:</label>
              <input type="date" v-model="alquilerEditable.fechaEntrega">
              <label>Fecha de recojo:</label>
              <input type="date" v-model="alquilerEditable.fechaRecojo">
            </div>
          </div>
        </details>

        <div class="table-scroll-wrapper">
          <table class="modal-table responsive-table">
            <thead>
              <tr><th>Cant.</th><th>Detalle</th><th>P/Unit</th><th>Total</th><th></th></tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in alquilerEditable.detalle" :key="idx">
                <td data-label="Cant.">
                  <input class="input-table" type="number" inputmode="numeric" v-model="item.cant" @input="actualizarTotales">
                </td>
                <td data-label="Detalle">
                  <input class="input-table" type="text" v-model="item.item">
                </td>
                <td data-label="P/Unit">
                  <input class="input-table" type="number" inputmode="decimal" v-model="item.precioUnitario" @input="actualizarTotales">
                </td>
                <td data-label="Total" class="text-end fw-bold">{{ item.total }} Bs.</td>
                <td class="action-cell">
                  <button class="btn-remove-item" @click="quitarItemDetalle(idx)" aria-label="Quitar item">-</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <button class="btn-add-item" @click="agregarItemDetalle">+ Añadir item</button>

        <details class="accordion" :open="!isCompact">
          <summary>Totales y dirección</summary>
          <div class="modal-footer-info">
            <div class="garantia">
              <input type="checkbox" v-model="alquilerEditable.garantia" id="chkGarantia">
              <label for="chkGarantia">Garantía:</label>
            </div>
            <div class="total-final">
              Total: <strong>{{ alquilerEditable.granTotal }} Bs.</strong>
            </div>
          </div>

          <div class="direccion editable-section">
            <label>Dirección:</label>
            <input type="text" v-model="alquilerEditable.direccion" autocomplete="street-address">
          </div>
        </details>

        <div class="modal-actions" :class="{'no-sticky': isShortHeight}">
          <button class="btn btn-cancel" @click="$emit('cerrar')">Cancelar</button>
          <button class="btn btn-save" @click="guardarCambios">Guardar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  alquiler: { type: Object, required: true },
  rol: { type: String, required: true }
});

const emit = defineEmits(['cerrar', 'borrar', 'guardar']);

// Modo de edición según rol
const enModoEdicion = ref(props.rol === 'Administrador');

// Clon editable
const alquilerEditable = ref(null);

// Título dinámico
const tituloModal = computed(() => enModoEdicion.value ? 'Editar Alquiler' : 'Detalle del Alquiler');

// Responsive flags (se actualizan en resize)
const isCompact = ref(false);     // pantallas angostas (≤430px)
const isShortHeight = ref(false); // pantallas bajas (≤700px)

const syncViewportFlags = () => {
  if (typeof window !== 'undefined') {
    isCompact.value = window.matchMedia('(max-width: 430px)').matches;
    isShortHeight.value = window.matchMedia('(max-height: 700px)').matches;
  }
};

// Sincroniza prop -> editable
watch(() => props.alquiler, (nuevoValor) => {
  if (nuevoValor) {
    alquilerEditable.value = JSON.parse(JSON.stringify(nuevoValor));
  }
}, { immediate: true, deep: true });

// Cerrar con overlay solo si no se edita
const onOverlayClick = () => { if (!enModoEdicion.value) emit('cerrar'); };

// Guardar
const guardarCambios = () => {
  alquilerEditable.value.ubicacion = alquilerEditable.value.direccion;
  emit('guardar', alquilerEditable.value);
};

// Detalle: agregar/quitar y totales
const agregarItemDetalle = () => {
  if (alquilerEditable.value && alquilerEditable.value.detalle) {
    alquilerEditable.value.detalle.push({ cant: 1, item: '', precioUnitario: 0, total: 0 });
  }
};
const quitarItemDetalle = (index) => {
  if (alquilerEditable.value && alquilerEditable.value.detalle) {
    alquilerEditable.value.detalle.splice(index, 1);
    actualizarTotales();
  }
};
const actualizarTotales = () => {
  let nuevoGranTotal = 0;
  if (alquilerEditable.value && alquilerEditable.value.detalle) {
    alquilerEditable.value.detalle.forEach(item => {
      item.total = (Number(item.cant) || 0) * (Number(item.precioUnitario) || 0);
      nuevoGranTotal += item.total;
    });
    alquilerEditable.value.granTotal = nuevoGranTotal;
  }
};

// Bloqueo de scroll del documento mientras el modal está abierto
onMounted(() => {
  const html = document.documentElement;
  html.dataset.prevOverflow = html.style.overflow;
  html.style.overflow = 'hidden';

  syncViewportFlags();
  window.addEventListener('resize', syncViewportFlags, { passive: true });
});
onBeforeUnmount(() => {
  const html = document.documentElement;
  html.style.overflow = html.dataset.prevOverflow || '';
  delete html.dataset.prevOverflow;

  window.removeEventListener('resize', syncViewportFlags);
});
</script>

<style scoped>
/* Base */
.modal-overlay {
  position: fixed; inset: 0;
  min-height: 100dvh;
  background-color: rgba(0,0,0,0.6);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000; padding: 10px;
}

.modal-content {
  background: #fff;
  width: min(100%, 720px);
  max-width: 800px;
  max-height: calc(100svh - 20px);
  display: flex; flex-direction: column;
  border-radius: 16px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  padding: clamp(10px, 2.5vw, 20px);
  padding-bottom: calc(clamp(10px, 2.5vw, 20px) + env(safe-area-inset-bottom, 0px));
}

.modal-title { text-align: center; font-size: clamp(1.1rem, 2.5vw, 1.5rem); margin-bottom: 6px; }

/* Contenido scrollable real */
.modal-body { flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; }

/* Acordeones */
.accordion {
  border: 1px solid #eee; border-radius: 10px; background: #fafafa;
  padding: 0.25rem 0.5rem; margin-bottom: 8px;
}
.accordion > summary {
  cursor: pointer; font-weight: 700; list-style: none; outline: none;
  padding: 0.35rem 0.2rem; user-select: none;
}
.accordion[open] { background: #f7f7f7; }
.accordion > summary::-webkit-details-marker { display: none; }

.table-scroll-wrapper {
  overflow: auto; flex: 1 1 auto; margin-bottom: 0.5rem; min-height: 0;
}
.modal-table { width: 100%; border-collapse: collapse; }
.modal-table thead th { position: sticky; top: 0; background-color: white; z-index: 1; }
.modal-table th, .modal-table td { padding: 0.45rem; border-bottom: 1px solid #eee; }

/* Bloques */
.modal-header-info {
  display: grid; gap: 8px; text-align: center; margin-bottom: 4px;
  background: #f7f7f7; padding: 8px; border-radius: 10px;
}
.modal-dates { text-align: center; margin: 0.25rem 0 0.5rem; font-size: 0.95rem; }

.modal-footer-info {
  display: grid; gap: 8px; align-items: center; justify-items: center;
  margin-top: 4px;
}
.garantia { display: inline-flex; align-items: center; gap: 0.5rem; }
.total-final { font-size: clamp(1rem, 2.3vw, 1.2rem); font-weight: 700; }

.direccion {
  background: #f7f7f7; padding: 8px; border-radius: 10px;
  margin-top: 4px; text-align: center; word-break: break-word;
}

/* Acciones */
.modal-actions {
  display: grid; grid-template-columns: 1fr; gap: 6px; margin-top: 10px;
  position: sticky; bottom: 0;
  padding-top: 6px;
  background: linear-gradient(to top, #fff, rgba(255,255,255,0.7));
}
.modal-actions.no-sticky { position: static; background: none; padding-top: 0; }

.btn {
  border: none; border-radius: 10px;
  padding: 0.85rem 1rem;
  color: #fff; cursor: pointer; display: inline-flex;
  justify-content: center; align-items: center; gap: 0.5rem; font-weight: 700;
  touch-action: manipulation;
  
}
.btn-cancel { background-color: #757575; }
.btn-save   { background-color: #2196F3; }
.btn-cancel:active,
.btn-cancel:focus {
  background-color: #757575 !important; 
  border-color: #757575 !important;
  box-shadow: none !important; 
}
.btn-save:active,
.btn-save:focus {
  background-color: #2196F3 !important; 
  border-color: #2196F3 !important;
  box-shadow: none !important; 
}

/* Inputs */
.editable-section label { display: block; font-weight: 600; font-size: 0.85rem; margin-top: 0.4rem; color: #555; }
.editable-section input, .input-table {
  width: 100%; padding: 0.55rem 0.65rem;
  border: 1px solid #ccc; border-radius: 8px; font-size: 1rem;
}

/* Botones tabla */
.btn-add-item {
  background: #eef1f3; color: #333; border: 1px solid #ddd;
  border-radius: 8px; padding: 0.55rem 0.9rem; cursor: pointer; margin-top: 0.25rem;
  align-self: start;
}
.btn-remove-item {
  background: #fbe9e7; color: #E53935; border: none; border-radius: 50%;
  width: 30px; height: 30px; cursor: pointer; font-weight: 800; line-height: 1;
}

/* ------- Móvil (≤ 430px) ------- */
@media (max-width: 430px) {
  /* Tabla en tarjetas */
  .responsive-table thead { display: none; }
  .responsive-table, .responsive-table tbody, .responsive-table tr, .responsive-table td { display: block; width: 100%; }
  .responsive-table tr {
    border: 1px solid #eee; border-radius: 10px; padding: 8px; margin-bottom: 8px; background: #fff;
  }
  .responsive-table td { border: none; padding: 6px 2px; position: relative; text-align: left !important; }
  .responsive-table td::before {
    content: attr(data-label);
    font-weight: 700; display: block; margin-bottom: 2px; opacity: 0.7; font-size: 0.85rem;
  }
  .responsive-table .action-cell { display: flex; justify-content: flex-end; }

  /* Compactar paddings para ganar alto visible */
  .btn { padding-block: 0.9rem; }
}

/* ------- Tablet+ ------- */
@media (min-width: 768px) {
  .modal-content { padding: 2rem; }
  .modal-title { font-size: 1.6rem; }
  .accordion { padding: 0.4rem 0.75rem; }
  .modal-header-info { grid-auto-flow: column; grid-auto-columns: 1fr; text-align: left; }
  .modal-footer-info { grid-auto-flow: column; grid-auto-columns: 1fr; }
  .total-final { font-size: 1.3rem; }
  .direccion { text-align: left; }
  .modal-actions { grid-template-columns: repeat(2, minmax(0, 1fr)); position: static; background: none; }
  .responsive-table thead { display: table-header-group; }
  .responsive-table tr { display: table-row; border: none; margin: 0; padding: 0; }
  .responsive-table td { display: table-cell; padding-left: 0.75rem; position: static; border-bottom: 1px solid #eee; }
  .responsive-table td::before { content: none; }
  .responsive-table .text-center { text-align: center !important; }
  .responsive-table .text-end { text-align: right !important; }
}

/* ------- Alturas bajas: evita sticky para ganar alto ------- */
@media (max-height: 700px) {
  .modal-actions { position: static; background: none; padding-top: 0; }
}
</style>
