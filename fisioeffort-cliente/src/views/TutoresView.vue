<script setup>
import { ref, onMounted } from 'vue'

const tutores = ref([])
const cargando = ref(true)

const nuevoTutor = ref({
  nombre_completo: '',
  telefono: '',
  correo: '' // Opcional, dependiendo de qué le pusiste a tu modelo
})

const cargarTutores = async () => {
  try {
    const respuesta = await fetch('http://127.0.0.1:8000/api/tutores/')
    tutores.value = await respuesta.json()
    cargando.value = false
  } catch (error) {
    console.error('Error al cargar tutores:', error)
    cargando.value = false
  }
}

const guardarTutor = async () => {
  try {
    const respuesta = await fetch('http://127.0.0.1:8000/api/tutores/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(nuevoTutor.value)
    })

    if (respuesta.ok) {
      nuevoTutor.value = { nombre_completo: '', telefono: '', correo: '' }
      cargarTutores() // Recarga la lista para ver al nuevo
    }
  } catch (error) {
    console.error('Error al guardar tutor:', error)
  }
}

onMounted(() => {
  cargarTutores()
})
</script>

<template>
  <div class="tutores-container">
    <div class="header-seccion">
      <h2>Gestión de <span class="morado">Tutores</span></h2>
      <p class="subtitulo">Registra tutores y consulta su información de contacto.</p>
    </div>

    <div class="grid-layout">
      <!-- Columna Izquierda: Formulario -->
      <div class="panel">
        <h3>Registrar Tutor</h3>
        <form @submit.prevent="guardarTutor" class="formulario">
          <div class="input-group">
            <label>Nombre Completo</label>
            <input type="text" v-model="nuevoTutor.nombre_completo" required placeholder="Ej. María López">
          </div>

          <div class="input-group">
            <label>Teléfono (Opcional)</label>
            <input type="text" v-model="nuevoTutor.telefono" placeholder="Ej. 449 123 4567">
          </div>

          <div class="input-group">
            <label>Correo Electrónico (Opcional)</label>
            <input type="email" v-model="nuevoTutor.correo" placeholder="correo@ejemplo.com">
          </div>

          <button type="submit" class="btn-guardar">Guardar Tutor</button>
        </form>
      </div>

      <!-- Columna Derecha: Lista -->
      <div class="panel">
        <h3>Directorio de Tutores</h3>
        <p v-if="cargando" class="cargando">Cargando datos...</p>
        <p v-else-if="tutores.length === 0" class="vacio">Aún no hay tutores registrados.</p>
        <ul v-else class="lista">
          <li v-for="tutor in tutores" :key="tutor.id">
            <div class="info-tutor">
              <span class="nombre">{{ tutor.nombre_completo }}</span>
              <span class="contacto" v-if="tutor.telefono || tutor.correo">
                {{ tutor.telefono }} <span v-if="tutor.telefono && tutor.correo">|</span> {{ tutor.correo }}
              </span>
            </div>
            <span class="id-badge">#{{ tutor.id }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tutores-container { padding: 1rem; }
h2 { font-size: 2rem; }
.morado { color: #8a2be2; }
.header-seccion { margin-bottom: 2rem; }
.subtitulo { color: #a0a0b0; margin-top: 0.35rem; }

.grid-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start; }

.panel {
  background-color: #1a1a2e;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.panel h3 { color: #00c3e3; margin-bottom: 1.5rem; }

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

.lista { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 1rem; }
.lista li {
  background-color: #23233b;
  padding: 1rem;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}
.info-tutor { display: flex; flex-direction: column; gap: 0.2rem; min-width: 0; }
.nombre { font-weight: bold; color: white; }
.contacto { font-size: 0.8rem; color: #a0a0b0; }
.id-badge {
  background-color: #33334d;
  color: #00c3e3;
  font-size: 0.8rem;
  padding: 0.3rem 0.6rem;
  border-radius: 12px;
  font-weight: bold;
  flex-shrink: 0;
}

@media (max-width: 900px) {
  .grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>