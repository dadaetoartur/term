<template>
  <section
    id="facilities"
    class="xl:mb-32 md:mb-28 mb-16"
  >
    <h2 class="xl:text-5xl md:text-4xl text-3xl xl:mb-16 md:mb-14 mb-9">
      Возможности платформы
    </h2>

    <div class="flex flex-col xl:gap-10 gap-5">
      <UCard
        v-for="(item, index) in cardText"
        :key="index"
        class="shadow-sm rounded-2xl  dark:bg-neutral-900 dark:ring-neutral-700"
      >
        <div class="grid xl:grid-cols-5 grid-cols-1 items-center gap-5">
          <NuxtImg
            class="rounded-2xl xl:w-full md:w-2/3 w-full place-self-center xl:col-span-3"
            :src="item.screenshot"
            :alt="item.title"
            loading="lazy"
          />
          <div class="xl:col-span-2">
            <h4 class="xl:text-4xl md:text-3xl text-2xl xl:mb-6 md:mb-5 mb-3">
              {{ item.title }}
            </h4>
            <p class="md:text-xl text-lg text-gray-500 dark:text-gray-400">
              {{ item.description }}
            </p>
          </div>
        </div>
      </UCard>
    </div>
  </section>
</template>

<script setup lang="ts">
const cardText = [
  {
    screenshot: '/facility-1.png',
    title: 'Файловое хранилище',
    description: 'Специализированная система для централизованного хранения и управления документацией зданий, включая чертежи, спецификации и графики работ. Она обеспечивает организациям удобный доступ и систематизацию всех необходимых документов на всех этапах строительства и эксплуатации',
  },
  {
    screenshot: '/facility-2.png',
    title: 'Управление персоналом',
    description: 'Становится более эффективным благодаря внедрению современных цифровых технологий. Эти технологии позволяют не только управлять и мониторить работу персонала, но и вести цифровой журнал эксплуатации, который упрощает документирование всех процессов и взаимодействий',
  },
  {
    screenshot: '/facility-3.png',
    title: 'Аналитика',
    description: 'Ключевой элемент к управлению персоналом и оборудованием в зданиях, улучшая процессы для более высокой эффективности и меньших затрат. Руководители и инженеры применяют передовые инструменты для сбора критически важной информации, способствующей взвешенным управленческим решениям',
  },
  {
    screenshot: '/facility-4.png',
    title: 'Bim-просмоторщик',
    description: 'Специализированное программное обеспечение, предназначенное для визуализации и анализа архитектурных и инженерных моделей зданий в формате IFC. Этот формат является международным стандартом для обмена данными в индустрии строительства, который поддерживает открытость и совместимость данных BIM',
  },
];
</script>

<style scoped>
.card {
  box-shadow: 0 10px 60px 0 rgba(0, 0, 0, 0.1);
  background: var(--white-100);
}
</style>
