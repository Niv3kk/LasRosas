<!-- src/components/layout/DashboardLayout.vue -->
<template>
  <div class="dash-root">
    <TopBar />

    <!-- FILA: sidebar (izq) + contenido (der) -->
    <div class="dash-body">
      <SideBar />
      <main class="dash-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import TopBar from './TopBar.vue'
import SideBar from './SideBar.vue'   // NO cambiar tu SideBar.vue
</script>

<!-- OJO: sin 'scoped' para que aplique al layout -->
<style>
.dash-root{
  min-height:100vh;
  background:#e9ebed;
}

/* CLAVE: 2 columnas: 260px (sidebar) + 1fr (contenido) */
.dash-body{
  display:grid;
  grid-template-columns: 260px 1fr;
  min-height: calc(100vh - 72px); /* 72px = alto del TopBar */
}

/* Contenido a la derecha */
.dash-content{
  padding:24px;
  overflow:auto;
  min-width:0;     /* evita que el grid “empuje” al siguiente renglón */
}
</style>
