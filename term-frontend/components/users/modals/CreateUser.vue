<template>
  <UModal>
    <UCard>
      <UForm
        :schema="schema"
        :state="state"
        class="space-y-4 flex flex-col"
        @submit="onSubmit"
        @error="onError"
      >
        <h2 class="text-xl text-center">
          Добавление сотрудника
        </h2>
        <UDivider />
        <div class="flex flex-col gap-3">
          <UFormGroup
            v-slot="{ error }"
            name="first_name"
            label="Имя"
          >
            <UInput
              v-model="state.first_name"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
            />
          </UFormGroup>

          <UFormGroup
            v-slot="{ error }"
            name="last_name"
            label="Фамилия"
          >
            <UInput
              v-model="state.last_name"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
            />
          </UFormGroup>

          <UFormGroup
            v-slot="{ error }"
            name="middle_name"
            label="Отчество"
          >
            <UInput
              v-model="state.middle_name"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
            />
          </UFormGroup>

          <UFormGroup
            v-slot="{ error }"
            name="email"
            label="Адрес электронной почты"
          >
            <UInput
              v-model="state.email"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
            />
          </UFormGroup>

          <UFormGroup
            v-slot="{ error }"
            name="password"
            label="Пароль"
          >
            <UInput
              v-model="state.password"
              :type="passwordType"
              placeholder="******"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
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

          <UFormGroup
            v-slot="{ error }"
            name="mobile_phone"
            label="Мобильный телефон"
          >
            <UInput
              v-model="state.mobile_phone"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
            />
          </UFormGroup>

          <UFormGroup
            name="role"
            label="Роль"
          >
            <USelectMenu
              v-model="state.role"
              placeholder="Выберите роль"
              :options="userRoles"
              value-attribute="role"
              option-attribute="name"
            />
          </UFormGroup>

          <UFormGroup
            name="active"
            label="Профиль активен"
            class="flex items-center flex-row-reverse justify-end gap-3"
          >
            <UToggle
              v-model="state.is_active"
              on-icon="i-heroicons-check-20-solid"
              off-icon="i-heroicons-x-mark-20-solid"
              disabled
            />
          </UFormGroup>

          <UFormGroup
            name="verified"
            label="Профиль верифицирован"
            class="flex items-center flex-row-reverse justify-end gap-3"
          >
            <UToggle
              v-model="state.is_verified"
              on-icon="i-heroicons-check-20-solid"
              off-icon="i-heroicons-x-mark-20-solid"
              disabled
            />
          </UFormGroup>

          <UFormGroup
            name="superuser"
            label="Права администратора"
            class="flex items-center flex-row-reverse justify-end gap-3"
          >
            <UToggle
              v-model="state.is_superuser"
              on-icon="i-heroicons-check-20-solid"
              off-icon="i-heroicons-x-mark-20-solid"
              disabled
            />
          </UFormGroup>
        </div>

        <div class="self-center flex justify-center gap-3">
          <UButton
            :loading="loading"
            type="submit"
            class="px-8"
          >
            Создать
          </UButton>

          <UButton
            variant="outline"
            class="px-8"
            @click="emit('success')"
          >
            Отменить
          </UButton>
        </div>
      </UForm>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
import { z } from 'zod';
import type { FormErrorEvent, FormSubmitEvent } from '#ui/types';
import useUserStore from '~/store/user';
import type { IUser } from '~/utils/types/User';
import { EMPTY_USER, USER_ROLES } from '~/utils/constants/Users';

const props = defineProps({
  user: {
    type: Object as () => IUser,
    default: () => ({ ...EMPTY_USER }),
  },
});

const emit = defineEmits(['success']);
type IStateForm = IUser & { password: string }

const userStore = useUserStore();
const toast = useToast();

const loading = ref(false);
const userRoles = ref([...USER_ROLES]);
const passwordType = ref('password');

const state = ref<IStateForm>({ ...props.user, password: '' });

const schema = z.object({
  first_name: z.string().min(2, {
    message: 'Имя должно быть не короче 2 символов',
  }),
  last_name: z.string().min(2, {
    message: 'Фамилия должна быть не короче 2 символов',
  }),
  middle_name: z.string().min(2, {
    message: 'Отчество должно быть не короче 2 символов',
  }),
  mobile_phone: z.string()
    .regex(/^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$/, 'Некорректный номер телефона'),
  email: z.string().email({
    message: 'Проверьте правильность ввода адреса эл. почты',
  }),
  password: z.string().min(5, {
    message: 'Пароль должен быть не короче 5 символов',
  }),
  role: z.string().refine((option) => option, {
    message: 'Выберите роль сотрудника',
  }),
  is_active: z.boolean(),
  is_superuser: z.boolean(),
  is_verified: z.boolean(),
});

type Schema = z.infer<typeof schema>

async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true;

  try {
    await userStore.createUser(event.data);
    await userStore.fetchAllUsers();

    toast.add({
      title: 'Готово',
      description: 'Новый сотрудник успешно зарегистрирован',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно зарегистрировать сотрудника, попробуйте позже',
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

<style scoped></style>
