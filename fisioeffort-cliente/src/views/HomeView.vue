<script setup>
import { ref, onMounted, computed } from 'vue'

const API_BASE = 'http://127.0.0.1:8000/api'

// Estado por sección: datos, carga y error, todo por separado
// para que una sección lenta o caída no bloquee a las demás.
const alumnos = ref([])
const tutores = ref([])
const clases = ref([])
const pagos = ref([])

const estado = ref({
  alumnos: { cargando: true, error: false },
  tutores: { cargando: true, error: false },
  clases: { cargando: true, error: false },
  pagos: { cargando: true, error: false },
})

async function cargarSeccion(nombre, url, destino) {
  try {
    const respuesta = await fetch(url)
    if (!respuesta.ok) throw new Error(`HTTP ${respuesta.status}`)
    const datos = await respuesta.json()
    destino.value = datos
  } catch (error) {
    console.error(`Error al cargar ${nombre}:`, error)
    estado.value[nombre].error = true
  } finally {
    estado.value[nombre].cargando = false
  }
}

onMounted(() => {
  cargarSeccion('alumnos', `${API_BASE}/alumnos/`, alumnos)
  cargarSeccion('tutores', `${API_BASE}/tutores/`, tutores)
  cargarSeccion('clases', `${API_BASE}/clases/`, clases)
  cargarSeccion('pagos', `${API_BASE}/pagos/`, pagos)
})

const formatoMoneda = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
})

// KPIs derivados de los campos reales de tus serializers.
const totalAlumnos = computed(() => alumnos.value.length)
const alumnosActivos = computed(() => alumnos.value.filter((a) => a.activo).length)
const totalTutores = computed(() => tutores.value.length)
const totalClases = computed(() => clases.value.length)
const cuposDisponibles = computed(() =>
  clases.value.reduce((suma, c) => suma + (c.lugares_disponibles ?? 0), 0)
)
const totalRecaudado = computed(() =>
  pagos.value.reduce((suma, p) => suma + Number(p.monto || 0), 0)
)
</script>

<template>
  <div class="dashboard">
    <header class="encabezado">
      <h2>Panel Principal</h2>
      <p>Bienvenido al sistema de control de FisioEffort Studio.</p>
    </header>

    <!-- Fila de KPIs: el vistazo rápido antes de entrar al detalle -->
    <section class="kpis">
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
        <span class="kpi-etiqueta">Total recaudado</span>
      </div>
    </section>

    <!-- Detalle por área -->
    <section class="tarjetas">
      <div class="tarjeta tarjeta--cian">
        <div class="tarjeta-encabezado">
          <h3>Alumnos</h3>
          <span class="contador">{{ totalAlumnos }}</span>
        </div>

        <p v-if="estado.alumnos.cargando" class="cargando">Conectando con la base de datos...</p>
        <p v-else-if="estado.alumnos.error" class="error">No se pudo cargar la información de alumnos.</p>
        <p v-else-if="alumnos.length === 0" class="vacio">Aún no hay alumnos registrados.</p>
        <ul v-else class="lista">
          <li v-for="alumno in alumnos" :key="alumno.id">
            <span class="acento acento--cian">#{{ alumno.id }}</span>
            <div class="lista-item-cuerpo">
              <span>{{ alumno.nombre_completo }}</span>
              <span class="lista-item-detalle">
                {{ alumno.nombre_tutor || 'Sin tutor asignado' }}
                <template v-if="alumno.clases_inscritas?.length">
                  · {{ alumno.clases_inscritas.join(', ') }}
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

      <div class="tarjeta tarjeta--morado">
        <div class="tarjeta-encabezado">
          <h3>Tutores</h3>
          <span class="contador">{{ totalTutores }}</span>
        </div>

        <p v-if="estado.tutores.cargando" class="cargando">Conectando con la base de datos...</p>
        <p v-else-if="estado.tutores.error" class="error">No se pudo cargar la información de tutores.</p>
        <p v-else-if="tutores.length === 0" class="vacio">Aún no hay tutores registrados.</p>
        <ul v-else class="lista">
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

      <div class="tarjeta tarjeta--cian">
        <div class="tarjeta-encabezado">
          <h3>Clases</h3>
          <span class="contador">{{ totalClases }}</span>
        </div>

        <p v-if="estado.clases.cargando" class="cargando">Conectando con la base de datos...</p>
        <p v-else-if="estado.clases.error" class="error">No se pudo cargar la información de clases.</p>
        <p v-else-if="clases.length === 0" class="vacio">Aún no hay clases registradas.</p>
        <ul v-else class="lista">
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

      <div class="tarjeta tarjeta--morado">
        <div class="tarjeta-encabezado">
          <h3>Pagos</h3>
          <span class="contador">{{ formatoMoneda.format(totalRecaudado) }}</span>
        </div>

        <p v-if="estado.pagos.cargando" class="cargando">Conectando con la base de datos...</p>
        <p v-else-if="estado.pagos.error" class="error">No se pudo cargar la información de pagos.</p>
        <p v-else-if="pagos.length === 0" class="vacio">Aún no hay pagos registrados.</p>
        <ul v-else class="lista">
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
  grid-template-columns: repeat(4, 1fr);
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
}

.kpi--cian { border-top-color: #00c3e3; }
.kpi--morado { border-top-color: #8a2be2; }

.kpi-numero {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
}

.kpi-etiqueta {
  color: #a0a0b0;
  font-size: 0.85rem;
}

/* --- Tarjetas de detalle --- */
.tarjetas {
  display: grid;
  grid-template-columns: repeat(2, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.tarjeta {
  background-color: #1a1a2e;
  padding: 1.75rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  border-left: 5px solid transparent;
}

.tarjeta--cian { border-left-color: #00c3e3; }
.tarjeta--morado { border-left-color: #8a2be2; }

.tarjeta-encabezado {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.tarjeta-encabezado h3 {
  color: #ffffff;
  margin: 0;
}

.contador {
  color: #a0a0b0;
  font-size: 0.85rem;
}

.lista {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 240px;
  overflow-y: auto;
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

.cargando {
  color: #8a2be2;
  font-style: italic;
}
.error {
  color: #ff6b6b;
}
.vacio {
  color: #a0a0b0;
  font-style: italic;
}

@media (max-width: 900px) {
  .kpis { grid-template-columns: repeat(2, 1fr); }
  .tarjetas { grid-template-columns: 1fr; }
}
</style>