<template>
  <main class="flex-grow h-full">
    <div class="absolute top-0 bottom-0 left-0 right-0 flex justify-center items-center">
      <UContainer>
        <UCard class="max-w-lg">
          <template #header>
            <div class="flex flex-col gap-3 items-center">
              <BimifyLogo />
              <h3 class="md:text-lg text-base text-center">
                Cистема для&nbsp;управления строительством с&nbsp;технологией цифрового двойника
              </h3>
            </div>
          </template>

          <UForm
            :schema="schema"
            :state="state"
            class="space-y-4"
            @submit="onSubmit"
            @error="onError"
          >
            <UFormGroup
              v-slot="{ error }"
              label="Имя пользователя"
              name="username"
            >
              <UInput
                v-model="state.username"
                placeholder="you@example.com"
                :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
              />
            </UFormGroup>

            <UFormGroup
              label="Пароль"
              name="password"
            >
              <UInput
                v-model="state.password"
                :type="passwordType"
                placeholder="******"
                :ui="{ icon: { trailing: { pointer: '' } } }"
              >
                <template #trailing>
                  <UButton
                    v-show="state.password !== ''"
                    color="gray"
                    variant="link"
                    :icon="passwordType === 'password' ? 'i-heroicons-eye' : 'i-heroicons-eye-slash'"
                    :padded="false"
                    @click="passwordType === 'password' ? passwordType = 'text' : passwordType = 'password'"
                  />
                </template>
              </UInput>
            </UFormGroup>

            <p class="md:text-base text-sm text-center">
              Ознакомиться с
              <ULink
                to="/#contacts"
                active-class="text-primary"
                inactive-class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
              >
                политикой конфиденциальности
              </ULink>
            </p>

            <UButton
              :loading="loading"
              class="w-full flex justify-center"
              color="primary"
              type="submit"
            >
              Войти
            </UButton>
          </UForm>

          <template #footer>
            <div class="flex flex-col items-center">
              <p class="md:text-base text-sm text-center">
                Нет аккаунта?
              </p>
              <p class="md:text-base text-sm text-center">
                Заполните
                <ULink
                  to="/#contacts"
                  active-class="text-primary"
                  inactive-class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                >
                  форму обратной связи
                </ULink>
                и мы свяжемся с вами!
              </p>
            </div>
          </template>
        </UCard>
      </UContainer>
    </div>
  </main>
</template>

<script setup lang="ts">
import { z } from 'zod';
import type { FormErrorEvent, FormSubmitEvent } from '#ui/types';
import { useAuthStore } from '~/store/auth';
import BimifyLogo from '~/components/BimifyLogo.vue';

definePageMeta({
  layout: false,
  middleware: 'auth',
});

const router = useRouter();
const toast = useToast();
const authStore = useAuthStore();
const loading = ref(false);
const passwordType = ref('password');

const state = reactive({
  username: undefined,
  password: undefined,
});

const schema = z.object({
  username: z.string({ message: 'Обязательное поле' }).email({
    message: 'Проверьте правильность ввода адреса эл. почты',
  }),
  password: z.string({ message: 'Обязательное поле' }).min(2, {
    message: 'Пароль должен быть не короче 2 символов',
  }),
});

type Schema = z.infer<typeof schema>

async function onSubmit(event: FormSubmitEvent<Schema>) {
  // admin@example.com  initialPassword123
  loading.value = true;

  try {
    await authStore.login({
      username: event.data.username,
      password: event.data.password,
    });

    router.push('/management');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Неправильное имя пользователя или пароль',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id);
  element?.focus();
  element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
</script>

<style lang="scss" scoped></style>
