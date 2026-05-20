<template>
  <div class="loading">
    <p class="text-xl">
      Загрузка...
    </p>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.loading {
  position: absolute;
  z-index: 1;
  top: 45%;
  left: 45%;
  background-color: rgb(var(--color-primary-400));
  padding: 1rem 2rem;
  border-radius: 0.5rem;
}
</style>
