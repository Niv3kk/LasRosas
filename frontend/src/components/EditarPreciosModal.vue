<template>
  <div class="modal-overlay">
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
              <th></th> 
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in listaEditable" :key="item.id">
              <td><input type="number" v-model="item.cantidad" @input="actualizarTotal(item)"></td>
              <td><input type="text" v-model="item.detalle"></td>
              <td><input type="number" v-model="item.precioUnitario" @input="actualizarTotal(item)"></td>
              <td class="text-right fw-bold">{{ item.total }} Bs.</td>
              <td class="text-center">
                <button class="btn-remove-item" @click="quitarItem(index)">-</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <button class="btn-add-item" @click="agregarItem">+ Añadir item</button>

      <div class="modal-actions">
        <button class="btn btn-cancel" @click="$emit('cerrar')">Cerrar</button>
        <button class="btn btn-save" @click="$emit('guardar', listaEditable)">Guardar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  lista: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['cerrar', 'guardar']);

const listaEditable = ref([]);

watch(() => props.lista, (nuevaLista) => {
  listaEditable.value = JSON.parse(JSON.stringify(nuevaLista));
}, { immediate: true, deep: true });

const actualizarTotal = (item) => {
  const cantidad = Number(item.cantidad) || 0;
  const precio = Number(item.precioUnitario) || 0;
  item.total = cantidad * precio;
};

// 5. Función para añadir una nueva fila
const agregarItem = () => {
  listaEditable.value.push({
    id: `new_${Date.now()}`, // ID temporal único
    cantidad: 1,
    detalle: '',
    precioUnitario: 0,
    total: 0
  });
};

// 6. Función para quitar una fila
const quitarItem = (index) => {
  listaEditable.value.splice(index, 1);
};
</script>

<style scoped>
/* (Tus estilos existentes se mantienen) */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  background: white; padding: 1rem; border-radius: 15px; width: 90%;
  max-width: 900px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  display: flex; flex-direction: column; max-height: 90vh;
}
.modal-title { text-align: center; font-size: 1.8rem; margin-bottom: 1.5rem; flex-shrink: 0; }
.table-scroll-wrapper { overflow-y: auto; flex-grow: 1; border: 1px solid #eee; border-radius: 8px; }
.modal-table { width: 100%; border-collapse: collapse; }
.modal-table th, .modal-table td { padding: 0.75rem; border-bottom: 1px solid #eee; }
.modal-table th { text-align: left; background-color: #f7f7f7; position: sticky; top: 0; }
.modal-table input { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; }
.modal-table input[type="number"] { text-align: right; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; flex-shrink: 0; }
.btn-save { background-color: #2196F3; border: none; border-radius: 8px; padding: 0.75rem 2rem; color: white; cursor: pointer; font-weight: 600; }
.fw-bold { font-weight: 700; }
.text-right { text-align: right; }
.text-center { text-align: center; }

/* ===== NUEVOS ESTILOS AÑADIDOS ===== */

/* Botón "Cerrar" / "Cancelar" */
.btn-cancel {
  background-color: #757575; /* Gris */
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
}

/* Botón "Añadir item" */
.btn-add-item {
  background: #eef1f3; color: #333; border: 1px solid #ddd;
  border-radius: 6px; padding: 0.5rem 1rem; cursor: pointer;
  margin-top: 1rem; align-self: flex-start; font-weight: 600;
  transition: background-color 0.2s;
}
.btn-add-item:hover { background-color: #e4e8eb; }

/* Botón "-" para eliminar fila */
.btn-remove-item {
  background: #fbe9e7; color: #E53935; border: none;
  border-radius: 50%; width: 28px; height: 28px; cursor: pointer;
  font-weight: bold; font-size: 1.2rem; line-height: 1;
  display: flex; align-items: center; justify-content: center;
  transition: background-color 0.2s;
}
.btn-remove-item:hover { background-color: #ffcdd2; }
.btn-cancel:active,
.btn-cancel:focus{
  background-color: #757575 !important;
  border-color: #757575 !important;
  box-shadow:none !important;
}
.btn-save:active,
.btn-save:focus {
  background-color: #2196F3 !important; 
  border-color: #2196F3 !important;
  box-shadow: none !important;
}
/* ===== ESTILOS PARA PANTALLAS GRANDES ===== */
@media (min-width: 768px) {
  .modal-content { padding: 1rem; }
  .modal-title { font-size: 1.8rem; }
  .modal-actions { flex-direction: row; justify-content: flex-end; }
  .modal-table td { padding: 0.75rem; }

  /* Restauramos la tabla para PC */
  .responsive-table thead { display: table-header-group; }
  .responsive-table tr { display: table-row; border: none; margin-bottom: 0; padding: 0; }
  .responsive-table td { display: table-cell; text-align: left !important; padding-left: 0.75rem; position: static; border-bottom: 1px solid #eee; }
  .responsive-table .text-right { text-align: right !important; }
  .responsive-table .text-center { text-align: center !important; }
  .responsive-table td:before { content: none; }
}
</style>