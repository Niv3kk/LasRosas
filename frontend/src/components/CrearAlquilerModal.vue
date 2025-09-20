<template>
  <div class="modal-overlay">
    <div class="modal-content" @click.stop>
      <h2 class="modal-title">Crear Nuevo Alquiler</h2>
      
      <div class="form-scroll-wrapper">
        <fieldset class="form-section">
          <legend>Información del Cliente</legend>
          <div class="form-grid">
            <div>
              <label for="cliente">Nombre del Cliente:</label>
              <input id="cliente" type="text" v-model="nuevoPedido.cliente" placeholder="Nombre completo">
            </div>
            <div>
              <label for="direccion">Dirección:</label>
              <input id="direccion" type="text" v-model="nuevoPedido.direccion" placeholder="Ej: Av. Villazon Km2">
            </div>
            <div>
              <label for="celular1">Celular 1:</label>
              <input id="celular1" type="text" v-model="nuevoPedido.celular1">
            </div>
            <div>
              <label for="celular2">Celular 2:</label>
              <input id="celular2" type="text" v-model="nuevoPedido.celular2">
            </div>
          </div>
        </fieldset>

        <fieldset class="form-section">
          <legend>Fechas del Alquiler</legend>
          <div class="form-grid">
            <div>
              <label for="fechaEntrega">Fecha de Entrega:</label>
              <input id="fechaEntrega" type="date" v-model="nuevoPedido.fechaEntrega">
            </div>
            <div>
              <label for="fechaRecojo">Fecha de Recojo:</label>
              <input id="fechaRecojo" type="date" v-model="nuevoPedido.fechaRecojo">
            </div>
          </div>
        </fieldset>

        <fieldset class="form-section">
          <legend>Detalle del Pedido</legend>
          <table class="modal-table">
            <thead><tr><th>Cant.</th><th>Detalle</th><th>P/Unit</th><th>Total</th><th></th></tr></thead>
            <tbody>
              <tr v-for="(item, index) in nuevoPedido.detalle" :key="index">
                <td><input class="input-table" type="number" v-model="item.cant" @input="actualizarTotales"></td>
                <td><input class="input-table" type="text" v-model="item.item"></td>
                <td><input class="input-table" type="number" v-model="item.precioUnitario" @input="actualizarTotales"></td>
                <td class="text-right fw-bold">{{ item.total }} Bs.</td>
                <td class="action-cell"><button class="btn-remove-item" @click="quitarItemDetalle(index)">-</button></td>
              </tr>
            </tbody>
          </table>
          <button class="btn-add-item" @click="agregarItemDetalle">+ Añadir item</button>
        </fieldset>

        <div class="footer-info">
          <div class="garantia">
            <input type="checkbox" id="garantia" v-model="nuevoPedido.garantia">
            <label for="garantia">Deja Garantía</label>
          </div>
          <div class="total-final">
            Total: <strong>{{ nuevoPedido.granTotal }} Bs.</strong>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-cancel" @click="$emit('cerrar')">Cancelar</button>
        <button class="btn btn-save" @click="guardar">Guardar Alquiler</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['cerrar', 'guardar']);

// Función para inicializar un objeto de pedido vacío
const inicializarPedido = () => ({
  cliente: '',
  ubicacion: '',
  direccion: '',
  celular1: '',
  celular2: '',
  fechaEntrega: '',
  fechaRecojo: '',
  garantia: false,
  pagado: false,
  detalle: [{ cant: 1, item: '', precioUnitario: 0, total: 0 }],
  granTotal: 0,
});

const nuevoPedido = ref(inicializarPedido());

const actualizarTotales = () => {
  let nuevoGranTotal = 0;
  nuevoPedido.value.detalle.forEach(item => {
    item.total = (Number(item.cant) || 0) * (Number(item.precioUnitario) || 0);
    nuevoGranTotal += item.total;
  });
  nuevoPedido.value.granTotal = nuevoGranTotal;
};

const agregarItemDetalle = () => {
  nuevoPedido.value.detalle.push({ cant: 1, item: '', precioUnitario: 0, total: 0 });
};

const quitarItemDetalle = (index) => {
  nuevoPedido.value.detalle.splice(index, 1);
  actualizarTotales();
};

const guardar = () => {
  if (!nuevoPedido.value.cliente) {
    alert('Por favor, ingresa el nombre del cliente.');
    return;
  }
  // Sincronizamos ubicacion con direccion antes de guardar
  nuevoPedido.value.ubicacion = nuevoPedido.value.direccion;
  emit('guardar', nuevoPedido.value);
};
</script>

<style scoped>
/* Estilos del modal optimizados */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 1rem; }
.modal-content { background: white; padding: 1rem; border-radius: 15px; width: 100%; max-width: 800px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); max-height: 90vh; display: flex; flex-direction: column; }
.modal-title { text-align: center; font-size: 1.5rem; margin-bottom: 1rem; color: #333; }
.form-scroll-wrapper { overflow-y: auto; flex-grow: 1; padding: 0 1rem; }
.form-section { border: 1px solid #eee; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
.form-section legend { font-weight: 600; padding: 0 0.5rem; }
.form-grid { display: grid; grid-template-columns: 1fr; gap: 0.5rem; }
.btn-save:active,

.btn-save:focus {
  background-color: #2196F3 !important; 
  border-color: #2196F3 !important;
  box-shadow: none !important;
}
.btn-cancel:active,
.btn-cancel:focus{
  background-color: #757575 !important;
  border-color: #757575 !important;
  box-shadow:none !important;
}
@media (min-width: 768px) {
  .modal-content { padding: 2rem; }
  .modal-title { font-size: 1.8rem; }
  .form-grid { grid-template-columns: 1fr 1fr; gap: 1rem; }
}
.form-section label { font-weight: 600; font-size: 0.9rem; color: #555; display: block; margin-bottom: 0.25rem; }
.form-section input, .form-section select { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
.modal-table { width: 100%; border-collapse: collapse; }
.modal-table th, .modal-table td { padding: 0.5rem; text-align: left; }
.input-table { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; }
.btn-add-item { background: #eef1f3; color: #333; border: 1px solid #ddd; border-radius: 6px; padding: 0.5rem 1rem; cursor: pointer; margin-top: 1rem; }
.btn-remove-item { background: #fbe9e7; color: #E53935; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; font-weight: bold; }
.footer-info { display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding: 1rem; background: #f7f7f7; border-radius: 8px; }
.garantia { display: flex; align-items: center; gap: 0.5rem; }
.total-final { font-size: 1.2rem; font-weight: bold; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; }
.btn-cancel { background-color: #757575; color: white; border: none; border-radius: 8px; padding: 0.75rem 1.5rem; cursor: pointer; }
.btn-save { background-color: #2196F3; color: white; border: none; border-radius: 8px; padding: 0.75rem 1.5rem; cursor: pointer; }
</style>