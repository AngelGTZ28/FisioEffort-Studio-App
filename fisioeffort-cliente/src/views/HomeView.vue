<script setup>
import { ref, onMounted } from 'vue'

// Aquí guardaremos los datos que lleguen de Django
const alumnos = ref([])
const cargando = ref(true)

// Esta función se ejecuta automáticamente cuando la pantalla carga
onMounted(async () => {
  try {
    // Asegúrate de que esta URL coincida con la ruta de tu API en Django
    const respuesta = await fetch('http://127.0.0.1:8000/api/alumnos/')
    const datos = await respuesta.json()

    console.log('Lo que mandó Django:', datos)

    alumnos.value = datos
    cargando.value = false
  } catch (error) {
    console.error('Error al conectar con la API:', error)
    cargando.value = false
  }
})
</script>

<template>
  <div class="dashboard">
    <h2>Panel Principal</h2>
    <p>Bienvenido al sistema de control de FisioEffort Studio.</p>
    
    <div class="tarjetas">
      <div class="tarjeta">
        <h3>Alumnos Registrados</h3>
        <!-- Mientras carga -->
        <p v-if="cargando" class="cargando">Conectando con la base de datos...</p>
        
        <!-- Cuando ya hay datos -->
        <ul v-else class="lista-alumnos">
          <li v-for="alumno in alumnos" :key="alumno.id">
            <span class="cian">#{{ alumno.id }}</span> - {{ alumno.nombre_completo }} 
          </li>
        </ul>
      </div>

      <div class="tarjeta">
        <h3>Pagos</h3>
        <p>Control de colegiaturas</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Conservamos los estilos que ya teníamos */
.dashboard { padding: 1rem; }
h2 { color: #00c3e3; margin-bottom: 0.5rem; }
p { color: #a0a0b0; }

.tarjetas {
  display: flex;
  gap: 2rem;
  margin-top: 3rem;
}

.tarjeta {
  background-color: #1a1a2e;
  padding: 2rem;
  border-radius: 12px;
  border-left: 5px solid #8a2be2;
  width: 350px; /* La hicimos un poco más ancha para que quepan los nombres */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.tarjeta h3 {
  color: #ffffff;
  margin-bottom: 1rem;
}

/* Nuevos estilos para la lista de datos */
.lista-alumnos {
  list-style: none;
  padding: 0;
}

.lista-alumnos li {
  background-color: #23233b;
  padding: 0.5rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 6px;
  font-size: 0.95rem;
}

.cargando {
  color: #8a2be2;
  font-style: italic;
}
.cian {
  color: #00c3e3;
  font-weight: bold;
}
</style>