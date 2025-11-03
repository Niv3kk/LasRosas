// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import DashboardLayout from "@/components/layout/DashboardLayout.vue";
import { isAuthenticated, me, getUser, userRole } from "@/services/auth";

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior() { return { top: 0 }; },
  routes: [
    { path: "/", redirect: { name: "login" } },

    // Público (no autenticado)
    {
      path: "/login",
      name: "login",
      component: () => import("@/pages/LoginView.vue"),
      meta: { guestOnly: true },
    },

    // Autenticado (layout privado)
    {
      path: "/app",
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        { path: "", redirect: { name: "inicio" } },
        { path: "inicio", name: "inicio", component: () => import("@/pages/InicioPage.vue") },

        // Abiertas para ambos roles (ejemplo)
        { path: "historial-pedidos",   name: "historial-pedidos",   component: () => import("@/pages/HistorialAquileresPage.vue") },
        { path: "inventario",          name: "inventario",          component: () => import("@/pages/InventarioPage.vue") },
        { path: "lista-precios",       name: "lista-precios",       component: () => import("@/pages/ListaPreciosPage.vue") },
        { path: "historial-inventario",name: "historial-inventario",component: () => import("@/pages/HistorialInventarioPage.vue") },

        // SOLO Administrador
        {
          path: "usuarios",
          name: "usuarios",
          component: () => import("@/pages/UsuariosPage.vue"),
          meta: { roles: ["Administrador"] },
        },

        // ejemplo de ruta SOLO Propietaria (si la tuvieras):
        // { path: "reportes-propietaria", name:"reportes-propietaria", component: () => import("@/pages/ReportesPropietaria.vue"), meta: { roles: ["Propietaria"] } },
      ],
    },

    // 404 → login por ahora
    { path: "/:pathMatch(.*)*", redirect: { name: "login" } },
  ],
});

// -------- Guard global --------
let meAttempted = false;

router.beforeEach(async (to, from, next) => {
  const needsAuth = !!to.meta?.requiresAuth;
  const guestOnly = !!to.meta?.guestOnly;

  // 1) Si ya está autenticado y va a /login, redirige a /app
  if (guestOnly && isAuthenticated()) {
    return next({ name: "inicio" });
  }

  // 2) Si requiere auth y no hay token → login
  if (needsAuth && !isAuthenticated()) {
    return next({ name: "login" });
  }

  // 3) Si requiere auth y hay token pero no tenemos usuario en memoria,
  //    intenta recuperar desde /me una sola vez (para rellenar rol)
  if (needsAuth && isAuthenticated() && !getUser() && !meAttempted) {
    meAttempted = true;
    try {
      await me(); // si falla, caerá al catch
    } catch {
      return next({ name: "login" });
    }
  }

  // 4) Chequeo de roles por ruta (si la ruta define meta.roles)
  const allowed = to.meta?.roles;
  if (needsAuth && allowed?.length) {
    const role = userRole(); // "Administrador" | "Propietaria" | null
    if (!role || !allowed.includes(role)) {
      // opcional: muestra notificación de "No autorizado"
      return next({ name: "inicio" });
    }
  }

  next();
});

export default router;
