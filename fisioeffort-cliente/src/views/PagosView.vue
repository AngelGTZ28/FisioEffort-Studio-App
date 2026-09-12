<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiFetch } from '../api'
import SkeletonTarjetas from '../components/SkeletonTarjetas.vue'

const pagos = ref([])
const alumnos = ref([])
const cargando = ref(true)

const nuevoPago = ref({
  inscripcion: '',
  monto: '',
  mes_cubierto: '',
  metodo_pago: 'EFECTIVO'
})

// --- Buscador de alumno (mismo patrón que en Clases/Alumnos) ---
const busquedaAlumno = ref('')
const alumnoSeleccionado = ref(null)
const mostrarDropdownAlumno = ref(false)

const alumnosFiltrados = computed(() => {
  const activos = alumnos.value.filter((a) => a.activo)
  if (!busquedaAlumno.value) return activos
  return activos.filter((a) =>
    a.nombre_completo.toLowerCase().includes(busquedaAlumno.value.toLowerCase())
  )
})

// Clases activas del alumno seleccionado (ya vienen con inscripcion_id
// gracias a AlumnoSerializer.get_clases_inscritas)
const clasesDelAlumno = computed(() => alumnoSeleccionado.value?.clases_inscritas || [])

const formatoMoneda = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
})

// --- Filtros del historial ---
const modoFiltro = ref('historico') // 'historico' | 'mes' | 'periodo'
const mesFiltro = ref('') // YYYY-MM
const desdeFiltro = ref('') // YYYY-MM-DD
const hastaFiltro = ref('') // YYYY-MM-DD

const pagosFiltrados = computed(() => {
  return pagos.value.filter((pago) => {
    const fecha = String(pago.fecha_registro) // ISO 8601
    if (modoFiltro.value === 'mes' && mesFiltro.value) {
      return fecha.slice(0, 7) === mesFiltro.value
    }
    if (modoFiltro.value === 'periodo') {
      if (!desdeFiltro.value || !hastaFiltro.value) return true
      const dia = fecha.slice(0, 10)
      return dia >= desdeFiltro.value && dia <= hastaFiltro.value
    }
    return true
  })
})

const totalFiltrado = computed(() =>
  pagosFiltrados.value.reduce((suma, p) => suma + Number(p.monto || 0), 0)
)

const filtroActivo = computed(
  () =>
    (modoFiltro.value === 'mes' && mesFiltro.value) ||
    (modoFiltro.value === 'periodo' && desdeFiltro.value && hastaFiltro.value)
)

const limpiarFiltros = () => {
  modoFiltro.value = 'historico'
  mesFiltro.value = ''
  desdeFiltro.value = ''
  hastaFiltro.value = ''
}

// Cargar el historial de pagos
const cargarPagos = async () => {
  try {
    const respuesta = await apiFetch('/pagos/')
    pagos.value = await respuesta.json()
    cargando.value = false
  } catch (error) {
    console.error('Error al cargar pagos:', error)
  }
}

// Cargar alumnos para el buscador del formulario
const cargarAlumnos = async () => {
  try {
    const respuesta = await apiFetch('/alumnos/')
    alumnos.value = await respuesta.json()
  } catch (error) {
    console.error('Error al cargar alumnos:', error)
  }
}

const seleccionarAlumno = (alumno) => {
  alumnoSeleccionado.value = alumno
  busquedaAlumno.value = alumno.nombre_completo
  mostrarDropdownAlumno.value = false

  // Si solo tiene una clase activa, la seleccionamos de una vez.
  // Si tiene varias, dejamos el select vacío para que elija cuál cobrar.
  const clases = alumno.clases_inscritas || []
  nuevoPago.value.inscripcion = clases.length === 1 ? clases[0].inscripcion_id : ''
}

const limpiarSeleccionAlumno = () => {
  alumnoSeleccionado.value = null
  busquedaAlumno.value = ''
  nuevoPago.value.inscripcion = ''
}

