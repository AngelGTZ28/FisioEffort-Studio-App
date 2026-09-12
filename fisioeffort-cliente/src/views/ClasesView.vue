<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiFetch } from '../api'
import SkeletonTarjetas from '../components/SkeletonTarjetas.vue'

const clases = ref([])
const alumnos = ref([])
const cargando = ref(true)

const nuevaClase = ref({
  nombre: '',
  capacidad_maxima: 10 // Un valor por defecto razonable
})

// --- Formulario "Agregar alumno a clase" ---
const claseSeleccionada = ref('')
const tipoInscripcion = ref('REGULAR')
const busquedaAlumno = ref('')
const alumnoSeleccionado = ref(null)
const mostrarDropdownAlumno = ref(false)
const enviandoInscripcion = ref(false)

const alumnosFiltrados = computed(() => {
  const activos = alumnos.value.filter((a) => a.activo)
  if (!busquedaAlumno.value) return activos
  return activos.filter((a) =>
    a.nombre_completo.toLowerCase().includes(busquedaAlumno.value.toLowerCase())
  )
})

const cargarClases = async () => {
  try {
    const respuesta = await apiFetch('/clases/')
    clases.value = await respuesta.json()
    cargando.value = false
  } catch (error) {
    console.error('Error al cargar clases:', error)
  }
}

const cargarAlumnos = async () => {
  try {
    const respuesta = await apiFetch('/alumnos/')
    alumnos.value = await respuesta.json()
  } catch (error) {
    console.error('Error al cargar alumnos:', error)
  }
}

