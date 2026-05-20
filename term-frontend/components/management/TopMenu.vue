<template>
  <div class="w-full flex justify-between mb-3 gap-3">
    <div class="flex items-stretch gap-3">
      <NuxtLink to="/management/objects/create?step=0">
        <UButton
          variant="soft"
          color="primary"
          icon="i-heroicons-plus"
        />
      </NuxtLink>

      <GroupObjectsSwitcher />

      <ObjectsSwitcher />

      <AdministrationSwitcher />
    </div>

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

      <UChip :show="notifications > 0">
        <UTooltip text="Уведомления">
          <UButton
            icon="i-heroicons-inbox"
            color="gray"
            @click="isOpenNotification = true"
          />
        </UTooltip>
      </UChip>

      <USlideover v-model="isOpenNotification">
        <UCard
          class="flex flex-col flex-1"
          :ui="{ body: { base: 'flex-1' }, ring: '', divide: 'divide-y divide-gray-100 dark:divide-gray-800' }"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold leading-6 text-gray-900 dark:text-white">
                Уведомления
              </h3>
              <UButton
                color="gray"
                variant="ghost"
                icon="i-heroicons-x-mark-20-solid"
                class="-my-1"
                @click="isOpenNotification = false"
              />
            </div>
          </template>

          <p class="text-base">
            Нет новых уведмолений
          </p>
        </UCard>
      </USlideover>
    </div>
  </div>
</template>

<script setup lang="ts">
import ObjectsSwitcher from './ObjectsSwitcher.vue';
import AdministrationSwitcher from './AdministrationSwitcher.vue';
import GroupObjectsSwitcher from './GroupObjectsSwitcher.vue';

const notifications = ref(0);
const isOpenNotification = ref(false);

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
