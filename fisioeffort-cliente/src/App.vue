<script setup>
import { RouterView, useRouter } from 'vue-router'
import { supabase} from './supabase'
 
const router = useRouter()

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
    <header class="navbar" c-if="route.name!== 'login'">
      <div class="marca">
        <h1>Fisio<span class="cian">Effort</span> <span class="morado">Studio</span></h1>
        <span class="admin-badge">Panel de administración</span>
      </div>

      <nav class="enlaces">
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/alumnos">Alumnos</RouterLink>
        <RouterLink to="/tutores">Tutores</RouterLink>
        <RouterLink to="/clases">Clases</RouterLink>
        <RouterLink to="/pagos">Pagos</RouterLink>
        <button @click="cerrarSesion" class="btn-logout">
          Cerrar Sesión
        </button>
      </nav>
    </header>

    <main class="main-content">
      <RouterView />
    </main>
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
}

/* --- Barra de navegación --- */
.navbar {
  background-color: #1a1a2e;
  padding: 1rem 2rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  border-bottom: 3px solid #00c3e3;
}

.marca {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
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

/* --- Links de navegación --- */
.enlaces {
  display: flex;
  gap: 0.35rem;
  align-items: center;
  flex-wrap: wrap;
}

.enlaces a {
  color: #a0a0b0;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
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

.main-content {
  padding: 2rem;
  flex: 1;
}

@media (max-width: 720px) {
  .navbar {
    padding: 1rem;
  }
  .enlaces {
    width: 100%;
    justify-content: flex-start;
  }
  .main-content {
    padding: 1rem;
  }
}

.btn-logout {
  background-color: transparent;
  color: #00c3e3;
  border: 1px solid #00c3e3;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
  margin-left: auto; /* Ayuda a empujarlo a la derecha si usas flexbox */
}

.btn-logout:hover {
  background-color: #00c3e3;
  color: #1a1a2e;
}

</style>