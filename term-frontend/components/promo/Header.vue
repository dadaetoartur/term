<template>
  <header class="mb-8 py-2 fixed top-0 left-0 right-0 bg-white dark:bg-neutral-900 z-50">
    <UContainer class="flex gap-3 justify-between items-center">
      <BimifyLogo />

      <div class="flex gap-3">
        <ClientOnly>
          <UTooltip text="Переключение темы">
            <UButton
              :icon="isDark ? 'i-heroicons-moon-20-solid' : 'i-heroicons-sun-20-solid'"
              color="gray"
              variant="ghost"
              aria-label="Theme"
              @click="isDark = !isDark"
            />
            <template #fallback>
              <div class="w-8 h-8" />
            </template>
          </UTooltip>
        </ClientOnly>

        <NuxtLink to="/login">
          <UButton
            color="primary"
            class="flex items-center gap-1"
          >
            <UIcon
              class="text-lg"
              dynamic
              name="i-heroicons-user"
            />
            <p class="text-lg">
              Войти
            </p>
          </UButton>
        </NuxtLink>
      </div>
    </UContainer>
  </header>
</template>

<script setup lang="ts">
import BimifyLogo from './BimifyLogo.vue';

const colorMode = useColorMode();
const isDark = computed({
  get() {
    return colorMode.value === 'dark';
  },
  set() {
    colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
  },
});
</script>

<style scoped></style>
