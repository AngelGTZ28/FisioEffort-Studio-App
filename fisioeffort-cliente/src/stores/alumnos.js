import { defineStore } from 'pinia'
import { apiFetch } from '../api'

let fetchPromise = null

export const useAlumnosStore = defineStore('alumnos', {
  state: () => ({
    alumnos: [],
    cargando: false,
    yaCargado: false,
  }),
  actions: {
    async fetchAlumnos(forzar = false) {
      if (this.yaCargado && !forzar) return
      if (fetchPromise && !forzar) return fetchPromise

      this.cargando = true
      fetchPromise = (async () => {
        try {
          const respuesta = await apiFetch('/alumnos/')
          this.alumnos = await respuesta.json()
          this.yaCargado = true
        } catch (error) {
          console.error('Error al cargar alumnos:', error)
        } finally {
          this.cargando = false
          fetchPromise = null
        }
      })()

      return fetchPromise
    },
    
    agregarAlumnoLocal(nuevoAlumno) {
      this.alumnos.push(nuevoAlumno)
    },
    
    cambiarEstadoLocal(alumnoId, nuevoEstado) {
      const index = this.alumnos.findIndex(a => a.id === alumnoId)
      if (index !== -1) {
        this.alumnos[index].activo = nuevoEstado
      }
    }
  },
  getters: {
    alumnosActivos: (state) => state.alumnos.filter(a => a.activo === true),
    alumnosInactivos: (state) => state.alumnos.filter(a => a.activo === false),
  }
})
