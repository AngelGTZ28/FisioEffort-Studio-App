<script setup>
import { ref, onMounted } from 'vue'

const alumnos = ref([])
const tutores = ref([]) 
const cargando = ref(true)

// 1. Agregamos "tutor" al objeto reactivo
const nuevoAlumno = ref({
  nombre_completo: '',
  tutor: '', 
  fecha_nacimiento: '',
  ha_tomado_clase_prueba: false
})

const cargarAlumnos = async () => {
  try {
    const respuesta = await fetch('http://127.0.0.1:8000/api/alumnos/')
    alumnos.value = await respuesta.json()
    console.log('Revisando tutor:', alumnos.value)
    cargando.value = false
  } catch (error) {
    console.error('Error:', error)
  }
}

const cargarTutores = async () => {
  try {
    // Asegúrate de que esta sea la URL correcta de tu API para los tutores
    const respuesta = await fetch('http://127.0.0.1:8000/api/tutores/')
    tutores.value = await respuesta.json()
  } catch (error) {
    console.error('Error al cargar tutores:', error)
  }
}

const guardarAlumno = async () => {
  try {
    // Si el select del tutor está vacío, lo mandamos como null para que Postgres no truene
    const payload = { ...nuevoAlumno.value }
    if (payload.tutor === '') {
      payload.tutor = null
    }

    const respuesta = await fetch('http://127.0.0.1:8000/api/alumnos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (respuesta.ok) {
      nuevoAlumno.value = { nombre_completo: '', tutor: '', fecha_nacimiento: '', ha_tomado_clase_prueba: false }
      cargarAlumnos()
    }
  } catch (error) {
    console.error('Error al guardar:', error)
  }
}


onMounted(async() => {
  await cargarAlumnos()
  await cargarTutores()
  cargando.value = false

})
</script>

<template>
  <div class="alumnos-container">
    <div class="header-seccion">
      <h2>Gestión de <span class="cian">Alumnos</span></h2>
    </div>

    <div class="grid-layout">
      <!-- Columna Izquierda: Formulario -->
      <div class="panel">
        <h3>Nuevo Registro</h3>
        <form @submit.prevent="guardarAlumno" class="formulario">
          <div class="input-group">
            <label>Nombre Completo</label>
            <input type="text" v-model="nuevoAlumno.nombre_completo" required placeholder="Ej. Juan Pérez">
          </div>
          
          <!-- 3. Agregamos el input visual para el Tutor -->
          <div class="input-group">
            <label>Tutor (Opcional)</label>
            <select v-model="nuevoAlumno.tutor" class="select-oscuro">
              <option value="">-- Sin tutor / Es mayor de edad --</option>
              <option v-for="tutor in tutores" :key="tutor.id" :value="tutor.id">
                {{ tutor.nombre_completo }}
              </option>
            </select>
          </div>

          <div class="input-group">
            <label>Fecha de Nacimiento</label>
            <input type="date" v-model="nuevoAlumno.fecha_nacimiento" required>
          </div>

          <div class="input-group checkbox">
            <input type="checkbox" v-model="nuevoAlumno.ha_tomado_clase_prueba" id="prueba">
            <label for="prueba">¿Ya tomó clase de prueba?</label>
          </div>

          <button type="submit" class="btn-guardar">Registrar Alumno</button>
        </form>
      </div>

      <!-- Columna Derecha: Lista -->
      <div class="panel">
        <h3>Alumnos Activos</h3>
        <p v-if="cargando">Cargando datos...</p>
        <ul v-else class="lista">
          <li v-for="alumno in alumnos" :key="alumno.id">
            <div class="info-alumno">
              <span class="nombre">{{ alumno.nombre_completo }}</span>
              <!-- 4. Mostramos el tutor en la lista solo si existe -->
              <span v-if="alumno.nombre_tutor" class="tutor-info">Tutor: {{ alumno.nombre_tutor }}</span>
              <span class="fecha">Nacimiento: {{ alumno.fecha_nacimiento }}</span>
            </div>
            <span v-if="alumno.ha_tomado_clase_prueba" class="badge">Clase de prueba</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.alumnos-container { padding: 1rem; }
h2 { font-size: 2rem; }
.cian { color: #00c3e3; }
.header-seccion { margin-bottom: 2rem; }

.grid-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.panel {
  background-color: #1a1a2e;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.panel h3 { color: #8a2be2; margin-bottom: 1.5rem; }

.formulario { display: flex; flex-direction: column; gap: 1.5rem; }
.input-group { display: flex; flex-direction: column; gap: 0.5rem; }
label { color: #a0a0b0; font-size: 0.9rem; }

input[type="text"], input[type="date"] {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.8rem;
  border-radius: 6px;
  outline: none;
}
input[type="text"]:focus, input[type="date"]:focus {
  border-color: #00c3e3;
}

.checkbox { flex-direction: row; align-items: center; }

.btn-guardar {
  background-color: #00c3e3;
  color: #12121a;
  border: none;
  padding: 1rem;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-guardar:hover { opacity: 0.8; }

.lista { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 1rem; }
.lista li {
  background-color: #23233b;
  padding: 1rem;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.info-alumno { display: flex; flex-direction: column; gap: 0.2rem; }
.nombre { font-weight: bold; color: white; }
.tutor-info { font-size: 0.85rem; color: #00c3e3; } /* El tutor resalta un poco en cian */
.fecha { font-size: 0.8rem; color: #a0a0b0; }
.badge {
  background-color: #8a2be2;
  color: white;
  font-size: 0.7rem;
  padding: 0.3rem 0.6rem;
  border-radius: 12px;
}

.select-oscuro {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.8rem;
  border-radius: 6px;
  outline: none;
  appearance: none; /* Quita la flechita fea por defecto en algunos navegadores */
}
.select-oscuro:focus {
  border-color: #00c3e3;
}
</style>