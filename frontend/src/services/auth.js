// src/services/auth.js
import { ref } from "vue";
import { api, BASE } from "@/axios";

// Estado reactivo del usuario en memoria
export const usuarioActual = ref(null);  // { usuario_id, nombre_completo, nombre_usuario, rol:{ nombre_rol, ... } }

// ---------- helpers de sesión ----------
const KEY_TOKEN = "token";
const KEY_USER  = "user";

export function setSession({ token, user }) {
  if (token) localStorage.setItem(KEY_TOKEN, token);
  if (user)  localStorage.setItem(KEY_USER, JSON.stringify(user));
  usuarioActual.value = user || null;
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
  return u?.rol?.nombre_rol || null;  // "Administrador" | "Propietaria" | null
}

// Carga inicial (rehidrata desde localStorage cuando arranca la app)
export function initAuthFromStorage() {
  const u = getUser();
  usuarioActual.value = u;
}

// ---------- llamadas al backend ----------
export async function login({ username, password }) {
  // login no usa bearer; por eso llamamos a fetch/axios a mano
  const res = await fetch(`${BASE}/api/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Credenciales inválidas");
  }

  const data = await res.json();
  setSession({ token: data.access, user: data.user });
  return data;
}

export async function me() {
  try {
    const { data } = await api.get("/api/auth/me/");
    setSession({ token: getToken(), user: data });
    return data;
  } catch (e) {
    clearSession();
    throw e;
  }
}

export function logout() {
  clearSession();
}
