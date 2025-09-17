<template>
  <div class="modal-overlay">
    <div class="modal-content" @click.stop>
      <h2 class="modal-title">{{ tituloModal }}</h2>

      <div class="form-section">
        <label for="nombre">Nombre de Usuario:</label>
        <input type="text" id="nombre" v-model="usuarioEditable.nombre" placeholder="Ej: Juan Perez">

        <label for="rol">Rol:</label>
        <select id="rol" v-model="usuarioEditable.rol">
          <option value="Administrador">Administrador</option>
          <option value="Encargado">Encargado</option>
          <option value="Empleado">Empleado</option>
        </select>
      </div>

      <div class="modal-actions">
        <button v-if="usuario" class="btn btn-delete" @click="borrar">Borrar</button>
        <div class="spacer"></div>
        <button class="btn btn-cancel" @click="$emit('cerrar')">Cancelar</button>
        <button class="btn btn-save" @click="guardar">Guardar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  usuario: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['cerrar', 'guardar', 'borrar']);

const usuarioEditable = ref({});

watch(() => props.usuario, (nuevoValor) => {
  if (nuevoValor) {
    usuarioEditable.value = { ...nuevoValor };
  } else {
    usuarioEditable.value = { nombre: '', rol: 'Empleado' };
  }
}, { immediate: true });

const tituloModal = computed(() => {
  return props.usuario ? 'Editar Usuario' : 'Añadir Nuevo Usuario';
});

const guardar = () => {
  if (!usuarioEditable.value.nombre.trim()) {
    alert('El nombre de usuario no puede estar vacío.');
    return;
  }
  emit('guardar', usuarioEditable.value);
};

const borrar = () => {
  if (confirm('¿Estás seguro de que quieres borrar a este usuario?')) {
    emit('borrar', props.usuario.id);
  }
};
</script>

<style scoped>
/* Estilos del modal y formulario */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: white; padding: 2rem; border-radius: 15px; width: 90%; max-width: 500px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
.modal-title { text-align: center; font-size: 1.8rem; margin-bottom: 1.5rem; }
.form-section { display: flex; flex-direction: column; gap: 0.5rem; }
.form-section label { font-weight: 600; color: #555; margin-top: 0.5rem; }
.form-section input, .form-section select { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; align-items: center; }
.spacer { flex-grow: 1; } /* Espaciador flexible */
.btn { border: none; border-radius: 8px; padding: 0.75rem 1.5rem; color: white; cursor: pointer; font-weight: 600; }
.btn-delete { background-color: #E53935; }
.btn-cancel { background-color: #757575; }
.btn-save { background-color: #2196F3; }
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
.btn-delete:active,
.btn-delete:focus {
  background-color: #E53935 !important; 
  border-color: #E53935 !important;
  box-shadow: none !important;
}
</style>