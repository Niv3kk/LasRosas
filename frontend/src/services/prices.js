// src/services/prices.js
import api from './api' // tu instancia de axios con baseURL y token

export function fetchListaPreciosAlquiler() {
  return api.get('/lista-precios/alquiler/')
}

export function fetchListaPreciosDanos() {
  return api.get('/lista-precios/danos/')
}
// 👉 NUEVO: guarda la lista completa (bulk update)
export function saveListaPreciosAlquiler(lista) {
  return api.put('/lista-precios/alquiler/', lista);
}

export function saveListaPreciosDanos(lista) {
  return api.put('/lista-precios/danos/', lista);
}