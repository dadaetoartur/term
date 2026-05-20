<template>
  <footer class="bg-gray-300 dark:bg-neutral-800  py-12">
    <UContainer class="grid xl:grid-cols-8 xl:grid-rows-1 items-start gap-5">
      <div class="xl:col-span-2 flex flex-col gap-3">
        <BimifyLogo />

        <a
          class="flex items-center gap-1"
          href="mailto:bimify@yandex.ru"
        >
          <UIcon
            class="text-2xl"
            name="i-heroicons-envelope"
          />
          <p class="text-lg =">bimify@yandex.ru</p>
        </a>
      </div>

      <nav
        class="flex md:flex-row flex-col w-full justify-between justify-self-center gap-5 xl:col-start-3 xl:col-span-4 xl:row-start-1 row-start-2"
      >
        <ul class="flex flex-col gap-5 xl:gap-12">
          <li>
            <NuxtLink to="/#about">
              <p class="text-lg">
                Цифровой двойник
              </p>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/#advantages">
              <p class="text-lg">
                Приемущества
              </p>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/#projects">
              <p class="text-lg">
                Наши проекты
              </p>
            </NuxtLink>
          </li>
        </ul>

        <ul class="flex flex-col gap-5 xl:gap-12">
          <li>
            <NuxtLink to="/#facilities">
              <p class="text-lg">
                Возможности платформы
              </p>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/#quickstart">
              <p class="text-lg">
                Быстрый старт
              </p>
            </NuxtLink>
          </li>
          <li>
            <a
              href="https://bimify.systems/sp131/"
              target="_blank"
            >
              <p class="text-lg">
                Машиночитаемые документы - СП 131
              </p>
            </a>
          </li>
        </ul>
      </nav>

      <div
        class="md:grid md:grid-cols-4 md:items-end md:justify-self-end xl:col-start-7 xl:col-span-4 xl:row-start-1 md:col-start-2 md:row-start-1 row-start-3"
      >
        <a
          class="md:col-start-2 md:col-span-3"
          href="https://fasie.ru/"
          target="_blank"
        >
          <img
            class="mb-2"
            src="~/assets/images/fond-support.svg"
            alt="фонд содействия инновациям"
          >
        </a>
        <p class="md:col-span-4 md:text-end text-start text-xs">
          Проект создан при поддержке Фондом содействия инновациям в рамках федерального проекта «Платформа
          университетского технологического предпринимательства»
        </p>
      </div>
    </UContainer>
  </footer>
</template>

<script setup lang="ts">
import BimifyLogo from './BimifyLogo.vue';
</script>

<style scoped></style>
