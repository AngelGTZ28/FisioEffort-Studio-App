<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiFetch } from '../api'
import SkeletonLista from '../components/SkeletonLista.vue'
import { useAlumnosStore } from '../stores/alumnos'
import { useTutoresStore } from '../stores/tutores'
import { useClasesStore } from '../stores/clases'
import { useUiStore } from '../stores/ui'

const alumnosStore = useAlumnosStore()
const tutoresStore = useTutoresStore()
const clasesStore = useClasesStore()
const ui = useUiStore()

const clases = computed(() => clasesStore.clases)

const cargando = computed(() => alumnosStore.cargando || tutoresStore.cargando || clasesStore.cargando)

// Control de las pestañas Activos / Inactivos
const mostrarActivos = ref(true)

// Formularios
const nuevoAlumno = ref({
  nombre_completo: '', tutor: '', fecha_nacimiento: '', ha_tomado_clase_prueba: false
})
const busquedaTutor = ref('')
const mostrarDropdown = ref(false)

// Objeto para la inscripción automática (al crear al alumno)
const nuevaInscripcion = ref({
  clase: '',
  tipo: 'REGULAR' // Puede ser REGULAR o PRUEBA
})

// --- Gestión de clase para un alumno YA EXISTENTE ---
const alumnoEditandoClase = ref(null) // id del alumno cuyo mini-formulario está abierto
const formClaseRapida = ref({ clase: '', tipo: 'REGULAR' })
const enviandoInscripcionRapida = ref(false)

// --- COMPUTED PARA FILTROS ---
const tutoresFiltrados = computed(() => {
  if (!busquedaTutor.value) return tutoresStore.tutores
  return tutoresStore.tutores.filter(t => t.nombre_completo.toLowerCase().includes(busquedaTutor.value.toLowerCase()))
})

const alumnosActivos = computed(() => alumnosStore.alumnosActivos)
const alumnosInactivos = computed(() => alumnosStore.alumnosInactivos)

// Clases en las que el alumno TODAVÍA no está inscrito (para no ofrecer duplicados)
function clasesDisponiblesPara(alumno) {
  const idsActuales = alumno.clases_inscritas.map((c) => c.clase_id)
  return clasesStore.clases.filter((c) => !idsActuales.includes(c.id))
}

// --- FUNCIONES DE CARGA ---
const cargarDatos = async (forzar = false) => {
  await Promise.all([
    alumnosStore.fetchAlumnos(forzar),
    tutoresStore.fetchTutores(forzar),
    clasesStore.fetchClases(forzar)
  ])
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
    const resAlumno = await apiFetch('/alumnos/', {
      method: 'POST',
      body: JSON.stringify(payloadAlumno)
    })

    if (resAlumno.ok) {
      const alumnoCreado = await resAlumno.json() // Extraemos el ID generado
      
      // Actualización optimista: inyectar el alumno en el store local inmediatamente
      // Si no eligió clase, lo inyectamos ya con un array vacío para clases_inscritas
      if (!alumnoCreado.clases_inscritas) {
         alumnoCreado.clases_inscritas = []
      }
      alumnosStore.agregarAlumnoLocal(alumnoCreado)

      // 2. Si eligió una clase, creamos la Inscripción inmediatamente
      if (nuevaInscripcion.value.clase !== '') {
        await apiFetch('/inscripciones/', {
          method: 'POST',
          body: JSON.stringify({
            alumno: alumnoCreado.id,
            clase: nuevaInscripcion.value.clase,
            tipo: nuevaInscripcion.value.tipo
          })
        })
        // Como las inscripciones afectan clases_inscritas complejas, recargamos el store de alumnos
        await alumnosStore.fetchAlumnos(true)
      }

      // Limpiamos formularios
      nuevoAlumno.value = { nombre_completo: '', tutor: '', fecha_nacimiento: '', ha_tomado_clase_prueba: false }
      busquedaTutor.value = ''
      nuevaInscripcion.value = { clase: '', tipo: 'REGULAR' }
    }
  } catch (error) {
    console.error('Error al guardar:', error)
  }
}

