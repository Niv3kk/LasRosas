<template>
  <div class="dash-root" :class="{ 'sidebar-open': isSidebarOpen }">
    <TopBar @toggle-sidebar="toggleSidebar" />

    <div class="backdrop" @click="toggleSidebar"></div>

    <div class="dash-body">
      <SideBar />
      <main class="dash-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import TopBar from './TopBar.vue'
import SideBar from './SideBar.vue'

// 3. Creamos una variable para saber si el sidebar está abierto o cerrado
const isSidebarOpen = ref(false);

// 4. Creamos la función que cambia el estado
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};
</script>

<style>
/* ... (tu CSS existente de html, body se queda igual) ... */
html, body { margin: 0; padding: 0; height: 100%; }

.dash-root {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #e9ebed;
  overflow: hidden;
}

.dash-body {
  display: grid;
  grid-template-columns: 260px 1fr; /* <- Diseño para PC */
  flex-grow: 1;
  overflow: hidden;
}

.dash-content {
  padding: 24px;
  overflow-y: auto;
}

/* ===== NUEVO: ESTILOS RESPONSIVOS ===== */
.backdrop {
  display: none; /* Oculto en PC */
}

/* Usamos una media query para aplicar estilos solo en pantallas pequeñas (ej. < 992px) */
@media (max-width: 992px) {
  .dash-body {
    grid-template-columns: 1fr; /* <- En móvil, solo hay una columna */
  }

  /* Cuando .sidebar-open está activo en el root... */
  .sidebar-open .sidebar {
    transform: translateX(0); /* ...el sidebar se desliza a su posición visible */
  }
  .sidebar-open .backdrop {
    display: block; /* ...y el fondo oscuro aparece */
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 998; /* Justo debajo del sidebar */
  }
}
</style>