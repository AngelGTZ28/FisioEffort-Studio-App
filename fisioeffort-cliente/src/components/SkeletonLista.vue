<script setup>
import SkeletonBlock from './SkeletonBlock.vue'

defineProps({
  filas: { type: Number, default: 4 },
})
</script>

<template>
  <div class="skeleton-lista" aria-hidden="true">
    <div v-for="fila in filas" :key="fila" class="skeleton-lista__fila">
      <SkeletonBlock ancho="2.1rem" alto="2.1rem" radio="50%" />
      <div class="skeleton-lista__cuerpo">
        <SkeletonBlock ancho="55%" alto="0.9rem" />
        <SkeletonBlock ancho="85%" alto="0.7rem" />
      </div>
      <SkeletonBlock ancho="4.6rem" alto="1.2rem" radio="999px" itemClass="skeleton-lista__etiqueta" />
    </div>
  </div>
</template>

<style scoped>
.skeleton-lista {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  cursor: default;
}

.skeleton-lista__fila {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background-color: #23233b;
  padding: 1rem;
  border-radius: 6px;
}

.skeleton-lista__cuerpo {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 0;
}

.skeleton-lista__etiqueta {
  margin-left: auto;
}
</style>