<template>
  <div class="modal-overlay">
    <div class="modal-content" @click.stop>
      <h2 class="modal-title">Añadir nuevo material</h2>

      <form @submit.prevent="guardar">
        <div class="form-group">
          <label>Nombre del artículo</label>
          <input
            v-model.trim="form.nombre_articulo"
            type="text"
            class="form-control"
            placeholder="Ej: Silla Tiffany blanca"
            required
          />
        </div>

        <div class="form-group">
          <label>Detalle</label>
          <textarea
            v-model.trim="form.detalle"
            class="form-control"
            rows="3"
            placeholder="Ej: Resina reforzada, apta para exterior"
          ></textarea>
        </div>

        <div v-if="error" class="alert-danger">
          {{ error }}
        </div>

        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" @click="$emit('cerrar')" :disabled="loading">
            Cancelar
          </button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { createInventarioItem } from '@/services/inventarioService.js';

const emit = defineEmits(['cerrar', 'guardado']);

const form = ref({
  nombre_articulo: '',
  detalle: '',
});

const loading = ref(false);
const error = ref('');

const guardar = async () => {
  error.value = '';
  if (!form.value.nombre_articulo) {
    error.value = 'El nombre del artículo es obligatorio.';
    return;
  }

  try {
    loading.value = true;
    const { data } = await createInventarioItem({
      nombre_articulo: form.value.nombre_articulo,
      detalle: form.value.detalle,
    });

    // Avisamos al padre que se creó OK y le pasamos el item nuevo
    emit('guardado', data);
  } catch (e) {
    console.error(e);
    if (e.response?.data?.nombre_articulo) {
      error.value = e.response.data.nombre_articulo.join(', ');
    } else {
      error.value = 'No se pudo guardar el material.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  display:flex; justify-content:center; align-items:center;
  z-index:1050;
}
.modal-content {
  background:white;
  border-radius:12px;
  padding:1.5rem;
  width:90%; max-width:500px;
  box-shadow:0 4px 20px rgba(0,0,0,0.2);
}
.modal-title {
  text-align:center;
  margin-bottom:1rem;
}
.form-group {
  margin-bottom:1rem;
}
.form-control {
  width:100%;
  padding:0.6rem;
  border-radius:8px;
  border:1px solid #ccc;
  box-sizing:border-box;
}
.alert-danger {
  margin-top:0.5rem;
  padding:0.75rem;
  border-radius:8px;
  background:#f8d7da;
  color:#721c24;
}
.modal-actions {
  display:flex;
  justify-content:flex-end;
  gap:0.5rem;
  margin-top:1rem;
}
.btn {
  border:none;
  border-radius:8px;
  padding:0.6rem 1.4rem;
  font-weight:600;
  color:white;
  cursor:pointer;
}
.btn-secondary { background:#757575; }
.btn-primary { background:#00BCD4; }
</style>
