<template>
  <div class="modal-overlay" @click="onOverlayClick">
    <div class="modal-content" @click.stop>
      
      <h2 class="modal-title">Detalle del Pedido</h2>
      
      <div v-if="!enModoEdicion" class="modal-body">
        <div class="modal-header-info">
          <div>
            <div class="fw-bold">Pedido de: {{ pedido.cliente }}</div>
            <div>Celular 1: <strong>{{ pedido.celular1 }}</strong></div>
            <div>Celular 2: <strong>{{ pedido.celular2 }}</strong></div>
          </div>
          <div class="text-end">
            <div>Fecha actual: <strong>{{ new Date().toLocaleDateString('es-ES') }}</strong></div>
            <div>N° <strong>{{ pedido.numeroPedido }}</strong></div>
          </div>
        </div>
        <div class="modal-dates">
          Fecha de entrega: <strong>{{ pedido.fechaEntrega }}</strong> / 
          Fecha de recojo: <strong>{{ pedido.fechaRecojo }}</strong>
        </div>
        <div class="table-scroll-wrapper">
          <table class="modal-table">
            <thead>
              <tr>
                <th>Cant.</th>
                <th>Detalle</th>
                <th>P/Unit</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in pedido.detalle" :key="idx">
                <td class="text-center">{{ item.cant }}</td>
                <td>{{ item.item }}</td>
                <td class="text-end">{{ item.precioUnitario }} Bs.</td>
                <td class="text-end fw-bold">{{ item.total }} Bs.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer-info">
          <div class="garantia">
            <input type="checkbox" id="garantia_vista" :checked="pedido.garantia" disabled>
            <label for="garantia_vista">Garantía:</label>
          </div>
          <div class="total-final">
            Total: <strong>{{ pedido.granTotal }} Bs.</strong>
          </div>
        </div>
        <div class="direccion">
          Dirección: <strong>{{ pedido.direccion }}</strong>
        </div>
        <div class="modal-actions">
          <button class="btn btn-edit" @click="entrarModoEdicion">
            <span>Editar</span>
            <img src="@/assets/Edit.png" alt="editar">
          </button>
          <button class="btn btn-delete" @click="$emit('borrar', pedido.numeroPedido)">
            <span>Borrar</span>
            <img src="@/assets/Delete.png" alt="borrar">
          </button>
        </div>
      </div>

      <div v-else class="modal-body">
         <div class="modal-header-info editable-section">
          <div>
            <label>Pedido de:</label>
            <input type="text" v-model="pedidoEditable.cliente">
            <label>Celular 1:</label>
            <input type="text" v-model="pedidoEditable.celular1">
            <label>Celular 2:</label>
            <input type="text" v-model="pedidoEditable.celular2">
          </div>
          <div class="text-end">
             <label>Fecha de entrega:</label>
            <input type="text" v-model="pedidoEditable.fechaEntrega">
            <label>Fecha de recojo:</label>
            <input type="text" v-model="pedidoEditable.fechaRecojo">
          </div>
        </div>
        <div class="table-scroll-wrapper">
          <table class="modal-table">
            <thead>
              <tr>
                <th>Cant.</th>
                <th>Detalle</th>
                <th>P/Unit</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in pedidoEditable.detalle" :key="idx">
                <td><input class="input-table text-center" type="number" v-model="item.cant" @input="actualizarTotales"></td>
                <td><input class="input-table" type="text" v-model="item.item"></td>
                <td><input class="input-table text-end" type="number" v-model="item.precioUnitario" @input="actualizarTotales"></td>
                <td class="text-end fw-bold">{{ item.total }} Bs.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer-info">
          <div class="garantia">
            <input type="checkbox" id="garantia_edit" v-model="pedidoEditable.garantia">
            <label for="garantia_edit">Garantía:</label>
          </div>
          <div class="total-final">
            Total: <strong>{{ pedidoEditable.granTotal }} Bs.</strong>
          </div>
        </div>
        <div class="direccion editable-section">
          <label>Dirección:</label>
          <input type="text" v-model="pedidoEditable.direccion">
        </div>
        <div class="modal-actions">
          <button class="btn btn-cancel" @click="cancelarEdicion">Cancelar</button>
          <button class="btn btn-save" @click="guardarCambios">Guardar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  pedido: { type: Object, required: true }
});

const emit = defineEmits(['cerrar', 'borrar', 'guardar']);

const enModoEdicion = ref(false);
const pedidoEditable = ref(null);

