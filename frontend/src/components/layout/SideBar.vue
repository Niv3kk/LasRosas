<template>
  <aside class="sidebar">
    <nav class="menu">
      <!-- Enlaces principales -->
      <RouterLink class="item" to="/app/inicio">
        <img class="logos" src="@/assets/Inicio.png" alt="Inicio" />
        <span>Inicio</span>
      </RouterLink>

      <RouterLink class="item" to="/app/historial-pedidos">
        <img class="logos" src="@/assets/HistorialPedido.png" alt="HistorialPedidos" />
        <span>Historial de alquileres</span>
      </RouterLink>

      <RouterLink class="item" to="/app/inventario">
        <img class="logos" src="@/assets/ControlInventario.png" alt="ControlInventario" />
        <span>Control de inventario</span>
      </RouterLink>

      <RouterLink class="item" to="/app/lista-precios">
        <img class="logos" src="@/assets/ListaPrecio.png" alt="ListaPrecio" />
        <span>Lista de precios</span>
      </RouterLink>

      <!-- Sección solo para Administradores -->
      <template v-if="usuarioActual?.rol?.nombre_rol === 'Administrador'">
        <RouterLink class="item" to="/app/historial-inventario">
          <img class="logos" src="@/assets/HistorialInventario.png" alt="HistorialInventario" />
          <span>Historial de inventario</span>
        </RouterLink>

        <RouterLink class="item" to="/app/usuarios">
          <img class="logos" src="@/assets/GestionUsuarios.png" alt="GestionUsuarios" />
          <span>Gestión de usuarios</span>
        </RouterLink>
      </template>
    </nav>

    <!-- Información del usuario y botón de logout -->
    <div class="sidebar-bottom">
      <div class="user d-flex gap-2">
        <div class="avatar">{{ inicialesUsuario }}</div>
        <div>
          <div class="user-name">{{ usuarioActual?.nombre_completo }}</div>
          <div class="user-role">{{ usuarioActual?.rol?.nombre_rol }}</div>
        </div>
      </div>

      <button @click="handleLogout" class="btn btn-outline-danger btn-sm w-100 mt-2">
        <i class="bi bi-box-arrow-right me-1"></i> Salir
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { usuarioActual, logout } from '@/services/auth.js';

const router = useRouter();

// Computar iniciales del usuario
const inicialesUsuario = computed(() => {
  if (!usuarioActual.value?.nombre_completo) {
    return "??";
  }

  const partes = usuarioActual.value.nombre_completo.split(' ');
  return partes.length >= 2
    ? (partes[0][0] + partes[1][0]).toUpperCase()
    : usuarioActual.value.nombre_completo.substring(0, 2).toUpperCase();
});

// Función para cerrar sesión
function handleLogout() {
  logout();
  router.push({ name: 'login' });
}
</script>


<style scoped>
.sidebar {
  width: 260px;
  background: #ecf0f1;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e3e3e3;
}
.menu{ padding: 16px 10px; display: grid; gap: 6px; }
.item{ display: flex; align-items: center; gap: 15px; padding: 15px 12px; border-radius: 10px; color: #40444b; text-decoration: none; }
.item:hover{ background: #dde4e6; }
.item.router-link-active{ background:#d2d8da; font-weight: 600; }
.sidebar-bottom{ margin-top: auto; padding: 14px; }
.avatar{ width: 38px; height: 38px; border-radius: 50%; background: #c9434d; color: #fff; display:grid; place-items:center; font-weight:700; }
.user-name{ font-size: 14px; font-weight: 700; }
.user-role{ font-size: 12px; color:#6b6f75; margin-top:-2px; }
.logos{ height: 24px; }

/* ===== NUEVO: ESTILOS RESPONSIVOS PARA EL SIDEBAR ===== */
@media (max-width: 992px) {
  .sidebar {
    position: fixed; /* Posición fija para que flote */
    top: 0;
    left: 0;
    height: 100vh; /* Ocupa toda la altura */
    z-index: 1000; /* Por encima de todo */
    transform: translateX(-260px); /* Oculto fuera de la pantalla a la izquierda */
    transition: transform 0.3s ease-in-out; /* Transición suave */
  }
}
</style>
