<template>
  <div class="modal-overlay" @click="$emit('cerrar')">
    <div class="modal-content" @click.stop>
      <h2 class="modal-title">Editar Lista de Precios</h2>
      <div class="table-scroll-wrapper">
        <table class="modal-table">
          <thead>
            <tr>
              <th>Cant.</th>
              <th>Detalle</th>
              <th>Precio Unit.</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in listaEditable" :key="item.id">
              <td><input type="number" v-model="item.cantidad" @input="actualizarTotal(item)"></td>
              <td><input type="text" v-model="item.detalle"></td>
              <td><input type="number" v-model="item.precioUnitario" @input="actualizarTotal(item)"></td>
              <td class="text-right fw-bold">{{ item.total }} Bs.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="modal-actions">
        <button class="btn btn-save" @click="$emit('guardar', listaEditable)">Guardar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

// 1. Definimos los "props": la información que este componente RECIBE del padre.
const props = defineProps({
  lista: {
    type: Array,
    required: true
  }
});

// 2. Definimos los "emits": los eventos que este componente ENVÍA al padre.
const emit = defineEmits(['cerrar', 'guardar']);

// 3. Creamos una copia local y editable de la lista que recibimos por props.
// Esto es VITAL para no modificar los datos del padre directamente.
const listaEditable = ref([]);

watch(() => props.lista, (nuevaLista) => {
  // Cada vez que la prop 'lista' cambia, hacemos una copia profunda.
  listaEditable.value = JSON.parse(JSON.stringify(nuevaLista));
}, { immediate: true, deep: true });


// 4. Función local para actualizar el total de una fila.
const actualizarTotal = (item) => {
  item.total = item.cantidad * item.precioUnitario;
};
</script>

<style scoped>
/* --- ESTILOS EXCLUSIVOS DEL MODAL --- */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  background: white; padding: 2rem; border-radius: 15px; width: 90%;
  max-width: 900px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  display: flex; flex-direction: column; max-height: 90vh;
}
.modal-title {
  text-align: center; font-size: 1.8rem; margin-bottom: 1.5rem; flex-shrink: 0;
}
.table-scroll-wrapper {
  overflow-y: auto; flex-grow: 1;
}
.modal-table {
  width: 100%; border-collapse: collapse;
}
.modal-table th, .modal-table td {
  padding: 0.75rem; border-bottom: 1px solid #eee;
}
.modal-table th {
  text-align: left; background-color: #f7f7f7; position: sticky; top: 0;
}
.modal-table input {
  width: 100%; padding: 0.5rem; border: 1px solid #ccc;
  border-radius: 6px; font-size: 1rem;
}
.modal-table input[type="number"] { text-align: right; }
.modal-actions {
  display: flex; justify-content: flex-end; margin-top: 1.5rem; flex-shrink: 0;
}
.btn-save {
  background-color: #2196F3; border: none; border-radius: 8px;
  padding: 0.75rem 2rem; color: white; cursor: pointer;
  font-weight: 600; transition: opacity 0.2s;
}
.btn-save:hover { opacity: 0.85; background-color: #2196F3;}
.fw-bold { font-weight: 700; }
.text-right { text-align: right; }

/* Para los botones de "Guardar" */
.btn-save:active,
.btn-save:focus {
  background-color: #2196F3 !important; 
  border-color: #2196F3 !important;
  box-shadow: none !important;
}
</style>