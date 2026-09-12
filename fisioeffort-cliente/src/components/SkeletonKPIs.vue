<script setup>
import SkeletonBlock from './SkeletonBlock.vue'

defineProps({
  cantidad: { type: Number, default: 4 },
})
</script>

<template>
  <div class="skeleton-kpis" aria-hidden="true">
    <div v-for="kpi in cantidad" :key="kpi" class="skeleton-kpis__tarjeta">
      <SkeletonBlock ancho="55%" alto="2rem" />
      <SkeletonBlock ancho="80%" alto="0.85rem" />
    </div>
  </div>
</template>

<style scoped>
.skeleton-kpis {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  margin-top: 2.5rem;
  cursor: default;
}

.skeleton-kpis__tarjeta {
  background-color: #1a1a2e;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  border-top: 3px solid transparent;
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

@media (max-width: 900px) {
  .skeleton-kpis {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>