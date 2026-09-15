import { defineStore } from 'pinia'
import { apiFetch } from '../api'

let fetchPromise = null

export const usePagosStore = defineStore('pagos', {
  state: () => ({
    pagos: [],
    cargando: false,
    yaCargado: false,
  }),
  actions: {
    async fetchPagos(forzar = false) {
      if (this.yaCargado && !forzar) return
      if (fetchPromise && !forzar) return fetchPromise

      this.cargando = true
      fetchPromise = (async () => {
        try {
          const respuesta = await apiFetch('/pagos/')
          this.pagos = await respuesta.json()
          this.yaCargado = true
        } catch (error) {
          console.error('Error al cargar pagos:', error)
        } finally {
          this.cargando = false
          fetchPromise = null
        }
      })()

      return fetchPromise
    },
    agregarPagoLocal(nuevoPago) {
      // Como los pagos suelen ordenarse por los más recientes primero, lo ponemos al inicio
      this.pagos.unshift(nuevoPago)
    }
  }
})
