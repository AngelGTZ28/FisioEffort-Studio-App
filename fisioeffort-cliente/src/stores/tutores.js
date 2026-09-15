import { defineStore } from 'pinia'
import { apiFetch } from '../api'

let fetchPromise = null

export const useTutoresStore = defineStore('tutores', {
  state: () => ({
    tutores: [],
    cargando: false,
    yaCargado: false,
  }),
  actions: {
    async fetchTutores(forzar = false) {
      if (this.yaCargado && !forzar) return
      if (fetchPromise && !forzar) return fetchPromise

      this.cargando = true
      fetchPromise = (async () => {
        try {
          const respuesta = await apiFetch('/tutores/')
          this.tutores = await respuesta.json()
          this.yaCargado = true
        } catch (error) {
          console.error('Error al cargar tutores:', error)
        } finally {
          this.cargando = false
          fetchPromise = null
        }
      })()

      return fetchPromise
    },
    agregarTutorLocal(nuevoTutor) {
      this.tutores.push(nuevoTutor)
    }
  }
})
