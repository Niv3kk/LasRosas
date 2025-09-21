// src/services/auth.js
import { ref } from 'vue';

// Esta variable reactiva guardará la información del usuario actual.
// Más adelante, la actualizarás cuando el usuario inicie sesión.
export const usuarioActual = ref({
  nombre: 'USUARIO DE PRUEBA',
  rol: 'Administrador' // Puedes cambiarlo a 'Propietaria' para probar
});