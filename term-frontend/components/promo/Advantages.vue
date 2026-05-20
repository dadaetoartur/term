<template>
  <section
    id="advantages"
    class="xl:mb-32 md:mb-28 mb-16"
  >
    <h2 class="xl:text-5xl md:text-4xl text-3xl xl:mb-16 md:mb-14 mb-9">
      Ключевые приемущества
    </h2>

    <div class="grid xl:grid-cols-4 md:grid-cols-2 grid-cols-1 md:gap-5 gap-3">
      <div
        v-for="(item, index) in cardText"
        :key="index"
        class="border border-black dark:border-neutral-500 rounded-2xl px-3 md:py-20 py-10 flex flex-col gap-6"
      >
        <div class="flex items-center gap-4">
          <p class="md:text-6xl text-5xl">
            {{ item.value }}
          </p>
          <span class="text-lg w-1/2">{{ item.valueText }}</span>
        </div>
        <p class="text-lg text-gray-500 dark:text-gray-400">
          {{ item.description }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const cardText = [
  {
    value: '45%',
    valueText: 'сокращение ошибок',
    description: 'Точное моделирование в BIM уменьшает ошибки в проектировании и строительстве',
  },
  {
    value: '50%',
    valueText: 'сокращение времени',
    description: 'Ускорение реагирования на аварии благодаря цифровым двойникам в сравнении с традиционными системами',
  },
  {
    value: '50%',
    valueText: 'увеличение срока зданий',
    description: 'Продление срока службы зданий благодаря предиктивному анализу и цифровым двойникам',
  },
  {
    value: '90%',
    valueText: 'сокращение времени',
    description: 'Быстрый доступ к информации по сравнению с бумажными архивами',
  },
];
</script>

<style scoped></style>
