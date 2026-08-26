<template>
  <div class="dashboard">
    <h2>Panel Principal</h2>
    <p>Bienvenido al sistema de control de FisioEffort Studio.</p>
    
    <div class="tarjetas">
      <div class="tarjeta">
        <h3>Alumnos</h3>
        <p>Gestiona expedientes e inscripciones</p>
      </div>
      <div class="tarjeta">
        <h3>Pagos</h3>
        <p>Control de colegiaturas</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 1rem;
}

h2 {
  color: #00c3e3; /* Cian */
  margin-bottom: 0.5rem;
}

p {
  color: #a0a0b0; /* Gris claro para texto secundario */
}

.tarjetas {
  display: flex;
  gap: 2rem;
  margin-top: 3rem;
}

.tarjeta {
  background-color: #1a1a2e; /* Fondo de tarjeta un poco más claro que el principal */
  padding: 2rem;
  border-radius: 12px;
  border-left: 5px solid #8a2be2; /* Borde morado de acento */
  width: 300px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
  cursor: pointer;
}

.tarjeta:hover {
  transform: translateY(-5px); /* Efecto de saltito al pasar el mouse */
}

.tarjeta h3 {
  color: #ffffff;
  margin-bottom: 0.5rem;
}
</style>