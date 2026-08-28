<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <!-- Barra de Navegación Superior -->
    <header class="navbar">
      <div class="logo">
        <!-- Usamos los colores de tu marca -->
        <h1>Fisio<span class="cian">Effort</span> <span class="morado">Studio</span></h1>
      </div>
      <nav>
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/alumnos">Alumnos</RouterLink>
        <RouterLink to="/tutores">Tutores</RouterLink>
        <span class="admin-badge">Panel de Administración</span>
      </nav>
    </header>

    <!-- Aquí se inyectarán las diferentes pantallas (Alumnos, Pagos, etc.) -->
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Reseteo básico y Tema Oscuro Base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
  background-color: #12121a; /* Azul marino/Carbón muy oscuro para no cansar la vista */
  color: #ffffff; /* Texto general en blanco puro */
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Estilos de la Barra de Navegación */
.navbar {
  background-color: #1a1a2e; /* Un tono ligeramente más claro para contraste */
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 3px solid #00c3e3; /* El acento Cian de tu logo */
}

.logo h1 {
  font-size: 1.8rem;
  font-weight: bold;
}

/* Colores de acento */
.cian { color: #00c3e3; }
.morado { color: #8a2be2; font-size: 1rem; font-weight: normal; }

.admin-badge {
  background-color: #33334d;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #00c3e3;
}

.main-content {
  padding: 2rem;
}

.enlaces { display: flex; gap: 1.5rem; align-items: center; }
.enlaces a { color: #a0a0b0; text-decoration: none; font-weight: bold; }
.enlaces a:hover { color: #00c3e3; }
.enlaces a.router-link-active { color: #00c3e3; border-bottom: 2px solid #00c3e3; }
</style>