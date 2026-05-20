<template>
  <section
    id="projects"
    class="xl:mb-32 md:mb-28 mb-16"
  >
    <h2 class="xl:text-5xl md:text-4xl text-3xl xl:mb-16 md:mb-14 mb-9">
      Наши проекты
    </h2>

    <div class="grid md:grid-cols-2 grid-cols-1 gap-5">
      <NuxtImg
        class="w-full rounded-2xl"
        src="/project.png"
        alt="project mdecial cluster"
        loading="lazy"
      />

      <div class="flex flex-col justify-between gap-4">
        <div>
          <h4 class="md:text-4xl text-2xl md:mb-6 mb-3">
            Московский международный медицинский кластер
          </h4>
          <p class="md:text-xl text-lg ">
            Использование технологии цифровых двойников для&nbsp;улучшения управления и&nbsp;эксплуатации зданий,
            включая интеграцию с&nbsp;системами диспетчеризации и&nbsp;аналитику энергоэффективности. Особое внимание
            уделено практическому применению этих технологий в&nbsp;медицинском кластере Москвы для&nbsp;оптимизации
            медицинского обслуживания и&nbsp;образовательных процессов
          </p>
        </div>

        <a
          class="flex items-center gap-4"
          href="#"
        >
          <NuxtImg
            src="/pdf-logo.png"
            alt="pdf-logo"
            loading="lazy"
          />
          <p class="text-lg">PDF-презентация International medical cluster</p>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts"></script>

<style scoped></style>
