import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// --- INICIO DE LA SOLUCIÓN ---

// 1. Importa tu función de auth
import { initAuthFromStorage } from './services/auth'

// 2. Importa tu CSS de layout (asegúrate que la ruta sea correcta)
import './assets/dashboard.css' 

// 3. Llama a la función ANTES de crear la app
// (Esto arregla el problema de "datos desaparecen al recargar")
initAuthFromStorage()

// --- FIN DE LA SOLUCIÓN ---

createApp(App).use(router).mount('#app')