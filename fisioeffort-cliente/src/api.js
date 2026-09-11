import { supabase } from './supabase'
import router from './router'

const API_BASE = 'http://127.0.0.1:8000/api'

/**
 * Wrapper around fetch() that attaches the Supabase JWT access token.
 * If the token expires (401), redirects to login.
 */
export async function apiFetch(path, options = {}) {
  const { data } = await supabase.auth.getSession()
  const token = data.session?.access_token

  if (!token) {
    router.push({ name: 'login' })
    throw new Error('No hay sesión activa')
  }

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
    Authorization: `Bearer ${token}`,
  }

  const respuesta = await fetch(`${API_BASE}${path}`, { ...options, headers })

  if (respuesta.status === 401) {
    await supabase.auth.signOut()
    router.push({ name: 'login' })
    throw new Error('Sesión expirada')
  }

  return respuesta
}
