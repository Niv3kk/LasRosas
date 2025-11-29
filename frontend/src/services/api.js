// src/services/api.js
import axios from 'axios';

const api = axios.create({
  // ajusta si tu backend tiene otra URL
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
});

// Adjuntar el token JWT en cada request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token'); // usa la misma key que ya estás usando
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
