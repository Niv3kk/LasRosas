import { ref } from "vue";
import { api, BASE } from "@/axios";
import axios from "axios";

// Estado reactivo del usuario en memoria
export const usuarioActual = ref(null);

// ---------- helpers de sesión ----------
const KEY_TOKEN = "token";
const KEY_USER  = "user";

// --- setSession (MODIFICADO) ---
// Ahora puede guardar token y usuario por separado sin borrar el otro
export function setSession({ token, user }) {
  if (token) {
    localStorage.setItem(KEY_TOKEN, token);
  }
  if (user) {
    localStorage.setItem(KEY_USER, JSON.stringify(user));
  }
  // Siempre lee desde localStorage para actualizar el estado
  usuarioActual.value = getUser(); 
}

export function clearSession() {
  localStorage.removeItem(KEY_TOKEN);
  localStorage.removeItem(KEY_USER);
  usuarioActual.value = null;
}

export function getToken() {
  return localStorage.getItem(KEY_TOKEN);
}

export function getUser() {
  const raw = localStorage.getItem(KEY_USER);
  try { return raw ? JSON.parse(raw) : null; } catch { return null; }
}

export function isAuthenticated() {
  return !!getToken();
}

export function userRole() {
  const u = usuarioActual.value || getUser();
  return u?.rol?.nombre_rol || null;
}

export function initAuthFromStorage() {
  const u = getUser();
  usuarioActual.value = u;
}

// ---------- llamadas al backend (CORREGIDAS) ----------

// --- login (Totalmente Modificado) ---
export async function login({ username, password }) {
  try {
    // Paso 1: Obtener el token de la nueva ruta de simplejwt
    // Usamos 'axios' base (no 'api') porque 'api' adjuntaría un token que no tenemos
    const res = await axios.post(`${BASE}/api/auth/token/`, {
      username,
      password,
    });

    const token = res.data.access; // simplejwt devuelve el token en 'access'
    if (!token) throw new Error("No se recibió token");

    // Paso 2: Guardar SOLO el token en sesión
    setSession({ token });

    // Paso 3: Llamar a 'me()' PARA OBTENER LOS DATOS DEL USUARIO
    // 'me()' usará la instancia 'api' que ahora adjuntará el nuevo token
    const user = await me(); // me() se encarga de guardar el usuario en sesión

    // Devolvemos ambos, tal como esperaba tu lógica anterior
    return { token, user };

  } catch (err) {
    clearSession(); // Limpia todo si falla
    // Muestra el error específico de "Credenciales inválidas"
    const errorMsg = err.response?.data?.detail || "Credenciales inválidas o error de red";
    throw new Error(errorMsg);
  }
}

// --- me (Corregido el Bug de la URL) ---
export async function me() {
  try {
    // BUG CORREGIDO:
    // Antes: api.get("/api/auth/me/") -> http://.../api/api/auth/me/ (MAL)
    // Ahora: api.get("/auth/me/")     -> http://.../api/auth/me/ (BIEN)
    const { data } = await api.get("/auth/me/");
    
    // Guardamos los datos del usuario en la sesión
    setSession({ user: data });
    return data;
  } catch (e) {
    clearSession(); // Si 'me' falla (ej. token expirado), deslogueamos
    throw e;
  }
}

export function logout() {
  clearSession();
}