// CAMBIO 1: Nueva función para manejar el clic en el overlay
const onOverlayClick = () => {
  // Si NO estamos en modo edición, entonces cerramos el modal
  if (!enModoEdicion.value) {
    emit('cerrar');
  }
};

const entrarModoEdicion = () => {
  pedidoEditable.value = JSON.parse(JSON.stringify(props.pedido));
  enModoEdicion.value = true;
};

const cancelarEdicion = () => {
  enModoEdicion.value = false;
  pedidoEditable.value = null;
};

const guardarCambios = () => {
  pedidoEditable.value.ubicacion = pedidoEditable.value.direccion;
  emit('guardar', pedidoEditable.value);
  enModoEdicion.value = false;
};

const actualizarTotales = () => {
  let nuevoGranTotal = 0;
  if (pedidoEditable.value && pedidoEditable.value.detalle) {
    pedidoEditable.value.detalle.forEach(item => {
      item.total = (item.cant || 0) * (item.precioUnitario || 0);
      nuevoGranTotal += item.total;
    });
    pedidoEditable.value.granTotal = nuevoGranTotal;
  }
};
</script>


<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  background: white; padding: 1rem 2rem 2rem 2rem; border-radius: 15px; width: 90%;
  max-width: 800px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  max-height: 90vh; display: flex; flex-direction: column;
}

/* --- ESTILOS CORREGIDOS Y NUEVOS --- */

.modal-body {
  flex-grow: 1; /* Permite que el cuerpo del modal crezca */
  overflow: hidden; /* Oculta el scroll de este div */
  display: flex;
  flex-direction: column;
}

.table-scroll-wrapper {
  overflow-y: auto; /* AÑADE EL SCROLL SÓLO A ESTA ÁREA */
  flex-grow: 1; /* Permite que la tabla ocupe el espacio disponible */
  margin-bottom: 1rem;
}

.modal-table thead th {
  position: sticky; /* Fija los encabezados de la tabla */
  top: 0;
  background-color: white; /* Evita que el texto de abajo se vea */
  z-index: 1;
}

/* --- (Resto de estilos sin cambios) --- */
.modal-title { text-align: center; font-size: 2rem; margin-bottom: 1.5rem; }
.modal-header-info { display: flex; justify-content: space-between; margin-bottom: 1rem; background: #f7f7f7; padding: 1rem; border-radius: 8px; }
.modal-dates { text-align: center; margin: 1.5rem 0; font-size: 1.2rem; }
.modal-table { width: 100%; border-collapse: collapse; }
.modal-table th, .modal-table td { padding: 0.75rem; border-bottom: 1px solid #eee; }
.modal-footer-info { display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; }
.garantia { display: flex; align-items: center; gap: 0.5rem; }
.total-final { font-size: 1.5rem; }
.direccion { background: #f7f7f7; padding: 1rem; border-radius: 8px; margin-top: 1.5rem; }
.modal-actions { display: flex; justify-content: center; gap: 1rem; margin-top: 2rem; }
.btn { border: none; border-radius: 8px; padding: 0.75rem 1.5rem; color: white; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; font-weight: 600; transition: opacity 0.2s; }
.btn-edit { background-color: #00BCD4; }
.btn-delete { background-color: #E53935; }
.editable-section label { display: block; font-weight: 600; font-size: 0.9rem; margin-top: 0.5rem; color: #555; }
.editable-section input { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; margin-top: 0.25rem; margin-bottom: 0.5rem; box-sizing: border-box; }
.input-table { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; box-sizing: border-box; }
.btn-cancel { background-color: #757575; }
.btn-save { background-color: #2196F3; }
.btn-edit:hover{
  background-color: #00BCD4;
}
.btn-delete:hover{
  background-color: #E53935;
}
.modal-actions img{
  height: 23px;
}
.modal-actions img{
  height: 23px;
}
.btn-cancel:hover{
  background-color: #757575;
}
.btn-save:hover{
  background-color: #2196F3;
}
/* Para los botones de "Editar" */
.btn-edit:active,
.btn-edit:focus {
  background-color: #00BCD4 !important; 
  border-color: #00BCD4 !important;
  box-shadow: none !important;
}

/* Para los botones de "Borrar" */
.btn-delete:active,
.btn-delete:focus {
  background-color: #E53935 !important; 
  border-color: #E53935 !important;
  box-shadow: none !important;
}

/* Para los botones de "Guardar" */
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

</style>