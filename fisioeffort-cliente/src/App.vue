<script setup>
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router'
import { supabase } from './supabase'

const router = useRouter()
const route = useRoute()

const esActivo = (ruta) =>
  ruta === '/' ? route.path === '/' : route.path.startsWith(ruta)

const cerrarSesion = async () => {
  // 1. Le decimos a Supabase que destruya la sesión actual
  const { error } = await supabase.auth.signOut()

  if (error) {
    console.error('Error al cerrar sesión:', error)
    return
  }

  // 2. Lo mandamos de regreso a la pantalla de login y el cadenero hará su trabajo
  router.push('/login')
}
</script>

<template>
  <div class="app-container">
    <header v-if="route.name !== 'login'" class="navbar">
      <div class="marca">
        <h1>Fisio<span class="cian">Effort</span> <span class="morado">Studio</span></h1>
        <span class="admin-badge">Panel de administración</span>
      </div>

      <!-- Navegación tradicional: solo en escritorio (md+) -->
      <nav class="enlaces">
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/alumnos">Alumnos</RouterLink>
        <RouterLink to="/tutores">Tutores</RouterLink>
        <RouterLink to="/clases">Clases</RouterLink>
        <RouterLink to="/pagos">Pagos</RouterLink>
      </nav>

      <button @click="cerrarSesion" class="btn-logout" aria-label="Cerrar sesión">
        <svg class="btn-logout__icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
          <polyline points="16 17 21 12 16 7" />
          <line x1="21" x2="9" y1="12" y2="12" />
        </svg>
        <span>Cerrar Sesión</span>
      </button>
    </header>

    <main class="main-content">
      <RouterView />
    </main>

    <!-- Bottom Navigation: solo en móviles (< md) -->
    <nav v-if="route.name !== 'login'" class="bottom-nav" aria-label="Navegación principal">
      <RouterLink to="/" class="bottom-nav__item" :class="{ activo: esActivo('/') }">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect width="7" height="9" x="3" y="3" rx="1" />
          <rect width="7" height="5" x="14" y="3" rx="1" />
          <rect width="7" height="9" x="14" y="12" rx="1" />
          <rect width="7" height="5" x="3" y="16" rx="1" />
        </svg>
        <span>Dashboard</span>
      </RouterLink>

      <RouterLink to="/alumnos" class="bottom-nav__item" :class="{ activo: esActivo('/alumnos') }">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z" />
          <path d="M22 10v6" />
          <path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5" />
        </svg>
        <span>Alumnos</span>
      </RouterLink>

      <RouterLink to="/tutores" class="bottom-nav__item" :class="{ activo: esActivo('/tutores') }">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="12" cy="8" r="5" />
          <path d="M20 21a8 8 0 0 0-16 0" />
        </svg>
        <span>Tutores</span>
      </RouterLink>

      <RouterLink to="/clases" class="bottom-nav__item" :class="{ activo: esActivo('/clases') }">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect width="18" height="18" x="3" y="4" rx="2" />
          <path d="M16 2v4" />
          <path d="M8 2v4" />
          <path d="M3 10h18" />
        </svg>
        <span>Clases</span>
      </RouterLink>

      <RouterLink to="/pagos" class="bottom-nav__item" :class="{ activo: esActivo('/pagos') }">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect width="20" height="14" x="2" y="5" rx="2" />
          <line x1="2" x2="22" y1="10" y2="10" />
        </svg>
        <span>Pagos</span>
      </RouterLink>
    </nav>
  </div>
</template>

<style>
/* Reseteo básico y tema oscuro base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

html,
body {
  max-width: 100%;
  overflow-x: hidden;
}

body {
  background-color: #12121a;
  color: #ffffff;
}

/* --- Scrollbars personalizados --- */
/* Chrome, Edge, Safari */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #1a1a2e;
  border-radius: 8px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #00c3e3, #8a2be2);
  border-radius: 8px;
  border: 2px solid #1a1a2e;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #5fe3fa, #a86bf0);
}

::-webkit-scrollbar-corner {
  background: #1a1a2e;
}

/* Firefox y Edge moderno */
* {
  scrollbar-width: thin;
  scrollbar-color: #23233b #1a1a2e;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

/* --- Barra de navegación superior --- */
.navbar {
  background-color: #1a1a2e;
  padding: 1rem 2rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  border-bottom: 3px solid #00c3e3;
}

.marca {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  min-width: 0;
}

.marca h1 {
  font-size: 1.5rem;
  font-weight: bold;
  white-space: nowrap;
}

.cian { color: #00c3e3; }
.morado { color: #8a2be2; }

.admin-badge {
  background-color: #23233b;
  padding: 0.35rem 0.9rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: #a0a0b0;
  white-space: nowrap;
}

/* --- Links de navegación (solo escritorio, md+) --- */
.enlaces {
  display: none;
  gap: 0.35rem;
  align-items: center;
  flex-wrap: wrap;
  max-width: 100%;
  min-width: 0;
}

.enlaces a {
  color: #a0a0b0;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  white-space: nowrap;
  transition: color 0.15s ease, background-color 0.15s ease;
}

.enlaces a:hover {
  color: #ffffff;
  background-color: #23233b;
}

.enlaces a.router-link-exact-active {
  color: #12121a;
  background-color: #00c3e3;
  font-weight: 700;
}

@media (min-width: 768px) {
  .enlaces {
    display: flex;
  }
}

/* --- Botón "Cerrar Sesión" compacto (arriba a la derecha) --- */
.btn-logout {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background-color: transparent;
  color: #00f2fe;
  border: 1px solid #00f2fe;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.85rem;
  white-space: nowrap;
  margin-left: auto;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background-color: #00f2fe;
  color: #1a1a2e;
}

.btn-logout__icon {
  flex-shrink: 0;
}

/* --- Contenido principal --- */
.main-content {
  padding: 2rem;
  padding-bottom: 1.5rem; /* pb-6 en escritorio */
  flex: 1;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
}

/* --- Bottom Navigation (solo móviles, < md) --- */
.bottom-nav {
  display: flex;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 50;
  background-color: rgba(26, 26, 46, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-top: 1px solid #23233b;
  padding-bottom: env(safe-area-inset-bottom);
}

.bottom-nav__item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.2rem;
  padding: 0.6rem 0.25rem;
  color: #a0a0b0;
  text-decoration: none;
  font-size: 0.65rem;
  font-weight: 600;
  line-height: 1;
  transition: color 0.15s ease, background-color 0.15s ease;
}

.bottom-nav__item svg {
  flex-shrink: 0;
}

.bottom-nav__item.activo {
  color: #00f2fe; /* cyan-400 */
}

@media (min-width: 768px) {
  .bottom-nav {
    display: none;
  }
}

/* --- Ajustes móviles (< md) --- */
@media (max-width: 767px) {
  .navbar {
    padding: 1rem;
    align-items: center;
  }
  .main-content {
    padding: 1rem;
    padding-bottom: 5rem; /* pb-20 para que la barra fija no tape el contenido */
  }
}

/* Pantallas muy pequeñas: título recortado y botón logout solo con icono */
@media (max-width: 480px) {
  .marca h1 {
    font-size: 1.25rem;
  }
  .btn-logout span {
    display: none;
  }
}
</style>