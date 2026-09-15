<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import SkeletonKPIs from '../components/SkeletonKPIs.vue'
import SkeletonLista from '../components/SkeletonLista.vue'

import { useAlumnosStore } from '../stores/alumnos'
import { useTutoresStore } from '../stores/tutores'
import { useClasesStore } from '../stores/clases'
import { usePagosStore } from '../stores/pagos'

const router = useRouter()

const irA = (ruta) => {
  router.push(ruta)
}

const alumnosStore = useAlumnosStore()
const tutoresStore = useTutoresStore()
const clasesStore = useClasesStore()
const pagosStore = usePagosStore()

const alumnos = computed(() => alumnosStore.alumnos)
const tutores = computed(() => tutoresStore.tutores)
const clases = computed(() => clasesStore.clases)
const pagos = computed(() => pagosStore.pagos)

const estado = computed(() => ({
  alumnos: { cargando: alumnosStore.cargando, error: false },
  tutores: { cargando: tutoresStore.cargando, error: false },
  clases: { cargando: clasesStore.cargando, error: false },
  pagos: { cargando: pagosStore.cargando, error: false },
}))

const kpisCargando = computed(() => 
  alumnosStore.cargando || tutoresStore.cargando || clasesStore.cargando || pagosStore.cargando
)

onMounted(() => {
  alumnosStore.fetchAlumnos()
  tutoresStore.fetchTutores()
  clasesStore.fetchClases()
  pagosStore.fetchPagos()
})

const formatoMoneda = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
})

// --- Total recaudado del mes en curso ---
const obtenerMesActual = () => {
  const ahora = new Date()
  return `${ahora.getFullYear()}-${String(ahora.getMonth() + 1).padStart(2, '0')}` // YYYY-MM
}

const formatoMes = new Intl.DateTimeFormat('es-MX', { year: 'numeric', month: 'long' })

// Se construye en hora local para evitar que '2026-09-01' se interprete como
// medianoche UTC y en zonas con offset negativo caiga en el mes anterior.
const [anioMes, mesNumero] = obtenerMesActual().split('-')
const etiquetaMesActual = formatoMes.format(new Date(Number(anioMes), Number(mesNumero) - 1, 1))

const totalRecaudado = computed(() =>
  pagos.value
    .filter((p) => String(p.fecha_registro).slice(0, 7) === obtenerMesActual())
    .reduce((suma, p) => suma + Number(p.monto || 0), 0)
)

// KPIs derivados de los campos reales de tus serializers.
const alumnosActivos = computed(() => alumnos.value.filter((a) => a.activo).length)
const totalTutores = computed(() => tutores.value.length)
const totalClases = computed(() => clases.value.length)
const cuposDisponibles = computed(() =>
  clases.value.reduce((suma, c) => suma + (c.lugares_disponibles ?? 0), 0)
)
</script>