const guardarClase = async () => {
  try {
    const respuesta = await apiFetch('/clases/', {
      method: 'POST',
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

const seleccionarAlumno = (alumno) => {
  alumnoSeleccionado.value = alumno
  busquedaAlumno.value = alumno.nombre_completo
  mostrarDropdownAlumno.value = false
}

// Extrae mensajes de error legibles de la respuesta de DRF,
// ej. {"alumno": ["El alumno ya se encuentra inscrito..."]}
function extraerMensajeError(datosError) {
  if (!datosError || typeof datosError !== 'object') {
    return 'No se pudo completar la inscripción.'
  }
  const mensajes = Object.values(datosError).flat()
  return mensajes.length > 0 ? mensajes.join(' ') : 'No se pudo completar la inscripción.'
}

const inscribirAlumno = async () => {
  if (!claseSeleccionada.value || !alumnoSeleccionado.value) {
    alert('Selecciona una clase y un alumno antes de inscribir.')
    return
  }

  enviandoInscripcion.value = true
  try {
    const respuesta = await apiFetch('/inscripciones/', {
      method: 'POST',
      body: JSON.stringify({
        alumno: alumnoSeleccionado.value.id,
        clase: claseSeleccionada.value,
        tipo: tipoInscripcion.value
      })
    })

    const datos = await respuesta.json()

    if (respuesta.ok) {
      alert(`${alumnoSeleccionado.value.nombre_completo} fue inscrito correctamente.`)
      // Limpiamos el formulario de inscripción
      claseSeleccionada.value = ''
      tipoInscripcion.value = 'REGULAR'
      busquedaAlumno.value = ''
      alumnoSeleccionado.value = null
      cargarClases()
      cargarAlumnos()
    } else {
      alert(extraerMensajeError(datos))
    }
  } catch (error) {
    console.error('Error al inscribir alumno:', error)
    alert('Error de red al inscribir al alumno.')
  } finally {
    enviandoInscripcion.value = false
  }
}

const quitarDeClase = async (inscripcionId, alumnoNombre, claseNombre) => {
  if (!confirm(`¿Quitar a ${alumnoNombre} de ${claseNombre}?`)) return

  try {
    const respuesta = await apiFetch(`/inscripciones/${inscripcionId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ activa: false })
    })

    if (respuesta.ok) {
      cargarClases()
    } else {
      alert('No se pudo quitar al alumno de la clase.')
    }
  } catch (error) {
    console.error('Error al quitar de clase:', error)
  }
}

onMounted(() => {
  cargarClases()
  cargarAlumnos()
})
</script>

<template>
  <div class="clases-container">
    <div class="header-seccion">
      <h2>Gestión de <span class="morado">Clases</span></h2>
      <p class="subtitulo">Crea grupos, consulta su cupo e inscribe alumnos.</p>
    </div>

    <div class="grid-layout">
      <!-- Columna Izquierda: Formularios -->
      <div class="columna-formularios">
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

        <div class="panel">
          <h3>Agregar Alumno a Clase</h3>
          <form @submit.prevent="inscribirAlumno" class="formulario">
            <div class="input-group">
              <label>Clase</label>
              <select v-model="claseSeleccionada" required>
                <option value="" disabled>-- Selecciona una clase --</option>
                <option v-for="clase in clases" :key="clase.id" :value="clase.id">
                  {{ clase.nombre }} ({{ clase.lugares_disponibles }} lugares libres)
                </option>
              </select>
            </div>

            <div class="input-group buscador-personalizado">
              <label>Alumno</label>
              <input
                type="text"
                v-model="busquedaAlumno"
                @focus="mostrarDropdownAlumno = true"
                class="input-busqueda"
                placeholder="Buscar alumno por nombre..."
                autocomplete="off"
              >
              <ul v-if="mostrarDropdownAlumno" class="dropdown-lista">
                <li v-if="alumnosFiltrados.length === 0" class="sin-resultados">
                  No se encontraron alumnos activos
                </li>
                <li v-for="alumno in alumnosFiltrados" :key="alumno.id" @click="seleccionarAlumno(alumno)">
                  {{ alumno.nombre_completo }}
                </li>
              </ul>
              <span v-if="mostrarDropdownAlumno" class="btn-cerrar" @click="mostrarDropdownAlumno = false">
                Cerrar
              </span>
            </div>

            <div class="input-group">
              <label>Tipo de Inscripción</label>
              <select v-model="tipoInscripcion">
                <option value="REGULAR">Regular (Pago normal)</option>
                <option value="PRUEBA">Clase de Prueba</option>
              </select>
            </div>

            <button type="submit" class="btn-guardar btn-guardar--cian" :disabled="enviandoInscripcion">
              {{ enviandoInscripcion ? 'Inscribiendo...' : 'Inscribir Alumno' }}
            </button>
          </form>
        </div>
      </div>

      <!-- Columna Derecha: Lista de Clases -->
      <div class="panel">
        <h3>Grupos Activos</h3>
        <SkeletonTarjetas v-if="cargando" :tarjetas="3" tipo="clases" />
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
              <span v-for="alumno in clase.alumnos_inscritos" :key="alumno.inscripcion_id" class="badge-alumno">
                {{ alumno.alumno_nombre }}
                <button
                  class="quitar-alumno"
                  title="Quitar de esta clase"
                  @click="quitarDeClase(alumno.inscripcion_id, alumno.alumno_nombre, clase.nombre)"
                >×</button>
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
.columna-formularios { display: flex; flex-direction: column; gap: 2rem; }

.panel {
  background-color: #1a1a2e;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.panel h3 { color: #00c3e3; margin-bottom: 1.5rem; }

/* Formulario */
.formulario { display: flex; flex-direction: column; gap: 1.5rem; }
.input-group { display: flex; flex-direction: column; gap: 0.5rem; position: relative; }
label { color: #a0a0b0; font-size: 0.9rem; }
input, select {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.8rem;
  border-radius: 6px;
  outline: none;
  width: 100%;
}
input:focus, select:focus { border-color: #8a2be2; }

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
.btn-guardar:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-guardar--cian { background-color: #00c3e3; color: #12121a; }

.vacio {
  color: #a0a0b0;
  font-style: italic;
}

/* Buscador de alumnos (mismo patrón que el buscador de tutores en AlumnosView) */
.buscador-personalizado { position: relative; }
.input-busqueda {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.8rem;
  border-radius: 6px;
  outline: none;
  width: 100%;
}
.input-busqueda:focus { border-color: #00c3e3; }

.dropdown-lista {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: #1a1a2e;
  border: 1px solid #33334d;
  border-radius: 6px;
  margin-top: 0.3rem;
  padding: 0;
  list-style: none;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: 0 4px 10px rgba(0,0,0,0.5);
}
.dropdown-lista li {
  padding: 0.8rem;
  cursor: pointer;
  border-bottom: 1px solid #23233b;
  color: white;
}
.dropdown-lista li:hover { background-color: #8a2be2; }
.sin-resultados {
  color: #ff4d4d !important;
  cursor: default;
  font-style: italic;
}
.sin-resultados:hover { background-color: transparent !important; }

.btn-cerrar {
  font-size: 0.8rem;
  color: #ff4d4d;
  cursor: pointer;
  text-align: right;
  margin-top: 0.3rem;
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
.badge-alumno {
  background-color: #33334d;
  color: #00c3e3;
  font-size: 0.75rem;
  padding: 0.3rem 0.4rem 0.3rem 0.7rem;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}
.sin-alumnos { color: #a0a0b0; font-size: 0.85rem; font-style: italic; }

.quitar-alumno {
  background: transparent;
  border: none;
  color: #ff6b6b;
  cursor: pointer;
  font-size: 0.95rem;
  line-height: 1;
  padding: 0 0.2rem;
}
.quitar-alumno:hover { color: #ff4d4d; }

@media (max-width: 900px) {
  .grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>