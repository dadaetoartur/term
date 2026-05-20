<template>
  <NuxtLayout>
    <UCard class="flex flex-col items-center mt-32">
      <h1 class="text-center text-5xl mb-5">
        Ошибка
      </h1>
      <p class="text-center text-2xl mb-0">
        {{ props.error.statusCode }}
      </p>
      <p class="text-center text-xl mb-5">
        {{ props.error.statusMessage }}
      </p>
      <NuxtLink to="/">
        <UButton>
          Вернуться на домашнюю страницу
        </UButton>
      </NuxtLink>
    </UCard>
  </NuxtLayout>
</template>

<script setup lang="ts">
import type { NuxtError } from '#app';

const props = defineProps({
  error: {
    type: Object as () => NuxtError,
    default: () => new Error(),
  },
});
</script>
