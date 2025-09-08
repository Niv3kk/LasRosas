import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

export async function login({ username, password }) {
  // Ajusta la ruta según tu backend (/api/login, /accounts/login/, etc.)
  const { data } = await api.post('/api/login', { username, password })
  return data
}
