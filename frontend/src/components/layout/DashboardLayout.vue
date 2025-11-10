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
