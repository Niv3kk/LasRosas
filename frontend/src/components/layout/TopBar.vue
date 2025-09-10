<template>
  <header class="topbar d-flex align-items-center px-3">
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
import logo from '@/assets/Rosa.png'
const logoSrc = logo
</script>

<style scoped>
.topbar{
  height: 72px;
  background: #c9434d;      /* rojo del mock */
  color: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,.15);
}
.logo{  height: 48px; object-fit: contain; background-color: #D9D9D9;}
.brand-title{
  font-family: 'Great Vibes', cursive;
  font-size: 28px; line-height: 1;
}
.brand{
  padding: 0px 25px;
}
.brand-subtitle{ font-size: 12px; margin-top: -2px; opacity: .9; }
</style>
