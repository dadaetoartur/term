<template>
  <section
    id="quickstart"
    class="flex flex-col xl:mb-32 md:mb-28 mb-16"
  >
    <h2 class="xl:text-5xl md:text-4xl text-3xl xl:mb-16 md:mb-14 mb-9">
      Быстрый старт
    </h2>

    <ClientOnly>
      <img
        :class="{ whiteFilter: isDark }"
        class="mb-10 xl:block hidden"
        src="~/assets/images/quick-start-desktop.svg"
        alt="quick-start-desktop"
        loading="lazy"
      >
      <img
        :class="{ whiteFilter: isDark }"
        class="mb-10 md:block xl:hidden hidden"
        src="~/assets/images/quick-start-tablet.svg"
        alt="quick-start-tablet"
        loading="lazy"
      >
      <img
        :class="{ whiteFilter: isDark }"
        class="mb-10 md:hidden block"
        src="~/assets/images/quick-start-mobile.svg"
        alt="quick-start-mobile"
        loading="lazy"
      >
    </ClientOnly>

    <div class="grid xl:grid-cols-2 grid-cols-1 gap-5 items-center">
      <div class="flex flex-col xl:order-none order-1">
        <h3 class="xl:text-4xl md:text-3xl text-2xl xl:mb-6 mb-3">
          Принцип работы:
        </h3>
        <ol class="list-decimal flex flex-col xl:gap-8 md:gap-5 gap-3 ml-5">
          <li
            v-for="(item, index) of list"
            :key="index"
            class="md:text-xl text-lg"
          >
            <p>
              {{ item.text }}
            </p>
          </li>
        </ol>
      </div>

      <NuxtImg
        class="place-self-center"
        src="/principes.png"
        loading="lazy"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
const colorMode = useColorMode();
const isDark = computed(() => colorMode.value === 'dark');

const list = [
  {
    text: 'Загрузка посчитенной записи в формате XML — начальный этап, на котором загружаются исходные данные, необходимые для работы системы',
  },
  {
    text: 'Загрузка BIM моделей — следующий шаг включает в себя импорт моделей зданий, что позволяет системе анализировать и визуализировать структурные аспекты',
  },
  {
    text: 'Добавление сотрудников — на этом этапе в систему добавляются пользователи или сотрудники, которые будут работать с данными и моделями',
  },
  {
    text: 'Старт — финальный этап, запускающий процессы или проекты после успешной подготовки и настройки системы',
  },
];
</script>

<style scoped>
.whiteFilter {
  filter: brightness(0) saturate(100%) invert(93%) sepia(93%) saturate(0%) hue-rotate(207deg) brightness(108%) contrast(107%);
}
</style>
