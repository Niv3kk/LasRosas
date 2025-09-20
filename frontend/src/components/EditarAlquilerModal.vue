<template>
  <div class="modal-overlay" @click="onOverlayClick">
    <div class="modal-content" @click.stop>
      <h2 class="modal-title">Detalle del Alquiler</h2>

      <div v-if="!enModoEdicion" class="modal-body">
        
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

        <div class="modal-dates">
          Fecha de entrega: <strong>{{ alquiler.fechaEntrega }}</strong> / 
          Fecha de recojo: <strong>{{ alquiler.fechaRecojo }}</strong>
        </div>

        <div class="table-scroll-wrapper">
          <table class="modal-table responsive-table">
            <thead>
              <tr>
                <th>Cant.</th>
                <th>Detalle</th>
                <th>P/Unit</th>
                <th>Total</th>
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
        
        <div class="modal-actions" v-if="rol === 'Administrador'">
          <button class="btn btn-edit" @click="entrarModoEdicion">
            <span>Editar</span><img src="@/assets/Edit.png" alt="editar">
          </button>
          <button class="btn btn-delete" @click="$emit('borrar', alquiler.id)">
            <span>Borrar</span><img src="@/assets/Delete.png" alt="borrar">
          </button>
        </div>
      </div>

      <div v-else class="modal-body">
        <div class="editable-section">
          <label>Alquiler de:</label>
          <input type="text" v-model="alquilerEditable.cliente">
          <label>Ubicación:</label>
          <input type="text" v-model="alquilerEditable.ubicacion">
          <label>Fecha:</label>
          <input type="text" v-model="alquilerEditable.fecha">
        </div>
        <div class="table-scroll-wrapper">
          </div>
        <button class="btn-add-item" @click="agregarItemDetalle">+ Añadir item</button>
        <div class="modal-actions">
          <button class="btn btn-cancel" @click="cancelarEdicion">Cancelar</button>
          <button class="btn btn-save" @click="guardarCambios">Guardar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  alquiler: { type: Object, required: true },
  rol: { type: String, required: true }
});

const emit = defineEmits(['cerrar', 'borrar', 'guardar']);

const enModoEdicion = ref(false);
const alquilerEditable = ref(null);

watch(() => props.alquiler, (nuevoValor) => {
  if (nuevoValor) {
    alquilerEditable.value = JSON.parse(JSON.stringify(nuevoValor));
  }
}, { immediate: true, deep: true });

const onOverlayClick = () => {
  if (!enModoEdicion.value) {
    emit('cerrar');
  }
};
const entrarModoEdicion = () => {
  enModoEdicion.value = true;
};
const cancelarEdicion = () => {
  enModoEdicion.value = false;
};
const guardarCambios = () => {
  alquilerEditable.value.ubicacion = alquilerEditable.value.direccion;
  emit('guardar', alquilerEditable.value);
  enModoEdicion.value = false;
};
const agregarItemDetalle = () => {
  alquilerEditable.value.detalle.push({ cant: 1, item: '', precioUnitario: 0, total: 0 });
};
const quitarItemDetalle = (index) => {
  alquilerEditable.value.detalle.splice(index, 1);
};
</script>

<style scoped>
/* Estilos generales del modal (Móvil Primero) */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 1rem; }
.modal-content { background: white; padding: 1rem; border-radius: 15px; width: 100%; max-width: 800px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); max-height: 90vh; display: flex; flex-direction: column; }
.modal-body { flex-grow: 1; overflow: hidden; display: flex; flex-direction: column; }
.table-scroll-wrapper { overflow-y: auto; flex-grow: 1; margin-bottom: 1rem; }
.modal-table thead th { position: sticky; top: 0; background-color: white; z-index: 1; }
.modal-title { text-align: center; font-size: 1.5rem; margin-bottom: 1rem; }
.modal-header-info { display: flex; flex-direction: column; gap: 1rem; text-align: center; margin-bottom: 1rem; background: #f7f7f7; padding: 1rem; border-radius: 8px; }
.modal-dates { text-align: center; margin: 1rem 0; font-size: 1rem; }
.modal-table { width: 100%; border-collapse: collapse; }
.modal-table th, .modal-table td { padding: 0.5rem; border-bottom: 1px solid #eee; }
.modal-footer-info { display: flex; flex-direction: column; gap: 1rem; align-items: center; margin-top: 1rem; }
.garantia { display: flex; align-items: center; gap: 0.5rem; }
.total-final { font-size: 1.2rem; font-weight: bold; }
.direccion { background: #f7f7f7; padding: 1rem; border-radius: 8px; margin-top: 1rem; text-align: center; }
.modal-actions { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 1.5rem; }
.btn { border: none; border-radius: 8px; padding: 0.75rem 1.5rem; color: white; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 0.5rem; font-weight: 600; }

/* ... (otros estilos de botones y responsivos) ... */

/* Tabla Responsiva */
.responsive-table thead { display: none; }
.responsive-table tr { display: block; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 1rem; padding: 0.5rem; }
.responsive-table td { display: block; text-align: right !important; padding-left: 50%; position: relative; border-bottom: 1px dotted #eee; }
.responsive-table td:last-child { border-bottom: none; }
.responsive-table td:before { content: attr(data-label); position: absolute; left: 10px; width: 45%; padding-right: 10px; text-align: left; font-weight: bold; }

/* Estilos para PC (a partir de 768px) */
@media (min-width: 768px) {
  .modal-content { padding: 2rem; }
  .modal-title { font-size: 1.8rem; }
  .modal-header-info { flex-direction: row; justify-content: space-between; text-align: left; }
  .modal-dates { font-size: 1.2rem; }
  .modal-footer-info { flex-direction: row; justify-content: space-between; }
  .total-final { font-size: 1.5rem; }
  .direccion { text-align: left; }
  .modal-actions { flex-direction: row; justify-content: center; }
  .responsive-table thead { display: table-header-group; }
  .responsive-table tr { display: table-row; border: none; margin-bottom: 0; padding: 0; }
  .responsive-table td { display: table-cell; text-align: left !important; padding-left: 0.75rem; position: static; border-bottom: 1px solid #eee; }
  .responsive-table .text-center { text-align: center !important; }
  .responsive-table .text-end { text-align: right !important; }
  .responsive-table td:before { content: none; }
}
</style>