<script setup>
import { ref, onMounted, computed } from 'vue'

const alumnos = ref([])
const tutores = ref([])
const clases = ref([]) // <-- Nueva variable para las clases
const cargando = ref(true)

// Control de las pestañas Activos / Inactivos
const mostrarActivos = ref(true)

// Formularios
const nuevoAlumno = ref({
  nombre_completo: '', tutor: '', fecha_nacimiento: '', ha_tomado_clase_prueba: false
})
const busquedaTutor = ref('')
const mostrarDropdown = ref(false)

// Objeto para la inscripción automática
const nuevaInscripcion = ref({
  clase: '',
  tipo: 'REGULAR' // Puede ser REGULAR o PRUEBA
})

// --- COMPUTED PARA FILTROS ---
const tutoresFiltrados = computed(() => {
  if (!busquedaTutor.value) return tutores.value
  return tutores.value.filter(t => t.nombre_completo.toLowerCase().includes(busquedaTutor.value.toLowerCase()))
})

const alumnosActivos = computed(() => alumnos.value.filter(a => a.activo === true))
const alumnosInactivos = computed(() => alumnos.value.filter(a => a.activo === false))

// --- FUNCIONES DE CARGA ---
const cargarDatos = async () => {
  try {
    const [resAlumnos, resTutores, resClases] = await Promise.all([
      fetch('http://127.0.0.1:8000/api/alumnos/'),
      fetch('http://127.0.0.1:8000/api/tutores/'),
      fetch('http://127.0.0.1:8000/api/clases/') // <-- Cargamos las clases
    ])
    alumnos.value = await resAlumnos.json()
    tutores.value = await resTutores.json()
    clases.value = await resClases.json()
    cargando.value = false
  } catch (error) {
    console.error('Error al cargar datos:', error)
  }
}

const seleccionarTutor = (tutor) => {
  if (tutor) {
    nuevoAlumno.value.tutor = tutor.id
    busquedaTutor.value = tutor.nombre_completo
  } else {
    nuevoAlumno.value.tutor = ''
    busquedaTutor.value = ''
  }
  mostrarDropdown.value = false
}

// --- FUNCIÓN UNIFICADA (ALUMNO + INSCRIPCIÓN) ---
const guardarAlumno = async () => {
  try {
    const payloadAlumno = { ...nuevoAlumno.value }
    if (payloadAlumno.tutor === '') payloadAlumno.tutor = null

    // 1. Creamos al Alumno
    const resAlumno = await fetch('http://127.0.0.1:8000/api/alumnos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payloadAlumno)
    })

    if (resAlumno.ok) {
      const alumnoCreado = await resAlumno.json() // Extraemos el ID generado

      // 2. Si eligió una clase, creamos la Inscripción inmediatamente
      if (nuevaInscripcion.value.clase !== '') {
        await fetch('http://127.0.0.1:8000/api/inscripciones/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            alumno: alumnoCreado.id,
            clase: nuevaInscripcion.value.clase,
            tipo: nuevaInscripcion.value.tipo
          })
        })
      }

      // Limpiamos formularios y recargamos
      nuevoAlumno.value = { nombre_completo: '', tutor: '', fecha_nacimiento: '', ha_tomado_clase_prueba: false }
      busquedaTutor.value = ''
      nuevaInscripcion.value = { clase: '', tipo: 'REGULAR' }
      cargarDatos()
    }
  } catch (error) {
    console.error('Error al guardar:', error)
  }
}