<template>
  <div class="dashboard">
    <header class="encabezado">
      <h2>Panel Principal</h2>
      <p>Bienvenido al sistema de control de FisioEffort Studio.</p>
    </header>

    <!-- Fila de KPIs: el vistazo rápido antes de entrar al detalle -->
    <template v-if="kpisCargando">
      <SkeletonKPIs />
    </template>
    <section v-else class="kpis">
      <div class="kpi kpi--cian">
        <span class="kpi-numero">{{ alumnosActivos }}</span>
        <span class="kpi-etiqueta">Alumnos activos</span>
      </div>
      <div class="kpi kpi--morado">
        <span class="kpi-numero">{{ totalTutores }}</span>
        <span class="kpi-etiqueta">Tutores</span>
      </div>
      <div class="kpi kpi--cian">
        <span class="kpi-numero">{{ cuposDisponibles }}</span>
        <span class="kpi-etiqueta">Cupos disponibles en {{ totalClases }} clases</span>
      </div>
      <div class="kpi kpi--morado">
        <span class="kpi-numero">{{ formatoMoneda.format(totalRecaudado) }}</span>
        <span class="kpi-etiqueta">Recaudado en {{ etiquetaMesActual }}</span>
      </div>
    </section>

    <!-- Detalle por área: cada tarjeta completa navega a su sección -->
    <section class="tarjetas">
      <div
        class="tarjeta tarjeta--cian interactiva"
        role="button"
        tabindex="0"
        @click="irA('/alumnos')"
        @keyup.enter="irA('/alumnos')"
      >
        <div class="tarjeta-encabezado">
          <h3>Alumnos <span class="flecha">➔</span></h3>
        </div>

        <SkeletonLista v-if="estado.alumnos.cargando" :filas="3" />
        <p v-else-if="estado.alumnos.error" class="error">No se pudo cargar la información de alumnos.</p>
        <p v-else-if="alumnos.length === 0" class="vacio">Aún no hay alumnos registrados.</p>
        <ul v-else class="lista" @click.stop>
          <li v-for="alumno in alumnos" :key="alumno.id">
            <span class="acento acento--cian">#{{ alumno.id }}</span>
            <div class="lista-item-cuerpo">
              <span>{{ alumno.nombre_completo }}</span>
              <span class="lista-item-detalle">
                {{ alumno.nombre_tutor || 'Sin tutor asignado' }}
                <template v-if="alumno.clases_inscritas?.length">
                  · {{ alumno.clases_inscritas.map((c) => c.clase_nombre).join(', ') }}
                </template>
              </span>
            </div>
            <span
              class="etiqueta-mini"
              :class="alumno.activo ? 'etiqueta-mini--ok' : 'etiqueta-mini--alerta'"
            >
              {{ alumno.activo ? 'Activo' : 'Inactivo' }}
            </span>
          </li>
        </ul>
      </div>

      <div
        class="tarjeta tarjeta--morado interactiva"
        role="button"
        tabindex="0"
        @click="irA('/tutores')"
        @keyup.enter="irA('/tutores')"
      >
        <div class="tarjeta-encabezado">
          <h3>Tutores <span class="flecha">➔</span></h3>
        </div>

        <SkeletonLista v-if="estado.tutores.cargando" :filas="3" />
        <p v-else-if="estado.tutores.error" class="error">No se pudo cargar la información de tutores.</p>
        <p v-else-if="tutores.length === 0" class="vacio">Aún no hay tutores registrados.</p>
        <ul v-else class="lista" @click.stop>
          <li v-for="tutor in tutores" :key="tutor.id">
            <span class="acento acento--morado">#{{ tutor.id }}</span>
            <div class="lista-item-cuerpo">
              <span>{{ tutor.nombre_completo }}</span>
              <span v-if="tutor.telefono || tutor.correo" class="lista-item-detalle">
                {{ tutor.telefono }}<template v-if="tutor.telefono && tutor.correo"> · </template>{{ tutor.correo }}
              </span>
            </div>
          </li>
        </ul>
      </div>

      <div
        class="tarjeta tarjeta--cian interactiva"
        role="button"
        tabindex="0"
        @click="irA('/clases')"
        @keyup.enter="irA('/clases')"
      >
        <div class="tarjeta-encabezado">
          <h3>Clases <span class="flecha">➔</span></h3>
        </div>

        <SkeletonLista v-if="estado.clases.cargando" :filas="3" />
        <p v-else-if="estado.clases.error" class="error">No se pudo cargar la información de clases.</p>
        <p v-else-if="clases.length === 0" class="vacio">Aún no hay clases registradas.</p>
        <ul v-else class="lista" @click.stop>
          <li v-for="clase in clases" :key="clase.id">
            <div class="lista-item-cuerpo">
              <span class="acento acento--cian">{{ clase.nombre }}</span>
              <span class="lista-item-detalle">
                {{ clase.alumnos_inscritos.length }} / {{ clase.capacidad_maxima }} inscritos
              </span>
            </div>
            <span
              class="etiqueta-mini"
              :class="clase.lugares_disponibles > 0 ? 'etiqueta-mini--ok' : 'etiqueta-mini--alerta'"
            >
              {{ clase.lugares_disponibles > 0 ? `${clase.lugares_disponibles} cupos` : 'Cupo lleno' }}
            </span>
          </li>
        </ul>
      </div>

      <div
        class="tarjeta tarjeta--morado interactiva"
        role="button"
        tabindex="0"
        @click="irA('/pagos')"
        @keyup.enter="irA('/pagos')"
      >
        <div class="tarjeta-encabezado">
          <h3>Pagos <span class="flecha">➔</span></h3>
        </div>

        <SkeletonLista v-if="estado.pagos.cargando" :filas="3" />
        <p v-else-if="estado.pagos.error" class="error">No se pudo cargar la información de pagos.</p>
        <p v-else-if="pagos.length === 0" class="vacio">Aún no hay pagos registrados.</p>
        <ul v-else class="lista" @click.stop>
          <li v-for="pago in pagos" :key="pago.id">
            <div class="lista-item-cuerpo">
              <span>{{ pago.alumno_nombre }}</span>
              <span class="lista-item-detalle">{{ pago.clase_nombre }} · {{ pago.mes_cubierto }}</span>
            </div>
            <span class="etiqueta-mini etiqueta-mini--ok">{{ formatoMoneda.format(pago.monto) }}</span>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 1.5rem;
  background-color: #12121f;
  min-height: 100%;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
}

