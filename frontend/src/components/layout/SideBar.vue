<template>
  <aside class="sidebar">
    <nav class="menu">
      <RouterLink class="item" to="/app/inicio">
        <img class="logos" src="@/assets/Inicio.png" alt="Inicio"/>
        <span>Inicio</span>
      </RouterLink>
      <RouterLink class="item" to="/app/historial-pedidos">
        <img class="logos" src="@/assets/HistorialPedido.png" alt="HistorialPedidos"/>
        <span>Historial de alquileres</span>
      </RouterLink>
      <RouterLink class="item" to="/app/inventario">
        <img class="logos" src="@/assets/ControlInventario.png" alt="ControlInventario"/>
        <span>Control de inventario</span>
      </RouterLink>
      <RouterLink class="item" to="/app/lista-precios">
        <img class="logos" src="@/assets/ListaPrecio.png" alt="ListaPrecio"/>
        <span>Lista de precios</span>
      </RouterLink>
      <RouterLink class="item" to="/app/reportes">
        <img class="logos" src="@/assets/Reportes.png" alt="Reportes.png"/>
        <span>Reportes</span>
      </RouterLink>
      <RouterLink class="item" to="/app/historial-inventario">
        <img class="logos" src="@/assets/HistorialInventario.png" alt="HistorialInventario"/>
        <span>Historial de inventario</span>
      </RouterLink>
      <RouterLink class="item" to="/app/usuarios">
        <img class="logos" src="@/assets/GestionUsuarios.png" alt="GestionUsuarios"/>
        <span>Gestión de usuarios</span>  
      </RouterLink>
    </nav>

    <div class="sidebar-bottom">
      <div class="user d-flex gap-2">
        <div class="avatar">JR</div>
        <div>
          <div class="user-name">JOSE ROSAS</div>
          <div class="user-role">Administrador</div>
        </div>
      </div>
      <button class="btn btn-outline-danger btn-sm w-100 mt-2">
        <i class="bi bi-box-arrow-right me-1"></i> Salir
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background: #ecf0f1;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e3e3e3;
  /* Se eliminó height y position: sticky */
}
.menu{ padding: 16px 10px; display: grid; gap: 6px; }
.item{
  display: flex; align-items: center; gap: 15px;
  padding: 15px 12px; border-radius: 10px; color: #40444b; text-decoration: none;
}
.item i{ font-size: 20px; width: 22px; text-align: center; }
.item:hover{ background: #dde4e6; }
.item.router-link-active{ background:#d2d8da; font-weight: 600; }

.sidebar-bottom{ margin-top: auto; padding: 14px; }
.avatar{
  width: 38px; height: 38px; border-radius: 50%;
  background: #c9434d; color: #fff; display:grid; place-items:center; font-weight:700;
}
.user-name{ font-size: 14px; font-weight: 700; }
.user-role{ font-size: 12px; color:#6b6f75; margin-top:-2px; }
.logos{
  height: 24px;
}
</style>
