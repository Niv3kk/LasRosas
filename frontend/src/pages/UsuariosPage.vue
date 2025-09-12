<template>
  <main class="usuarios-container">
    <h1 class="main-title">Usuarios</h1>

    <div class="user-list-container">
      
      <div class="user-list-header">
        <div>Usuario</div>
        <div>Rol</div>
        <div>Acciones</div>
      </div>

      <div class="user-row" v-for="usuario in usuarios" :key="usuario.id">
        <div>{{ usuario.nombre }}</div>
        <div>{{ usuario.rol }}</div>
        <div class="actions">
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

      <div class="user-row add-user-row">
        <div class="add-icon">+</div>
      </div>

    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';

// Datos de ejemplo para la lista de usuarios.
// Esto lo conectarás después con tu base de datos.
const usuarios = ref([
  { id: 1, nombre: 'JOSE ROSAS', rol: 'Administrador' },
  { id: 2, nombre: 'HILDA ALMENDRAS', rol: 'Encargado' },
  // ... aquí irían más usuarios
]);
</script>

<style scoped>
/* Estilo General del Contenedor de la Página */
.usuarios-container {
  padding: 2rem;
  background-color: #f0f2f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  min-height: 100%;
}

/* Título */
.main-title {
  text-align: center;
  color: #000000;
  margin-bottom: 2rem;
  font-weight: 600;
  font-size: 2.5rem;
}

/* Contenedor de la lista completa */
.user-list-container {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Espacio entre cada fila */
}

/* Estilo común para la cabecera y las filas de usuario */
.user-list-header,
.user-row {
  background: white;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  
  /* Usamos Grid para alinear las columnas perfectamente */
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr; /* Usuario | Rol | Acciones */
  align-items: center;
  gap: 1rem;
}

/* Estilo específico para la cabecera */
.user-list-header {
  font-weight: bold;
  color: #333;
  font-size: 1.1rem;
}

/* Estilo específico para las filas de usuario */
.user-row {
  font-size: 1rem;
}

/* Contenedor para los botones de acción */
.actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end; /* Alinea los botones a la derecha de su columna */
}

/* Estilo general de los botones */
.btn {
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  transition: opacity 0.2s;
}
.btn:hover {
  opacity: 0.85;
}

/* Botones específicos */
.btn-edit {
  background-color: #00BCD4; /* Cian */
}
.btn-edit:hover{
    background-color: #00BCD4;
}
.btn-delete {
  background-color: #E53935; /* Rojo */
}
.btn-delete:hover{
    background-color: #E53935;
}
.btn-edit img{
  height: 23px;
}
.btn-delete img{
  height: 23px;
}


.add-user-row {
  display: flex;
  justify-content: center; 
  align-items: center;    
  cursor: pointer;
  transition: background-color 0.2s;
  padding: 0.5rem;
}
.add-user-row:hover {
  background-color: #f7f7f7;
}

.add-icon {
  font-size: 2.5rem;
  color: #888;
  font-weight: 300;
}

</style>