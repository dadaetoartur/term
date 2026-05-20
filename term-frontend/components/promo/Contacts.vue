<template>
  <section
    id="contacts"
    class="xl:mb-32 md:mb-28 mb-16"
  >
    <h2 class="xl:text-5xl md:text-4xl text-3xl xl:mb-16 md:mb-14 mb-9">
      Остались вопросы
    </h2>

    <div class="grid xl:grid-cols-12 grid-cols-1">
      <div class="flex flex-col xl:gap-8 gap-3 xl:col-span-6 mb-5">
        <p class="md:text-xl text-lg">
          Свяжитесь с нами по почте или заполните форму обратной связи
        </p>
        <a
          class="flex items-center gap-1"
          href="mailto:bimify@yandex.ru"
        >
          <UIcon
            class="text-2xl"
            name="i-heroicons-envelope"
          />
          <p class="md:text-xl text-lg">bimify@yandex.ru</p>
        </a>
      </div>

      <UForm
        :schema="schema"
        :state="state"
        class="max-w-2xl w-full space-y-4 xl:col-start-8 xl:col-span-5 grid place-self-center"
        @submit="onSubmit"
        @error="onError"
      >
        <UFormGroup
          class="relative"
          name="name"
        >
          <UInput
            v-model="state.name"
            input-class="text-lg"
            placeholder="Имя"
          />
          <template #error="{ error }">
            <span class="absolute -bottom-3 left-1">
              {{ error }}
            </span>
          </template>
        </UFormGroup>

        <UFormGroup
          class="relative"
          name="email"
        >
          <UInput
            v-model="state.email"
            input-class="text-lg"
            placeholder="Email"
          />
          <template #error="{ error }">
            <span class="absolute -bottom-3 left-1">
              {{ error }}
            </span>
          </template>
        </UFormGroup>

        <UFormGroup
          class="relative"
          name="phone"
        >
          <UInput
            v-model="state.phone"
            input-class="text-lg border-none"
            placeholder="Телефон"
          />
          <template #error="{ error }">
            <span class="absolute -bottom-3 left-1">
              {{ error }}
            </span>
          </template>
        </UFormGroup>

        <UFormGroup name="message">
          <UInput
            v-model="state.message"
            input-class="text-lg"
            placeholder="Сообщение"
          />
        </UFormGroup>

        <UFormGroup name="agreement">
          <template #default="{ error }">
            <UCheckbox v-model="state.agreement">
              <template #label>
                <span :class="error ? 'text-red-500 dark:text-red-400' : ''">
                  Я согласен(-на) на обработку персональных данных
                </span>
              </template>
            </UCheckbox>
          </template>
          <template #error />
        </UFormGroup>

        <UButton
          class="flex justify-center text-lg"
          type="submit"
          color="primary"
        >
          Отправить
        </UButton>
      </UForm>
    </div>
  </section>
</template>

<script setup lang="ts">
import { z } from 'zod';
import type { FormErrorEvent, FormSubmitEvent } from '#ui/types';

const state = reactive({
  name: undefined,
  email: undefined,
  phone: undefined,
  message: undefined,
  agreement: true,
});

const schema = z.object({
  name: z.string({ message: 'Обязательное поле' }).min(2, {
    message: 'Имя должно быть не короче 2 символов',
  }),
  email: z.string({ message: 'Обязательное поле' }).email({
    message: 'Проверьте правильность ввода адреса эл. почты',
  }),
  agreement: z.boolean().refine((value) => value === true, {
    message: 'Обязательное поле',
  }),
});

type Schema = z.infer<typeof schema>

async function onSubmit(event: FormSubmitEvent<Schema>) {
  // admin@example.com  initialPassword123
  console.log(event.data);
}

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id);
  element?.focus();
  element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
</script>

<style scoped></style>
