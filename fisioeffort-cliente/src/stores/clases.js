import { defineStore } from 'pinia'
import { apiFetch } from '../api'

let fetchPromise = null

export const useClasesStore = defineStore('clases', {
  state: () => ({
    clases: [],
    cargando: false,
    yaCargado: false,
  }),
  actions: {
    async fetchClases(forzar = false) {
      if (this.yaCargado && !forzar) return
      if (fetchPromise && !forzar) return fetchPromise

      this.cargando = true
      fetchPromise = (async () => {
        try {
          const respuesta = await apiFetch('/clases/')
          this.clases = await respuesta.json()
          this.yaCargado = true
        } catch (error) {
          console.error('Error al cargar clases:', error)
        } finally {
          this.cargando = false
          fetchPromise = null
        }
      })()

      return fetchPromise
    }
  }
})
