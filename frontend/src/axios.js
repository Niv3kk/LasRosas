// src/axios.js
import axios from "axios";
// Asegúrate de que la ruta a tu auth.js sea correcta
import { getToken, clearSession } from './services/auth.js';

// 1. Definir BASE (SIN 'export' aquí)
const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

// 2. Crear 'api' con la baseURL CORREGIDA
const api = axios.create({
  baseURL: `${BASE}/api/`, // <-- Esta era la corrección importante para el 404
});

// 3. Interceptor: añade token si existe
api.interceptors.request.use(
  (config) => {
    const token = getToken(); // Usamos tu helper de auth.js
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 4. (Recomendado) Interceptor de respuesta para manejar 401 (Token expirado)
api.interceptors.response.use(
  (response) => response, // Pasa la respuesta si todo está bien
  (error) => {
    // Si el backend responde 401 (No autorizado)
    if (error.response && error.response.status === 401) {
      clearSession(); // Usamos tu helper de auth.js
      
      // Redirige al login
      window.location.href = '/login'; 
    }
    return Promise.reject(error);
  }
);


// 5. Exportar 'api' y 'BASE' al final (esto arregla el error de duplicado)
export { api, BASE };