// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'

// Helper de “sesión” temporal mientras no conectas backend
function isLoggedIn() {
  return localStorage.getItem('logged') === '1'
}

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior() {
    // Siempre arriba al cambiar de ruta
    return { top: 0 }
  },
  routes: [
    // Arranque: manda al login
    { path: '/', redirect: { name: 'login' } },

    // Login (ruta pública, fuera del layout)
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginView.vue'),
      meta: { guestOnly: true },
    },

    // Rutas autenticadas: usan el layout (navbar + sidebar)
    {
      path: '/app',
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: { name: 'inicio' } }, // /app → /app/inicio
        { path: 'inicio', name: 'inicio', component: () => import('@/pages/InicioPage.vue') },
        { path: 'historial-pedidos', name: 'historial-pedidos', component: () => import('@/pages/HistorialAquileresPage.vue') },
        { path: 'inventario', name: 'inventario', component: () => import('@/pages/InventarioPage.vue') },
        { path: 'lista-precios', name: 'lista-precios', component: () => import('@/pages/ListaPreciosPage.vue') },
        { path: 'historial-inventario', name: 'historial-inventario', component: () => import('@/pages/HistorialInventarioPage.vue') },
        { path: 'usuarios', name: 'usuarios', component: () => import('@/pages/UsuariosPage.vue') },
      ],
    },

    // 404
    { path: '/:pathMatch(.*)*', redirect: { name: 'login' } },
  ],
})

// // Guard global (simple y funcional para ahora)
// router.beforeEach((to, from, next) => {
//   if (to.meta?.requiresAuth && !isLoggedIn()) {
//     // Si quiere ir a /app/* pero no está logueado → login
//     return next({ name: 'login' })
//   }
//   if (to.meta?.guestOnly && isLoggedIn()) {
//     // Si ya está logueado, evitar volver al login
//     return next({ name: 'inicio' })
//   }
//   next()
// })

export default router