// --- FUNCIÓN PARA DAR DE BAJA / REACTIVAR ---
const cambiarEstadoAlumno = async (alumno) => {
  // Confirmación por seguridad
  const accion = alumno.activo ? 'dar de baja' : 'reactivar'
  const confirmado = await ui.mostrarConfirmacion(`¿Estás seguro de que deseas ${accion} a ${alumno.nombre_completo}?`, 'Confirmación')
  if (!confirmado) return

  try {
    const respuesta = await apiFetch(`/alumnos/${alumno.id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ activo: !alumno.activo })
    })

    if (respuesta.ok) {
      // Cambio ultra-rápido en memoria, sin re-fetchear todos los alumnos
      alumnosStore.cambiarEstadoLocal(alumno.id, !alumno.activo)
    } else {
      console.error('Error del servidor al actualizar')
    }
  } catch (error) {
    console.error('Error de red al cambiar estado:', error)
  }
}

// --- GESTIÓN DE CLASE PARA UN ALUMNO EXISTENTE ---
function abrirFormClase(alumno) {
  alumnoEditandoClase.value = alumno.id
  formClaseRapida.value = { clase: '', tipo: 'REGULAR' }
}

function cerrarFormClase() {
  alumnoEditandoClase.value = null
}

function extraerMensajeError(datosError) {
  if (!datosError || typeof datosError !== 'object') {
    return 'No se pudo completar la inscripción.'
  }
  const mensajes = Object.values(datosError).flat()
  return mensajes.length > 0 ? mensajes.join(' ') : 'No se pudo completar la inscripción.'
}

const inscribirEnClase = async (alumno) => {
  if (!formClaseRapida.value.clase) {
    await ui.mostrarAlerta('Selecciona una clase.', 'Atención')
    return
  }

  enviandoInscripcionRapida.value = true
  try {
    const respuesta = await apiFetch('/inscripciones/', {
      method: 'POST',
      body: JSON.stringify({
        alumno: alumno.id,
        clase: formClaseRapida.value.clase,
        tipo: formClaseRapida.value.tipo
      })
    })

    const datos = await respuesta.json()

    if (respuesta.ok) {
      cerrarFormClase()
      // Invalidar caché de alumnos para reflejar la nueva clase y cupos
      await Promise.all([
        alumnosStore.fetchAlumnos(true),
        clasesStore.fetchClases(true)
      ])
    } else {
      await ui.mostrarAlerta(extraerMensajeError(datos), 'No se pudo inscribir')
    }
  } catch (error) {
    console.error('Error al inscribir en clase:', error)
    await ui.mostrarAlerta('Error de red al inscribir al alumno.', 'Error de red')
  } finally {
    enviandoInscripcionRapida.value = false
  }
}

const quitarDeClase = async (inscripcionId, alumnoNombre, claseNombre) => {
  const confirmado = await ui.mostrarConfirmacion(`¿Quitar a ${alumnoNombre} de ${claseNombre}?`, 'Baja de Clase')
  if (!confirmado) return

  try {
    const respuesta = await apiFetch(`/inscripciones/${inscripcionId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ activa: false })
    })

    if (respuesta.ok) {
      // Recargar alumnos y clases para reflejar el cupo recuperado y badges quitados
      await Promise.all([
        alumnosStore.fetchAlumnos(true),
        clasesStore.fetchClases(true)
      ])
    } else {
      await ui.mostrarAlerta('No se pudo quitar al alumno de la clase.', 'Error')
    }
  } catch (error) {
    console.error('Error al quitar de clase:', error)
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

        <SkeletonLista v-if="cargando" :filas="4" />
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
                <span v-for="c in alumno.clases_inscritas" :key="c.inscripcion_id" class="badge-clase">
                  {{ c.clase_nombre }}
                  <button
                    v-if="alumno.activo"
                    class="quitar-clase"
                    title="Quitar de esta clase"
                    @click="quitarDeClase(c.inscripcion_id, alumno.nombre_completo, c.clase_nombre)"
                  >×</button>
                </span>
                <button
                  v-if="alumno.activo && alumnoEditandoClase !== alumno.id"
                  class="badge-agregar"
                  @click="abrirFormClase(alumno)"
                >
                  + Agregar clase
                </button>
              </div>

              <!-- Mini-formulario para inscribir a un alumno existente en otra clase -->
              <div v-if="alumnoEditandoClase === alumno.id" class="form-clase-rapida">
                <select v-model="formClaseRapida.clase">
                  <option value="">-- Selecciona una clase --</option>
                  <option v-for="c in clasesDisponiblesPara(alumno)" :key="c.id" :value="c.id">
                    {{ c.nombre }} ({{ c.lugares_disponibles }} lugares)
                  </option>
                </select>
                <select v-model="formClaseRapida.tipo">
                  <option value="REGULAR">Regular</option>
                  <option value="PRUEBA">Prueba</option>
                </select>
                <div class="botones-form-rapida">
                  <button
                    class="btn-mini btn-mini--ok"
                    :disabled="enviandoInscripcionRapida"
                    @click="inscribirEnClase(alumno)"
                  >
                    {{ enviandoInscripcionRapida ? 'Inscribiendo...' : 'Inscribir' }}
                  </button>
                  <button class="btn-mini btn-mini--cancelar" @click="cerrarFormClase">Cancelar</button>
                </div>
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
  max-width: 100%;
  box-sizing: border-box;
}