const registrarPago = async () => {
  try {
    const respuesta = await apiFetch('/pagos/', {
      method: 'POST',
      body: JSON.stringify(nuevoPago.value)
    })

    if (respuesta.ok) {
      // Limpiamos el formulario y recargamos la lista
      nuevoPago.value = { inscripcion: '', monto: '', mes_cubierto: '', metodo_pago: 'EFECTIVO' }
      limpiarSeleccionAlumno()
      cargarPagos()
      alert('¡Pago registrado con éxito!')
    }
  } catch (error) {
    console.error('Error al registrar pago:', error)
  }
}

onMounted(() => {
  cargarPagos()
  cargarAlumnos()
})
</script>

<template>
  <div class="pagos-container">
    <div class="header-seccion">
      <h2>Caja <span class="morado">Registradora</span></h2>
      <p class="subtitulo">Registra cobros y consulta el historial reciente.</p>
    </div>

    <div class="grid-layout">
      <!-- Columna Izquierda: Formulario de Cobro -->
      <div class="panel">
        <h3>Registrar Nuevo Pago</h3>
        <form @submit.prevent="registrarPago" class="formulario">

          <div class="input-group buscador-personalizado">
            <label>Alumno</label>
            <input
              type="text"
              v-model="busquedaAlumno"
              @focus="mostrarDropdownAlumno = true"
              class="input-busqueda"
              placeholder="Buscar alumno por nombre..."
              autocomplete="off"
              required
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

          <!-- Solo aparece una vez que hay un alumno elegido -->
          <div v-if="alumnoSeleccionado" class="input-group">
            <template v-if="clasesDelAlumno.length === 0">
              <p class="aviso-sin-clase">
                {{ alumnoSeleccionado.nombre_completo }} no tiene ninguna clase activa.
                Inscríbelo en una clase antes de registrarle un pago.
              </p>
            </template>
            <template v-else-if="clasesDelAlumno.length === 1">
              <label>Clase</label>
              <p class="clase-unica">{{ clasesDelAlumno[0].clase_nombre }}</p>
            </template>
            <template v-else>
              <label>¿Qué clase está pagando?</label>
              <select v-model="nuevoPago.inscripcion" required>
                <option value="" disabled>-- Selecciona una clase --</option>
                <option v-for="c in clasesDelAlumno" :key="c.inscripcion_id" :value="c.inscripcion_id">
                  {{ c.clase_nombre }}{{ c.tipo === 'PRUEBA' ? ' (Prueba)' : '' }}
                </option>
              </select>
            </template>
          </div>

          <div class="input-group">
            <label>Monto a Cobrar ($)</label>
            <input type="number" v-model="nuevoPago.monto" required min="1" step="0.50" placeholder="Ej. 500.00">
          </div>

          <div class="input-group">
            <label>Mes que cubre</label>
            <input type="text" v-model="nuevoPago.mes_cubierto" required placeholder="Ej. Septiembre 2026">
          </div>

          <div class="input-group">
            <label>Método de Pago</label>
            <select v-model="nuevoPago.metodo_pago" required>
              <option value="EFECTIVO">Efectivo</option>
              <option value="TARJETA">Tarjeta</option>
              <option value="TRANSFERENCIA">Transferencia Bancaria</option>
            </select>
          </div>

          <button type="submit" class="btn-guardar" :disabled="!nuevoPago.inscripcion">
            Registrar Ingreso
          </button>
        </form>
      </div>

      <!-- Columna Derecha: Historial de Pagos -->
      <div class="panel">
        <h3>Historial Reciente</h3>

        <div class="filtros-historial">
          <select v-model="modoFiltro" class="input-filtro">
            <option value="historico">Histórico completo</option>
            <option value="mes">Por mes</option>
            <option value="periodo">Por periodo</option>
          </select>

          <input
            v-if="modoFiltro === 'mes'"
            v-model="mesFiltro"
            type="month"
            class="input-filtro"
            aria-label="Mes a filtrar"
          >

          <template v-if="modoFiltro === 'periodo'">
            <input v-model="desdeFiltro" type="date" class="input-filtro" aria-label="Fecha inicial">
            <span class="filtro-sep">a</span>
            <input v-model="hastaFiltro" type="date" class="input-filtro" aria-label="Fecha final">
          </template>

          <button v-if="filtroActivo" class="btn-limpiar" @click="limpiarFiltros">Limpiar</button>
        </div>

        <div v-if="filtroActivo" class="resumen-filtro">
          {{ pagosFiltrados.length }}
          {{ pagosFiltrados.length === 1 ? 'pago' : 'pagos' }} ·
          {{ formatoMoneda.format(totalFiltrado) }}
        </div>

        <SkeletonTarjetas v-if="cargando" :tarjetas="4" tipo="pagos" />

        <div v-else class="lista-pagos">
          <div v-if="pagos.length === 0" class="sin-datos">
            Aún no hay pagos registrados.
          </div>
          <div v-else-if="pagosFiltrados.length === 0" class="sin-datos">
            Sin resultados para este filtro.
          </div>

          <div v-for="pago in pagosFiltrados" v-else :key="pago.id" class="tarjeta-pago">
            <div class="pago-header">
              <h4>{{ pago.alumno_nombre }}</h4>
              <span class="monto-badge">{{ formatoMoneda.format(pago.monto) }}</span>
            </div>
            <div class="pago-body">
              <p><span class="label">Clase:</span> {{ pago.clase_nombre }}</p>
              <p><span class="label">Mes:</span> {{ pago.mes_cubierto }}</p>
              <p><span class="label">Método:</span> {{ pago.metodo_pago }}</p>
            </div>
            <div class="pago-footer">
              <small>{{ new Date(pago.fecha_registro).toLocaleString() }}</small>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.pagos-container { padding: 1rem; }
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

