<template>
  <div class="modal-backdrop">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">Agregar Movimiento de Inventario</h3>
        <button
          type="button"
          class="btn-close"
          @click="cerrar"
          :disabled="loading"
        >
          &times;
        </button>
      </div>

      <form @submit.prevent="guardar">
        <div class="modal-body">
          <div class="form-group">
            <label for="articulo">Artículo</label>
            <select
              id="articulo"
              class="form-control"
              v-model="movimiento.inventario"
              required
            >
              <option :value="null" disabled>Seleccione un artículo...</option>
              <option
                v-for="item in inventarioList"
                :key="item.id"
                :value="item.id"
              >
                {{ item.nombre_articulo }} (Stock: {{ item.stock_actual }})
              </option>
            </select>
            <div v-if="loadingItems" class="text-muted small">
              Cargando artículos...
            </div>
          </div>

          <div class="form-group">
            <label for="tipo_movimiento">Tipo de Movimiento</label>
            <select
              id="tipo_movimiento"
              class="form-control"
              v-model="movimiento.tipo_movimiento"
              required
            >
              <option value="Salida">Salida (Resta del stock)</option>
              <option value="Entrada">Entrada (Suma al stock)</option>
            </select>
          </div>

          <div class="form-group">
            <label for="cantidad">Cantidad</label>
            <input
              id="cantidad"
              type="number"
              class="form-control"
              v-model.number="movimiento.cantidad"
              min="1"
              required
            >
          </div>

          <div class="form-group">
            <label for="motivo">Motivo</label>
            <textarea
              id="motivo"
              class="form-control"
              v-model="movimiento.motivo"
              rows="3"
              placeholder="Ej: Ajuste manual por rotura, compra de nuevo stock, etc."
              required
            ></textarea>
          </div>

          <div v-if="error" class="alert-danger">
            {{ error }}
          </div>
        </div>

        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            @click="cerrar"
            :disabled="loading"
          >
            Cancelar
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="loading"
          >
            {{ loading ? 'Guardando...' : 'Guardar Movimiento' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import {
  getInventario,
  createHistorialMovimiento,
} from '@/services/inventarioService.js';

const emit = defineEmits(['cerrar', 'guardar']);

// Estado del formulario
const movimiento = ref({
  inventario: null,
  tipo_movimiento: 'Salida',
  cantidad: 1,
  motivo: '',
});

// Estado del componente
const inventarioList = ref([]);
const loading = ref(false);
const loadingItems = ref(false);
const error = ref(null);

// Cargar artículos para el dropdown
onMounted(async () => {
  loadingItems.value = true;
  try {
    const response = await getInventario();
    inventarioList.value = response.data;
  } catch (err) {
    console.error('Error al cargar inventario en modal:', err);
    error.value = 'Error al cargar la lista de artículos.';
  } finally {
    loadingItems.value = false;
  }
});

const cerrar = () => {
  emit('cerrar');
};

const guardar = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = null;

  // Validaciones
  if (!movimiento.value.inventario) {
    error.value = 'Por favor, seleccione un artículo.';
    loading.value = false;
    return;
  }
  if (!movimiento.value.cantidad || movimiento.value.cantidad <= 0) {
    error.value = 'La cantidad debe ser mayor a 0.';
    loading.value = false;
    return;
  }
  if (!movimiento.value.motivo.trim()) {
    error.value = 'Por favor, ingrese un motivo.';
    loading.value = false;
    return;
  }

  try {
    await createHistorialMovimiento({
      inventario: movimiento.value.inventario,
      tipo_movimiento: movimiento.value.tipo_movimiento,
      cantidad: movimiento.value.cantidad,
      motivo: movimiento.value.motivo,
    });

    emit('guardar');
  } catch (err) {
    console.error('Error en guardar():', err);

    if (err.response && err.response.data) {
      if (typeof err.response.data === 'object') {
        const errors = Object.entries(err.response.data).map(([key, value]) => {
          return `${key}: ${Array.isArray(value) ? value.join(', ') : value}`;
        });
        error.value = `Error de validación: ${errors.join('. ')}`;
      } else {
        error.value =
          err.response.data.detail || 'Error al guardar. Revise los campos.';
      }
    } else {
      error.value = 'Error al guardar el movimiento. Intente de nuevo.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Estilos básicos para el modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.btn-close {
  border: none;
  background: none;
  font-size: 1.75rem;
  font-weight: 300;
  cursor: pointer;
  color: #888;
}

/* Estilos del formulario */
.modal-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  /* Importante */
}

.form-control[disabled] {
  background-color: #f5f5f5;
  color: #555;
}

textarea.form-control {
  resize: vertical;
}

.alert-danger {
  padding: 1rem;
  background-color: #f8d7da;
  color: #721c24;
  border-radius: 8px;
  text-align: center;
}

.text-muted {
  font-size: 0.85rem;
  color: #6c757d;
  margin-top: 0.25rem;
}


.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1.5rem;
  border-top: 1px solid #eee;
}

.btn {
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
  color: white;
  cursor: pointer;
  font-weight: 600;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-primary {
  background-color: #00BCD4;
  /* Usando tu color cian */
}
</style>