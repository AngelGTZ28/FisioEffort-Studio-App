<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useUiStore } from '../stores/ui'

const uiStore = useUiStore()

// Permitir cerrar con la tecla Escape
const handleKeydown = (e) => {
  if (e.key === 'Escape' && uiStore.isOpen) {
    uiStore.cancelar() // Esc cuenta como cancelar
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <Transition name="dialog-fade">
    <div v-if="uiStore.isOpen" class="dialog-overlay" @click.self="uiStore.cancelar">
      <div class="dialog-card" role="dialog" aria-modal="true" :aria-labelledby="uiStore.titulo ? 'dialog-title' : undefined">
        
        <!-- Icono Decorativo -->
        <div class="dialog-icon" :class="uiStore.tipo">
          <svg v-if="uiStore.tipo === 'alert'" viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <svg v-else viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10" />
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
        </div>

        <div class="dialog-content">
          <h3 id="dialog-title">{{ uiStore.titulo }}</h3>
          <p>{{ uiStore.mensaje }}</p>
        </div>

        <div class="dialog-actions">
          <button 
            v-if="uiStore.tipo === 'confirm'" 
            class="btn-cancelar" 
            @click="uiStore.cancelar"
          >
            Cancelar
          </button>
          <button 
            class="btn-aceptar" 
            @click="uiStore.aceptar"
          >
            Aceptar
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* --- OVERLAY CON BLUR --- */
.dialog-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background-color: rgba(11, 14, 23, 0.75); /* #0b0e17 con transparencia */
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

/* --- TARJETA PRINCIPAL --- */
.dialog-card {
  background-color: #0f1422;
  border: 1px solid rgba(0, 242, 254, 0.15); /* Borde sutil cian */
  border-radius: 16px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 20px -5px rgba(0, 242, 254, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

/* --- ICONO SUPERIOR --- */
.dialog-icon {
  padding: 1.5rem 1.5rem 0;
  display: flex;
  justify-content: center;
}

.dialog-icon.alert {
  color: #00f2fe; /* Acento Cian */
}

.dialog-icon.confirm {
  color: #fe00ea; /* Acento Fucsia */
}

/* --- CONTENIDO DE TEXTO --- */
.dialog-content {
  padding: 1.5rem;
  text-align: center;
}

.dialog-content h3 {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.dialog-content p {
  color: #cbd5e1;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
  white-space: pre-line;
  word-break: break-word;
}

/* --- ACCIONES (BOTONES) --- */
.dialog-actions {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  padding: 0 1.5rem 1.75rem;
}

button {
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 8px;
  padding: 0.65rem 1.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

/* Botón Secundario (Cancelar) */
.btn-cancelar {
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #94a3b8;
}

.btn-cancelar:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.3);
}

/* Botón Primario (Aceptar) */
.btn-aceptar {
  background: linear-gradient(135deg, #00f2fe 0%, #00b5cc 100%);
  border: none;
  color: #0b0e17; /* Texto oscuro para contraste */
  box-shadow: 0 4px 15px rgba(0, 242, 254, 0.25);
  min-width: 120px;
}

.btn-aceptar:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4);
  background: linear-gradient(135deg, #33f5fe 0%, #00c7e0 100%);
}

/* --- RESPONSIVE MÓVIL --- */
@media (max-width: 480px) {
  .dialog-actions {
    flex-direction: column-reverse; /* Invertir para dejar aceptar arriba o por flujo natural */
  }
  button {
    width: 100%;
    padding: 0.85rem 1.25rem; /* Área táctil de mayor tamaño */
  }
}

/* --- ANIMACIONES VUE TRANSITION --- */
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.3s ease;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}

/* Escalar y deslizar ligeramente la tarjeta */
.dialog-fade-enter-active .dialog-card,
.dialog-fade-leave-active .dialog-card {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
}

.dialog-fade-enter-from .dialog-card,
.dialog-fade-leave-to .dialog-card {
  opacity: 0;
  transform: scale(0.95) translateY(15px);
}
</style>
