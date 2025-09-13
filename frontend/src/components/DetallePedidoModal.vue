<template>
  <div class="modal-overlay" @click="$emit('cerrar')">
    <div class="modal-content" @click.stop>
      
      <h2 class="modal-title">Detalle del Pedido</h2>
      
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

      <div class="modal-footer-info">
        <div class="garantia">
          <input type="checkbox" id="garantia" :checked="pedido.garantia">
          <label for="garantia">Garantía:</label>
        </div>
        <div class="total-final">
          Total: <strong>{{ pedido.granTotal }} Bs.</strong>
        </div>
      </div>

      <div class="direccion">
        Dirección: <strong>{{ pedido.direccion }}</strong>
      </div>

      <div class="modal-actions">
        <button class="btn btn-edit">
          <span>Editar</span>
          <img src="@/assets/Edit.png" alt="editar">
        </button>
        <button class="btn btn-delete">
          <span>Borrar</span>
          <img src="@/assets/Delete.png" alt="editar">
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
// 1. Definimos los "props": la información que este componente RECIBE.
// En este caso, recibe el objeto completo del pedido.
defineProps({
  pedido: {
    type: Object,
    required: true
  }
});

// 2. Definimos los "emits": los eventos que este componente ENVÍA hacia afuera.
// En este caso, envía un evento 'cerrar' para decirle al padre que se cierre.
defineEmits(['cerrar']);
</script>

<style scoped>
/* --- COPIA Y PEGA AQUÍ TODOS LOS ESTILOS DEL MODAL --- */
/* (los que empiezan desde .modal-overlay en el archivo anterior) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  width: 90%;
  max-width: 800px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
.modal-title { text-align: center; font-size: 2rem; margin-bottom: 1.5rem; }
.modal-header-info { display: flex; justify-content: space-between; margin-bottom: 1rem; background: #f7f7f7; padding: 1rem; border-radius: 8px; }
.modal-dates { text-align: center; margin: 1.5rem 0; font-size: 1.2rem; }
.modal-table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }
.modal-table th, .modal-table td { padding: 0.75rem; border-bottom: 1px solid #eee; }
.modal-table th { text-align: left; background-color: #f7f7f7; }
.modal-footer-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.garantia { display: flex; align-items: center; gap: 0.5rem; }
.total-final { font-size: 1.5rem; }
.direccion { background: #f7f7f7; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; }
.modal-actions { display: flex; justify-content: center; gap: 1rem; }
.btn { border: none; border-radius: 8px; padding: 0.75rem 1.5rem; color: white; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; font-weight: 600; transition: opacity 0.2s; }
.btn:hover { opacity: 0.85; }
.btn-edit { background-color: #00BCD4; }
.btn-delete { background-color: #E53935; }
.fw-bold { font-weight: 700; }
.text-end { text-align: right; }
.text-center { text-align: center; }
.btn-edit img{
  height: 23px;
}
.btn-edit:hover{
    background-color: #00BCD4;
}
.btn-delete img{
  height: 23px;
}
.btn-delete:hover{
    background-color: #E53935;
}
</style>