.encabezado h2 {
  color: #00c3e3;
  margin-bottom: 0.5rem;
}
.encabezado p {
  color: #a0a0b0;
  margin: 0;
}

/* --- KPIs --- */
.kpis {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
  margin-top: 2.5rem;
}

.kpi {
  background-color: #1a1a2e;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  border-top: 3px solid transparent;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 0;
}

.kpi--cian { border-top-color: #00c3e3; }
.kpi--morado { border-top-color: #8a2be2; }

.kpi-numero {
  font-size: clamp(1.5rem, 4vw, 2rem);
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
  overflow-wrap: anywhere;
}

.kpi-etiqueta {
  color: #a0a0b0;
  font-size: 0.85rem;
}

/* --- Tarjetas de detalle --- */
.tarjetas {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-top: 2rem;
}

.tarjeta {
  background-color: #1a1a2e;
  padding: 1.75rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  border-left: 5px solid transparent;
  min-width: 0;
}

.tarjeta--cian { border-left-color: #00c3e3; }
.tarjeta--morado { border-left-color: #8a2be2; }

/* Tarjetas clicables: toda la tarjeta navega, no solo el título */
.tarjeta.interactiva {
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-left-color 0.15s ease;
}
.tarjeta.interactiva:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
}
.tarjeta.interactiva:focus-visible {
  outline: 2px solid #ffffff;
  outline-offset: 2px;
}
.tarjeta--cian.interactiva:hover { border-left-color: #5fe3fa; }
.tarjeta--morado.interactiva:hover { border-left-color: #a86bf0; }

.tarjeta-encabezado {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.tarjeta-encabezado h3 {
  color: #ffffff;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.flecha {
  color: inherit;
  opacity: 0.6;
  font-size: 0.9em;
  transition: transform 0.15s ease, opacity 0.15s ease;
}
.tarjeta.interactiva:hover .flecha {
  opacity: 1;
  transform: translateX(3px);
}

.lista {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 240px;
  overflow-y: auto;
  cursor: default;
}

.lista li {
  background-color: #23233b;
  padding: 0.6rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 6px;
  font-size: 0.95rem;
  color: #f5f5fa;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.acento {
  font-weight: bold;
}
.acento--cian { color: #00c3e3; }
.acento--morado { color: #8a2be2; }

.lista-item-cuerpo {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  flex: 1;
  min-width: 0;
}

.lista-item-detalle {
  font-size: 0.78rem;
  color: #a0a0b0;
}

.etiqueta-mini {
  margin-left: auto;
  font-size: 0.75rem;
  color: #a0a0b0;
  background-color: #12121f;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
}

.etiqueta-mini--alerta { color: #ff6b6b; }
.etiqueta-mini--ok { color: #2ecc71; }

.error {
  color: #ff6b6b;
}
.vacio {
  color: #a0a0b0;
  font-style: italic;
}

@media (min-width: 640px) {
  .kpis { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .kpis { grid-template-columns: repeat(4, 1fr); }
}

@media (min-width: 900px) {
  .tarjetas { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>