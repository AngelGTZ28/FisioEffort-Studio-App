<script setup>
import SkeletonBlock from './SkeletonBlock.vue'

defineProps({
  tarjetas: { type: Number, default: 3 },
  tipo: { type: String, default: 'clases' },
})
</script>

<template>
  <div class="skeleton-tarjetas" aria-hidden="true">
    <div
      v-for="tarjeta in tarjetas"
      :key="tarjeta"
      class="skeleton-tarjeta"
      :class="tipo === 'pagos' ? 'skeleton-tarjeta--pago' : 'skeleton-tarjeta--clase'"
    >
      <div class="skeleton-tarjeta__header">
        <SkeletonBlock ancho="45%" alto="1.05rem" />
        <SkeletonBlock ancho="5rem" alto="1.3rem" radio="999px" />
      </div>

      <template v-if="tipo === 'clases'">
        <div class="skeleton-tarjeta__linea">
          <SkeletonBlock ancho="35%" alto="0.8rem" />
        </div>
        <div class="skeleton-tarjeta__badges">
          <SkeletonBlock
            v-for="badge in 3"
            :key="badge"
            ancho="6rem"
            alto="1.45rem"
            radio="999px"
          />
        </div>
      </template>

      <template v-else>
        <div class="skeleton-tarjeta__lineas">
          <SkeletonBlock v-for="linea in 3" :key="linea" :ancho="linea === 3 ? '70%' : '90%'" alto="0.8rem" />
        </div>
        <div class="skeleton-tarjeta__footer">
          <SkeletonBlock ancho="40%" alto="0.7rem" />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.skeleton-tarjetas {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  cursor: default;
}

.skeleton-tarjeta {
  background-color: #23233b;
  padding: 1.5rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.skeleton-tarjeta--clase {
  border-left: 4px solid #00c3e3;
}

.skeleton-tarjeta--pago {
  border-left: 4px solid #2e8b57;
}

.skeleton-tarjeta__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
}

.skeleton-tarjeta__badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  border-top: 1px solid #33334d;
  padding-top: 1rem;
}

.skeleton-tarjeta__lineas {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.skeleton-tarjeta__footer {
  margin-top: auto;
  border-top: 1px solid #33334d;
  padding-top: 0.5rem;
  display: flex;
  justify-content: flex-end;
}
</style>