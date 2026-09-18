import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const isOpen = ref(false)
  const tipo = ref('alert') // 'alert' | 'confirm'
  const titulo = ref('')
  const mensaje = ref('')
  const resolvePromise = ref(null)

  function mostrarAlerta(mensajeTexto, tituloTexto = 'Aviso') {
    return new Promise((resolve) => {
      isOpen.value = true
      tipo.value = 'alert'
      titulo.value = tituloTexto
      mensaje.value = mensajeTexto
      resolvePromise.value = resolve
    })
  }

  function mostrarConfirmacion(mensajeTexto, tituloTexto = 'Confirmación') {
    return new Promise((resolve) => {
      isOpen.value = true
      tipo.value = 'confirm'
      titulo.value = tituloTexto
      mensaje.value = mensajeTexto
      resolvePromise.value = resolve
    })
  }

  function aceptar() {
    if (resolvePromise.value) {
      resolvePromise.value(true)
    }
    cerrar()
  }

  function cancelar() {
    if (resolvePromise.value) {
      resolvePromise.value(false)
    }
    cerrar()
  }

  function cerrar() {
    isOpen.value = false
    // Esperamos a que la transición CSS termine antes de limpiar los textos
    setTimeout(() => {
      tipo.value = 'alert'
      titulo.value = ''
      mensaje.value = ''
      resolvePromise.value = null
    }, 300)
  }

  return {
    isOpen,
    tipo,
    titulo,
    mensaje,
    mostrarAlerta,
    mostrarConfirmacion,
    aceptar,
    cancelar
  }
})
