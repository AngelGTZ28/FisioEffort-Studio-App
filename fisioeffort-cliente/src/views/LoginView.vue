<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../supabase'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const cargando = ref(false)

const iniciarSesion = async () => {
  cargando.value = true
  errorMsg.value = ''

  try {
    // Le pedimos a Supabase que nos loguee
    const { data, error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value
    })

    if (error) throw error

    // Supabase maneja los tokens y el localStorage por ti automáticamente.
    // Así que si no hubo error, directo pa' adentro.
    router.push('/')
  } catch (error) {
    console.error('Error de Supabase:', error.message)
    errorMsg.value = 'Credenciales incorrectas o usuario no registrado.'
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Fisio<span class="cian">Effort</span> <span class="morado">Studio</span></h1>
        <p>Ingresa tus credenciales para acceder</p>
      </div>

      <form @submit.prevent="iniciarSesion" class="formulario">
        <div class="input-group">
          <label>Correo Electrónico</label>
          <input type="email" v-model="email" required placeholder="tu@correo.com" autocomplete="username">
        </div>

        <div class="input-group">
          <label>Contraseña</label>
          <input type="password" v-model="password" required placeholder="••••••••" autocomplete="current-password">
        </div>

        <p v-if="errorMsg" class="mensaje-error">{{ errorMsg }}</p>

        <button type="submit" class="btn-login" :disabled="cargando">
          {{ cargando ? 'Verificando...' : 'Entrar al Sistema' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Pantalla completa para centrar la tarjeta */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #12121a;
  padding: 1rem;
  /* Posicionamiento absoluto para sobreponerse al App.vue si es necesario */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.login-card {
  background-color: #1a1a2e;
  padding: 3rem 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  width: 100%;
  max-width: 420px;
  border-top: 4px solid #00c3e3;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 2rem;
  color: white;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #a0a0b0;
  font-size: 0.95rem;
}

.cian { color: #00c3e3; }
.morado { color: #8a2be2; }

.formulario {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #a0a0b0;
  font-size: 0.9rem;
}

input {
  background-color: #23233b;
  border: 1px solid #33334d;
  color: white;
  padding: 1rem;
  border-radius: 6px;
  outline: none;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #00c3e3;
}

.mensaje-error {
  color: #ff4d4d;
  font-size: 0.85rem;
  text-align: center;
  background-color: rgba(255, 77, 77, 0.1);
  padding: 0.5rem;
  border-radius: 6px;
}

.btn-login {
  background-color: #8a2be2;
  color: white;
  border: none;
  padding: 1rem;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
  margin-top: 0.5rem;
}

.btn-login:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-login:active:not(:disabled) {
  transform: scale(0.98);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>