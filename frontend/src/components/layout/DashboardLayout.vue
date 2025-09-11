<template>
  <div class="dash-root">
    <TopBar />

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
import SideBar from './SideBar.vue'
</script>

<style>
/* Reseteo básico para que el layout ocupe toda la pantalla sin márgenes inesperados */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

/* 1. Contenedor Raíz: ahora usa Flexbox y tiene altura FIJA */
.dash-root {
  display: flex;
  flex-direction: column;
  height: 100vh; /* <-- CLAVE: altura fija al 100% de la ventana */
  background: #e9ebed;
  overflow: hidden; /* <-- CLAVE: Evita que el body tenga scroll */
}

/* 2. Cuerpo Principal: crece para ocupar el espacio restante */
.dash-body {
  display: grid;
  grid-template-columns: 260px 1fr; /* 260px sidebar, el resto contenido */
  flex-grow: 1; /* <-- CLAVE: hace que ocupe el espacio que dejó el TopBar */
  overflow: hidden; /* Contiene a sus hijos */
}

/* 3. Área de Contenido: es la única con scroll */
.dash-content {
  padding: 24px;
  overflow-y: auto; /* <-- CLAVE: Aquí aparecerá la barra de scroll */
}
</style>