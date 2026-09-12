<script setup>
defineProps({
  ancho: { type: String, default: '100%' },
  alto: { type: String, default: '1rem' },
  radio: { type: String, default: '6px' },
  itemClass: { type: String, default: '' },
})
</script>

<template>
  <div class="skeleton-block" :class="itemClass" :style="{ width: ancho, height: alto, borderRadius: radio }"></div>
</template>

<style scoped>
.skeleton-block {
  position: relative;
  overflow: hidden;
  background-color: #23233b;
  flex-shrink: 0;
}

.skeleton-block::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.07) 50%,
    transparent 100%
  );
  animation: shimmer 1.6s infinite;
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-block::after {
    animation: none;
  }
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}
</style>