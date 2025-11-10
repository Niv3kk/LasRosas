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
import logo from '@/assets/Rosa.png';

defineEmits(['toggle-sidebar']);

const logoSrc = logo;
</script>

<style scoped>
/* Las reglas de .topbar están en dashboard.css */

.logo {
  height: 48px;
  object-fit: contain;
  background-color: #D9D9D9;
}

.brand {
  padding: 0px 25px;
}

.brand-title {
  font-family: 'Great Vibes', cursive;
  font-size: 28px;
  line-height: 1;
}

.brand-subtitle {
  font-size: 12px;
  margin-top: -2px;
  opacity: 0.9;
}

/* Estilo interno del botón hamburguesa */
@media (max-width: 992px) {
  .brand {
    padding: 0px 10px;
  }
}
</style>
