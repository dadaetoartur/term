<template>
  <UCard class="mb-3">
    <div class="flex justify-between items-center mb-10">
      <h2 class="text-2xl">
        Качество выполнения
      </h2>
      <USelectMenu
        v-model="current"
        :options="dateRange"
      >
        <template #label>
          <span
            v-if="current.length"
            class="truncate"
          >За последние {{ current }}</span>
        </template>
      </USelectMenu>
    </div>

    <div class="flex gap-10">
      <div class="flex flex-col items-start gap-3">
        <p>Повторные отказы</p>
        <UBadge
          variant="soft"
          class="text-4xl px-5 py-2"
        >
          18%
        </UBadge>
      </div>

      <UDivider orientation="vertical" />

      <div class="flex flex-col items-start gap-3">
        <p>Дельта</p>
        <UBadge
          variant="soft"
          class="text-4xl px-5 py-2"
        >
          62%
        </UBadge>
      </div>

      <UDivider orientation="vertical" />

      <div class="flex flex-col items-start gap-3">
        <p>В работе</p>
        <UBadge
          variant="soft"
          class="text-4xl px-5 py-2"
        >
          1
        </UBadge>
      </div>
    </div>
  </UCard>
</template>

<script setup lang="ts">
const dateRange = ref(['7 дней', '2 недели', '1 месяц']);

const current = ref(dateRange.value[0]);
</script>

<style scoped></style>