.clase-unica {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: #00c3e3;
  padding: 0.8rem;
  border-radius: 6px;
  font-weight: bold;
  margin: 0;
}

.aviso-sin-clase {
  color: #ff6b6b;
  font-size: 0.85rem;
  background-color: #2a1a1f;
  border: 1px solid #ff4d4d;
  border-radius: 6px;
  padding: 0.75rem;
  margin: 0;
}

.btn-guardar {
  background-color: #2e8b57; /* Verde para que parezca dinero/éxito */
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

/* Filtros del historial */
.filtros-historial {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  align-items: center;
  margin-bottom: 1rem;
}

.input-filtro {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: #f5f5fa;
  padding: 0.6rem 0.8rem;
  border-radius: 6px;
  outline: none;
  color-scheme: dark;
  font-size: 0.9rem;
}
.input-filtro:focus { border-color: #00c3e3; }

.filtro-sep { color: #a0a0b0; font-size: 0.9rem; }

.btn-limpiar {
  background: transparent;
  border: 1px solid #ff6b6b;
  color: #ff6b6b;
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.8rem;
  transition: background-color 0.2s, color 0.2s;
}
.btn-limpiar:hover { background-color: #ff6b6b; color: #12121a; }

.resumen-filtro {
  background-color: #23233b;
  border-left: 3px solid #00c3e3;
  color: #00c3e3;
  font-weight: bold;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

/* Buscador de alumno (mismo patrón que Clases/Alumnos) */
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

/* Tarjetas de Pagos */
.lista-pagos { display: flex; flex-direction: column; gap: 1rem; }
.tarjeta-pago {
  background-color: #23233b;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #2e8b57;
}
.pago-header { display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; }
.pago-header h4 { margin: 0; color: white; font-size: 1.1rem; }
.monto-badge { background-color: #2e8b57; color: white; padding: 0.3rem 0.6rem; border-radius: 12px; font-weight: bold; white-space: nowrap; }

.pago-body p { margin: 0.3rem 0; color: #d0d0e0; font-size: 0.9rem; }
.label { color: #a0a0b0; font-weight: bold; }

.pago-footer { margin-top: 1rem; border-top: 1px solid #33334d; padding-top: 0.5rem; color: #606070; text-align: right; }
.sin-datos { color: #a0a0b0; font-style: italic; }

@media (max-width: 900px) {
  .grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>