<template>
  <div class="modal-overlay" @click="onOverlayClick">
    <div class="modal-content" @click.stop>
      <h2 class="modal-title">Detalle del Alquiler</h2>

      <div v-if="!enModoEdicion" class="modal-body">
        <div class="card-content">
          <div class="fw-semibold">Alquiler de: {{ alquiler.cliente }}</div>
          <div>Ubicacion: {{ alquiler.ubicacion }}</div>
          <div class="text-muted small mt-auto">{{ alquiler.fecha }}</div>
        </div>
        <div class="table-scroll-wrapper">
          <table class="modal-table">
            <thead><tr><th>Cant.</th><th>Detalle</th></tr></thead>
            <tbody>
              <tr v-for="(item, idx) in alquiler.detalle" :key="idx">
                <td class="text-center">{{ item.cant }}</td>
                <td>{{ item.item }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-actions">
          <button class="btn btn-edit" @click="entrarModoEdicion">
            <span>Editar</span>
            <img src="@/assets/Edit.png" alt="editar">
          </button>
          <button class="btn btn-delete" @click="$emit('borrar', alquiler.id)">
            <span>Borrar</span>
            <img src="@/assets/Delete.png" alt="borrar">
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
          <table class="modal-table">
            <thead><tr><th>Cant.</th><th>Detalle</th><th></th></tr></thead>
            <tbody>
              <tr v-for="(item, idx) in alquilerEditable.detalle" :key="idx">
                <td><input class="input-table input-cant" type="number" v-model="item.cant"></td>
                <td><input class="input-table" type="text" v-model="item.item"></td>
                <td class="text-center">
                  <button class="btn-remove-item" @click="quitarItemDetalle(idx)">-</button>
                </td>
              </tr>
            </tbody>
          </table>
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
  alquiler: { type: Object, required: true }
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
  emit('guardar', alquilerEditable.value);
  enModoEdicion.value = false;
};

const agregarItemDetalle = () => {
  alquilerEditable.value.detalle.push({ cant: 1, item: '' });
};

const quitarItemDetalle = (index) => {
  alquilerEditable.value.detalle.splice(index, 1);
};
</script>

<style scoped>
/* Estilos generales del modal y botones (puedes copiarlos de tus otros modales) */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: white; padding: 2rem; border-radius: 15px; width: 90%; max-width: 700px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); max-height: 90vh; display: flex; flex-direction: column; }
.modal-title { text-align: center; font-size: 1.8rem; margin-bottom: 1.5rem; }
.modal-body { display: flex; flex-direction: column; flex-grow: 1; overflow: hidden; }
.table-scroll-wrapper { overflow-y: auto; flex-grow: 1; margin-top: 1rem; border: 1px solid #eee; border-radius: 8px;}
.modal-table { width: 100%; border-collapse: collapse; }
.modal-table th, .modal-table td { padding: 0.75rem; border-bottom: 1px solid #eee; }
.modal-table th { text-align: left; background-color: #f7f7f7; position: sticky; top: 0; }
.modal-actions { display: flex; justify-content: center; gap: 1rem; margin-top: 2rem; }
.btn { border: none; border-radius: 8px; padding: 0.75rem 1.5rem; color: white; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; font-weight: 600; }
.btn-edit { background-color: #00BCD4; }
.btn-delete { background-color: #E53935; }
.btn-cancel { background-color: #757575; }
.btn-save { background-color: #2196F3; }
.btn-edit img, .btn-delete img { height: 20px; }
.fw-semibold { font-weight: 600; }
.text-muted { color: #6c757d; }
.small { font-size: 0.9rem; }
.mt-auto { margin-top: auto; }
.text-center { text-align: center; }
.btn-cancel:hover{ background-color: #757575;}
.btn-save:hover{ background-color: #2196f3;}

/* Estilos para modo edición */
.editable-section { border: 1px solid #eee; border-radius: 8px; padding: 1rem; }
.editable-section label { display: block; font-weight: 600; font-size: 0.9rem; margin-top: 0.5rem; color: #555; }
.editable-section input { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; margin-top: 0.25rem; }
.input-table { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; }
.input-cant { max-width: 80px; }
.btn-add-item { background: #e0e0e0; border: none; border-radius: 6px; padding: 0.5rem 1rem; cursor: pointer; margin-top: 1rem; align-self: flex-start; }
.btn-remove-item { background: #fbe9e7; color: #E53935; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; font-weight: bold; }
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