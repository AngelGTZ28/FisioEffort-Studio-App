<script setup>
import { ref, onMounted } from 'vue'

const pagos = ref([])
const inscripciones = ref([])
const cargando = ref(true)

const nuevoPago = ref({
  inscripcion: '',
  monto: '',
  mes_cubierto: '',
  metodo_pago: 'EFECTIVO'
})

const formatoMoneda = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
})

// Cargar el historial de pagos
const cargarPagos = async () => {
  try {
    const respuesta = await fetch('http://127.0.0.1:8000/api/pagos/')
    pagos.value = await respuesta.json()
    cargando.value = false
  } catch (error) {
    console.error('Error al cargar pagos:', error)
  }
}

// Cargar las inscripciones para el select del formulario
const cargarInscripciones = async () => {
  try {
    const respuesta = await fetch('http://127.0.0.1:8000/api/inscripciones/')
    if (respuesta.ok) {
      inscripciones.value = await respuesta.json()
    }
  } catch (error) {
    console.error('Error al cargar inscripciones:', error)
  }
}

const registrarPago = async () => {
  try {
    const respuesta = await fetch('http://127.0.0.1:8000/api/pagos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(nuevoPago.value)
    })

    if (respuesta.ok) {
      // Limpiamos el formulario y recargamos la lista
      nuevoPago.value = { inscripcion: '', monto: '', mes_cubierto: '', metodo_pago: 'EFECTIVO' }
      cargarPagos()
      alert('¡Pago registrado con éxito!')
    }
  } catch (error) {
    console.error('Error al registrar pago:', error)
  }
}

onMounted(() => {
  cargarPagos()
  cargarInscripciones()
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

          <div class="input-group">
            <label>Alumno y Clase (Inscripción)</label>
            <select v-model="nuevoPago.inscripcion" required>
              <option value="" disabled>Selecciona una inscripción...</option>
              <!-- Iteramos sobre las inscripciones activas -->
              <option v-for="insc in inscripciones" :key="insc.id" :value="insc.id">
                Inscripción #{{ insc.id }}
              </option>
            </select>
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

          <button type="submit" class="btn-guardar">Registrar Ingreso</button>
        </form>
      </div>

      <!-- Columna Derecha: Historial de Pagos -->
      <div class="panel">
        <h3>Historial Reciente</h3>
        <p v-if="cargando" class="cargando">Cargando la bóveda...</p>

        <div v-else class="lista-pagos">
          <div v-if="pagos.length === 0" class="sin-datos">
            Aún no hay pagos registrados.
          </div>

          <div v-for="pago in pagos" :key="pago.id" class="tarjeta-pago">
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
.input-group { display: flex; flex-direction: column; gap: 0.5rem; }
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

.cargando {
  color: #8a2be2;
  font-style: italic;
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