// --- FUNCIÓN PARA DAR DE BAJA / REACTIVAR ---
const cambiarEstadoAlumno = async (alumno) => {
  // Confirmación por seguridad (opcional pero recomendada)
  const accion = alumno.activo ? 'dar de baja' : 'reactivar'
  if (!confirm(`¿Estás seguro de que deseas ${accion} a ${alumno.nombre_completo}?`)) return

  try {
    const respuesta = await fetch(`http://127.0.0.1:8000/api/alumnos/${alumno.id}/`, {
      method: 'PATCH', // Usamos PATCH porque solo actualizaremos un campo, no todo el registro
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ activo: !alumno.activo }) // Invertimos su estado actual
    })

    if (respuesta.ok) {
      cargarDatos() // Recargamos la lista para que desaparezca de los activos
    } else {
      console.error('Error del servidor al actualizar')
    }
  } catch (error) {
    console.error('Error de red al cambiar estado:', error)
  }
}

onMounted(() => { cargarDatos() })
</script>

<template>
  <div class="alumnos-container">
    <div class="header-seccion">
      <h2>Gestión de <span class="cian">Alumnos</span></h2>
      <p class="subtitulo">Registra alumnos nuevos y administra el directorio.</p>
    </div>

    <div class="grid-layout">
      <!-- PANEL IZQUIERDO: FORMULARIO -->
      <div class="panel">
        <h3>Nuevo Registro</h3>
        <form @submit.prevent="guardarAlumno" class="formulario">
          <div class="input-group">
            <label>Nombre Completo</label>
            <input type="text" v-model="nuevoAlumno.nombre_completo" required>
          </div>

          <div class="input-group buscador-personalizado">
            <label>Tutor (Opcional)</label>
            <input type="text" v-model="busquedaTutor" @focus="mostrarDropdown = true" class="input-busqueda">
            <ul v-if="mostrarDropdown" class="dropdown-lista">
              <li @click="seleccionarTutor(null)" class="opcion-nula">-- Sin tutor --</li>
              <li v-if="tutoresFiltrados.length === 0" class="sin-resultados">
                No se encontraron tutores
              </li>
              <li v-for="tutor in tutoresFiltrados" :key="tutor.id" @click="seleccionarTutor(tutor)">
                {{ tutor.nombre_completo }}
              </li>
            </ul>
            <span v-if="mostrarDropdown" class="btn-cerrar" @click="mostrarDropdown = false">Cerrar</span>
          </div>

          <div class="input-group">
            <label>Fecha Nacimiento</label>
            <input type="date" v-model="nuevoAlumno.fecha_nacimiento" required>
          </div>

          <hr class="separador">
          <h4 class="subtitulo-form">Asignación de Clase (Opcional)</h4>

          <div class="input-group">
            <label>Seleccionar Clase</label>
            <select v-model="nuevaInscripcion.clase" class="input-busqueda">
              <option value="">-- No inscribir por ahora --</option>
              <option v-for="clase in clases" :key="clase.id" :value="clase.id">
                {{ clase.nombre }} (Cupo: {{ clase.capacidad_maxima }})
              </option>
            </select>
          </div>

          <div class="input-group" v-if="nuevaInscripcion.clase !== ''">
            <label>Tipo de Inscripción</label>
            <select v-model="nuevaInscripcion.tipo" class="input-busqueda">
              <option value="REGULAR">Regular (Pago normal)</option>
              <option value="PRUEBA">Clase de Prueba</option>
            </select>
          </div>

          <button type="submit" class="btn-guardar">Registrar e Inscribir</button>
        </form>
      </div>

      <!-- PANEL DERECHO: LISTA Y FILTROS -->
      <div class="panel">
        <div class="header-lista">
          <h3>Directorio</h3>
          <div class="tabs">
            <button :class="{ activo: mostrarActivos }" @click="mostrarActivos = true">Activos</button>
            <button :class="{ activo: !mostrarActivos }" @click="mostrarActivos = false">Inactivos</button>
          </div>
        </div>

        <p v-if="cargando" class="cargando">Cargando datos...</p>
        <p
          v-else-if="(mostrarActivos ? alumnosActivos : alumnosInactivos).length === 0"
          class="vacio"
        >
          {{ mostrarActivos ? 'No hay alumnos activos por ahora.' : 'No hay alumnos dados de baja.' }}
        </p>
        <ul v-else class="lista">
          <li v-for="alumno in (mostrarActivos ? alumnosActivos : alumnosInactivos)" :key="alumno.id">
            <div class="info-alumno">
              <span class="nombre" :class="{ tachado: !alumno.activo }">{{ alumno.nombre_completo }}</span>
              <span v-if="alumno.nombre_tutor" class="tutor-info">Tutor: {{ alumno.nombre_tutor }}</span>

              <div class="badges-clases">
                <span v-if="alumno.clases_inscritas.length === 0" class="badge-gris">Sin clase asignada</span>
                <span v-for="(clase, index) in alumno.clases_inscritas" :key="index" class="badge-clase">
                  {{ clase }}
                </span>
              </div>
            </div>
            <div class="acciones-alumno">
              <span v-if="!alumno.activo" class="badge-rojo">Baja</span>
              <button
                @click="cambiarEstadoAlumno(alumno)"
                class="btn-estado"
                :class="alumno.activo ? 'btn-peligro' : 'btn-exito'"
              >
                {{ alumno.activo ? 'Dar de baja' : 'Reactivar' }}
              </button>
            </div>
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
.subtitulo { color: #a0a0b0; margin-top: 0.35rem; }

.grid-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
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
  gap: 1rem;
}
.info-alumno { display: flex; flex-direction: column; gap: 0.2rem; min-width: 0; }
.nombre { font-weight: bold; color: white; }
.tutor-info { font-size: 0.85rem; color: #00c3e3; }

.cargando {
  color: #8a2be2;
  font-style: italic;
}
.vacio {
  color: #a0a0b0;
  font-style: italic;
}

/* Buscador de Tutores */
.buscador-personalizado {
  position: relative;
}

.input-busqueda {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.8rem;
  border-radius: 6px;
  outline: none;
  width: 100%;
  appearance: none;
}
.input-busqueda:focus {
  border-color: #00c3e3;
}

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

.dropdown-lista li:hover {
  background-color: #8a2be2;
}

.opcion-nula {
  color: #a0a0b0 !important;
  font-style: italic;
}

.sin-resultados {
  color: #ff4d4d !important;
  cursor: default;
  font-style: italic;
}
.sin-resultados:hover {
  background-color: transparent !important;
}

.btn-cerrar {
  font-size: 0.8rem;
  color: #ff4d4d;
  cursor: pointer;
  text-align: right;
  margin-top: 0.3rem;
}

.separador { border: none; border-top: 1px solid #33334d; margin: 1rem 0; }
.subtitulo-form { color: #8a2be2; margin-bottom: 0.5rem; font-size: 0.95rem; }

.header-lista { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 0.75rem; }
.tabs { display: flex; gap: 0.5rem; }
.tabs button {
  background: transparent;
  color: #a0a0b0;
  border: 1px solid #33334d;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}
.tabs button.activo { background-color: #00c3e3; color: #12121a; border-color: #00c3e3; font-weight: bold; }

.badges-clases { display: flex; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap; }
.badge-clase { background-color: #2e8b57; color: white; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
.badge-gris { background-color: #33334d; color: #a0a0b0; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
.badge-rojo { background-color: #ff4d4d; color: white; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
.tachado { text-decoration: line-through; opacity: 0.6; }

.acciones-alumno { display: flex; flex-direction: column; align-items: flex-end; gap: 0.5rem; flex-shrink: 0; }

.btn-estado {
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: bold;
  cursor: pointer;
  color: white;
  transition: opacity 0.2s;
}
.btn-estado:hover { opacity: 0.8; }

.btn-peligro { background-color: transparent; border: 1px solid #ff4d4d; color: #ff4d4d; }
.btn-peligro:hover { background-color: #ff4d4d; color: white; }

.btn-exito { background-color: transparent; border: 1px solid #2e8b57; color: #2e8b57; }
.btn-exito:hover { background-color: #2e8b57; color: white; }

@media (max-width: 900px) {
  .grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>