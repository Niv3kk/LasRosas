// src/services/inventarioService.js
import { api } from '../axios'; // Importa la instancia 'api' configurada

/**
 * Obtiene la lista completa de inventario con stock calculado.
 * Llama al endpoint: GET /api/inventario/
 */
export const getInventario = () => {
  return api.get('/inventario/');
};

/**
 * Obtiene el historial de movimientos.
 * Llama al endpoint: GET /api/historial-inventario/
 * @param {Object} [filtroParams] - Opcional. Objeto con filtros.
 * @param {number} [filtroParams.inventario] - ID del item de inventario para filtrar.
 */
export const getHistorialInventario = (filtroParams = {}) => {
  return api.get('/historial-inventario/', { params: filtroParams });
};

/**
 * ---- NUEVA FUNCIÓN ----
 * Crea un nuevo movimiento en el historial de inventario.
 * Llama al endpoint: POST /api/historial-inventario/
 * @param {Object} data - Los datos del nuevo movimiento
 * @param {number} data.inventario - El ID del artículo (ej. 1)
 * @param {string} data.tipo_movimiento - "Entrada" o "Salida"
 * @param {number} data.cantidad - Ej. 10
 * @param {string} data.motivo - Ej. "Ajuste manual"
 */
export const createHistorialMovimiento = (data) => {
  // El serializador del backend espera 'inventario' (el ID), no 'inventario_id'
  return api.post('/historial-inventario/', data);
};
  //Crea un nuevo item en el inventario
export const createInventarioItem = (data) => {
  return api.post('/inventario/', data);
};
// Editar nombre / detalle de un ítem
export const updateInventarioItem = (id, data) => {
  // data = { nombre_articulo, detalle }
  return api.put(`/inventario/${id}/`, data);
};
// Borrar un ítem de inventario
export const deleteInventarioItem = (id) => {
  return api.delete(`/inventario/${id}/`);
};