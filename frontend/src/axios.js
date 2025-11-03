// src/axios.js
import axios from "axios";

// Base del backend (ajusta si usas otra URL)
const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: BASE,
});

// Interceptor: añade token si existe
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export { api, BASE };