.panel h3 { color: #8a2be2; margin-bottom: 1.5rem; word-break: break-word; }

.formulario { display: flex; flex-direction: column; gap: 1.5rem; }
.input-group { display: flex; flex-direction: column; gap: 0.5rem; max-width: 100%; box-sizing: border-box; }
label { color: #a0a0b0; font-size: 0.9rem; }

input[type="text"], input[type="date"], select {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.8rem;
  border-radius: 6px;
  outline: none;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
input[type="text"]:focus, input[type="date"]:focus, select:focus {
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
  width: 100%;
  box-sizing: border-box;
}
.btn-guardar:hover { opacity: 0.8; }

.lista { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 1rem; max-width: 100%; box-sizing: border-box; }
.lista li {
  background-color: #23233b;
  padding: 1rem;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  max-width: 100%;
  box-sizing: border-box;
}
.info-alumno { display: flex; flex-direction: column; gap: 0.2rem; min-width: 0; flex: 1; }
.nombre { font-weight: bold; color: white; word-break: break-word; }
.tutor-info { font-size: 0.85rem; color: #00c3e3; word-break: break-word; }

.vacio {
  color: #a0a0b0;
  font-style: italic;
}

/* Buscador de Tutores */
.buscador-personalizado {
  position: relative;
  max-width: 100%;
  box-sizing: border-box;
}

.input-busqueda {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.8rem;
  border-radius: 6px;
  outline: none;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
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

.badges-clases { display: flex; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap; align-items: center; }
.badge-clase {
  background-color: #2e8b57;
  color: white;
  font-size: 0.75rem;
  padding: 0.3rem 0.4rem 0.3rem 0.6rem;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.badge-gris { background-color: #33334d; color: #a0a0b0; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
.badge-rojo { background-color: #ff4d4d; color: white; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
.tachado { text-decoration: line-through; opacity: 0.6; }

.quitar-clase {
  background: transparent;
  border: none;
  color: #f0fff5;
  cursor: pointer;
  font-size: 0.9rem;
  line-height: 1;
  padding: 0 0.1rem;
  opacity: 0.8;
}
.quitar-clase:hover { opacity: 1; }

.badge-agregar {
  background-color: transparent;
  border: 1px dashed #33334d;
  color: #a0a0b0;
  font-size: 0.75rem;
  padding: 0.3rem 0.6rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}
.badge-agregar:hover { border-color: #00c3e3; color: #00c3e3; }

.form-clase-rapida {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.6rem;
  padding: 0.75rem;
  background-color: #1a1a2e;
  border-radius: 8px;
  align-items: center;
  max-width: 100%;
  box-sizing: border-box;
}
.form-clase-rapida select {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 0.5rem;
  border-radius: 6px;
  outline: none;
  max-width: 100%;
  box-sizing: border-box;
  flex: 1 1 0%;
  min-width: 0;
}
.form-clase-rapida select:focus { border-color: #00c3e3; }

.botones-form-rapida { display: flex; gap: 0.5rem; flex-wrap: wrap; max-width: 100%; box-sizing: border-box; }
.btn-mini {
  border: none;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-mini:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-mini--ok { background-color: #00c3e3; color: #12121a; }
.btn-mini--ok:hover { opacity: 0.8; }
.btn-mini--cancelar { background-color: transparent; border: 1px solid #33334d; color: #a0a0b0; }
.btn-mini--cancelar:hover { color: white; border-color: #a0a0b0; }

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

@media (max-width: 768px) {
  .form-clase-rapida {
    width: 100%;
    flex-direction: column;
    gap: 0.75rem;
    align-items: stretch;
  }
  .form-clase-rapida select {
    width: 100%;
    min-height: 42px;
    font-size: 16px;
    flex: none; /* overrides flex: 1 1 0% */
  }
  .botones-form-rapida {
    width: 100%;
    justify-content: space-between;
  }
  .botones-form-rapida .btn-mini {
    flex: 1;
    text-align: center;
  }
}
</style>