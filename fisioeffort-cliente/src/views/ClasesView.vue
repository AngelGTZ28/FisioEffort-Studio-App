<script setup>
import { ref, onMounted } from 'vue'

const clases = ref([])
const cargando = ref(true)

const nuevaClase = ref({
  nombre: '',
  capacidad_maxima: 10 // Un valor por defecto razonable
})

const cargarClases = async () => {
  try {
    const respuesta = await fetch('http://127.0.0.1:8000/api/clases/')
    clases.value = await respuesta.json()
    cargando.value = false
  } catch (error) {
    console.error('Error al cargar clases:', error)
  }
}

const guardarClase = async () => {
  try {
    const respuesta = await fetch('http://127.0.0.1:8000/api/clases/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(nuevaClase.value)
    })

    if (respuesta.ok) {
      nuevaClase.value = { nombre: '', capacidad_maxima: 10 }
      cargarClases()
    }
  } catch (error) {
    console.error('Error al guardar clase:', error)
  }
}

onMounted(() => {
  cargarClases()
})
</script>

<template>
  <div class="clases-container">
    <div class="header-seccion">
      <h2>Gestión de <span class="morado">Clases</span></h2>
      <p class="subtitulo">Crea grupos y consulta su cupo disponible.</p>
    </div>

    <div class="grid-layout">
      <!-- Columna Izquierda: Formulario -->
      <div class="panel">
        <h3>Nueva Clase</h3>
        <form @submit.prevent="guardarClase" class="formulario">
          <div class="input-group">
            <label>Nombre de la Clase (o Grupo)</label>
            <input type="text" v-model="nuevaClase.nombre" required placeholder="Ej. Rehabilitación 10:00 AM">
          </div>

          <div class="input-group">
            <label>Capacidad Máxima de Alumnos</label>
            <input type="number" v-model="nuevaClase.capacidad_maxima" required min="1">
          </div>

          <button type="submit" class="btn-guardar">Crear Clase</button>
        </form>
      </div>

      <!-- Columna Derecha: Lista de Clases -->
      <div class="panel">
        <h3>Grupos Activos</h3>
        <p v-if="cargando" class="cargando">Cargando datos...</p>
        <p v-else-if="clases.length === 0" class="vacio">Aún no hay clases creadas.</p>

        <div v-else class="grid-clases">
          <!-- Tarjeta por cada clase -->
          <div v-for="clase in clases" :key="clase.id" class="tarjeta-clase">
            <div class="header-tarjeta">
              <h4>{{ clase.nombre }}</h4>
              <span class="badge" :class="clase.lugares_disponibles === 0 ? 'lleno' : 'disponible'">
                {{ clase.lugares_disponibles }} lugares libres
              </span>
            </div>

            <div class="info-cupo">
              <p>Capacidad: {{ clase.capacidad_maxima }} alumnos</p>
            </div>

            <!-- Lista de alumnos inscritos (Badges) -->
            <div class="alumnos-list">
              <span v-if="clase.alumnos_inscritos.length === 0" class="sin-alumnos">
                No hay alumnos inscritos aún.
              </span>
              <span v-for="(alumno, index) in clase.alumnos_inscritos" :key="index" class="badge-alumno">
                {{ alumno }}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.clases-container { padding: 1rem; }
h2 { font-size: 2rem; }
.morado { color: #8a2be2; }
.header-seccion { margin-bottom: 2rem; }
.subtitulo { color: #a0a0b0; margin-top: 0.35rem; }

.grid-layout { display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; align-items: start; }

.panel {
  background-color: #1a1a2e;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.panel h3 { color: #00c3e3; margin-bottom: 1.5rem; }

/* Formulario */
.formulario { display: flex; flex-direction: column; gap: 1.5rem; }
.input-group { display: flex; flex-direction: column; gap: 0.5rem; }
label { color: #a0a0b0; font-size: 0.9rem; }
input {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.8rem;
  border-radius: 6px;
  outline: none;
  width: 100%;
}
input:focus { border-color: #8a2be2; }

.btn-guardar {
  background-color: #8a2be2;
  color: white;
  border: none;
  padding: 1rem;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-guardar:hover { opacity: 0.8; }

.cargando {
  color: #8a2be2;
  font-style: italic;
}
.vacio {
  color: #a0a0b0;
  font-style: italic;
}

/* Tarjetas de Clases */
.grid-clases { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
.tarjeta-clase {
  background-color: #23233b;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #00c3e3;
}
.header-tarjeta { display: flex; justify-content: space-between; align-items: flex-start; gap: 0.75rem; margin-bottom: 1rem; }
.header-tarjeta h4 { margin: 0; color: white; font-size: 1.1rem; }

.badge { font-size: 0.8rem; padding: 0.3rem 0.6rem; border-radius: 12px; font-weight: bold; white-space: nowrap; }
.disponible { background-color: #2e8b57; color: white; }
.lleno { background-color: #ff4d4d; color: white; }

.info-cupo p { color: #a0a0b0; font-size: 0.9rem; margin-bottom: 1rem; }

.alumnos-list { display: flex; flex-wrap: wrap; gap: 0.5rem; border-top: 1px solid #33334d; padding-top: 1rem; }
.badge-alumno { background-color: #33334d; color: #00c3e3; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 12px; }
.sin-alumnos { color: #a0a0b0; font-size: 0.85rem; font-style: italic; }

@media (max-width: 900px) {
  .grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>