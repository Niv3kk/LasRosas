<template>
  <header class="topbar d-flex align-items-center px-3">
    <button class="hamburger-btn" @click="$emit('toggle-sidebar')">
      <i class="bi bi-list"></i>
    </button>

    <div class="d-flex align-items-center gap-2">
      <img :src="logoSrc" class="logo" alt="Las Rosas" />
      <div class="brand">
        <div class="brand-title">Las Rosas</div>
        <div class="brand-subtitle">Organizadora de eventos</div>
      </div>
    </div>
  </header>
</template>

<script setup>
// 2. Definimos el evento que este componente puede emitir
defineEmits(['toggle-sidebar']);
import logo from '@/assets/Rosa.png'
const logoSrc = logo
</script>

<style scoped>
.topbar{
  height: 72px;
  background: #c9434d;
  color: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,.15);
  position: sticky; /* Importante para que se mantenga arriba */
  top: 0;
  z-index: 999;
}
.logo{ height: 48px; object-fit: contain; background-color: #D9D9D9;}
.brand-title{ font-family: 'Great Vibes', cursive; font-size: 28px; line-height: 1; }
.brand{ padding: 0px 25px; }
.brand-subtitle{ font-size: 12px; margin-top: -2px; opacity: .9; }

/* ===== NUEVO: ESTILOS PARA EL BOTÓN HAMBURGUESA ===== */
.hamburger-btn {
  display: none; /* Oculto en PC por defecto */
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  margin-right: 1rem;
  cursor: pointer;
}

@media (max-width: 992px) {
  .hamburger-btn {
    display: block; /* Visible solo en móvil */
  }
  .brand {
    padding: 0px 10px; /* Reducimos el padding en móvil */
  }
}
</style>