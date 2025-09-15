<template>
  <div class="modal-overlay">
    <div class="modal-content" @click.stop>
      <h2 class="modal-title">Editar Inventario</h2>
      
      <div class="table-scroll-wrapper">
        <table class="modal-table">
          <thead>
            <tr>
              <th>Detalle</th>
              <th>Stock Inicial</th>
              <th>Salidas</th>
              <th>Total</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in inventarioEditable" :key="item.id">
              <td><input type="text" v-model="item.detalle"></td>
              <td><input class="text-right" type="number" v-model="item.stockInicial" @input="actualizarTotales(item)"></td>
              <td><input class="text-right" type="number" v-model="item.salidas" @input="actualizarTotales(item)"></td>
              <td class="text-right fw-bold">{{ item.total }}</td>
              <td class="text-center">
                <button class="btn-remove-item" @click="quitarItem(index)">-</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <button class="btn-add-item" @click="agregarItem">+ Añadir item</button>

      <div class="modal-actions">
        <button class="btn btn-cancel" @click="$emit('cerrar')">Cancelar</button>
        <button class="btn btn-save" @click="guardarCambios">Guardar Cambios</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  inventario: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['cerrar', 'guardar']);

const inventarioEditable = ref([]);

watch(() => props.inventario, (nuevoValor) => {
  inventarioEditable.value = JSON.parse(JSON.stringify(nuevoValor));
}, { immediate: true, deep: true });

const actualizarTotales = (item) => {
  const stock = Number(item.stockInicial) || 0;
  const salidas = Number(item.salidas) || 0;
  item.total = stock - salidas;
  item.cantidad = item.total;
};

const guardarCambios = () => {
  inventarioEditable.value.forEach(item => actualizarTotales(item));
  emit('guardar', inventarioEditable.value);
};

const agregarItem = () => {
  inventarioEditable.value.push({
    id: `new_${Date.now()}`,
    cantidad: 0,
    detalle: '',
    stockInicial: 0,
    salidas: 0,
    total: 0
  });
};

// ===== CAMBIO 3: Nueva función para quitar un item =====
const quitarItem = (index) => {
  // Usamos splice para remover el item de la lista en la posición (index)
  inventarioEditable.value.splice(index, 1);
};
</script>

<style scoped>
/* (Estilos existentes del modal) */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: white; padding: 2rem; border-radius: 15px; width: 90%; max-width: 900px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); max-height: 90vh; display: flex; flex-direction: column; }
.modal-title { text-align: center; font-size: 1.8rem; margin-bottom: 1.5rem; flex-shrink: 0; }
.table-scroll-wrapper { overflow-y: auto; flex-grow: 1; border: 1px solid #eee; border-radius: 8px; }
.modal-table { width: 100%; border-collapse: collapse; }
.modal-table th, .modal-table td { padding: 0.75rem; border-bottom: 1px solid #eee; }
.modal-table th { text-align: left; background-color: #f7f7f7; position: sticky; top: 0; }
.modal-table input { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; flex-shrink: 0; }
.btn-cancel { background-color: #757575; color: white; border: none; border-radius: 8px; padding: 0.75rem 1.5rem; cursor: pointer; font-weight: 600; }
.btn-save { background-color: #2196F3; color: white; border: none; border-radius: 8px; padding: 0.75rem 1.5rem; cursor: pointer; font-weight: 600; }
.text-right { text-align: right; }
.text-center { text-align: center; }
.fw-bold { font-weight: 700; }
.btn-add-item {
  background: #eef1f3; color: #333; border: 1px solid #ddd;
  border-radius: 6px; padding: 0.5rem 1rem; cursor: pointer;
  margin-top: 1rem; align-self: flex-start; font-weight: 600;
  transition: background-color 0.2s;
}
.btn-add-item:hover { background-color: #e4e8eb; }

/* ===== CAMBIO 4: Estilo para el nuevo botón de eliminar fila ===== */
.btn-remove-item {
  background: #fbe9e7; /* Rojo claro */
  color: #E53935; /* Rojo oscuro */
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.2rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}
.btn-remove-item:hover {
  background-color: #ffcdd2; /* Rojo más claro al pasar el mouse */
}
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
</style>