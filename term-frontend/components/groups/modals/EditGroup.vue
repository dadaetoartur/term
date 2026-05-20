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
          Изменение группы
        </h2>

        <UDivider />

        <div class="flex flex-col gap-3">
          <UFormGroup
            v-slot="{ error }"
            name="name"
            label="Наименование"
          >
            <UInput
              v-model="state.name"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
            />
          </UFormGroup>

          <UFormGroup
            v-slot="{ error }"
            name="description"
            label="Описание"
          >
            <UInput
              v-model="state.description"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
            />
          </UFormGroup>

          <div class="flex flex-col gap-1">
            <h3 class="text-sm">
              Добавить пользователей в группу
            </h3>
            <div class="flex items-start flex-wrap gap-1 mb-1">
              <UBadge
                v-for="(item, index) in selected"
                :key="item.id"
                class="flex items-center gap-2"
              >
                <p>{{ item.label }}</p>
                <UIcon
                  class="cursor-pointer"
                  name="i-heroicons-x-mark"
                  @click="selected.splice(index, 1)"
                />
              </UBadge>
            </div>

            <div class="rounded-lg border border-gray-300 dark:border-gray-700">
              <UCommandPalette
                v-model="selected"
                placeholder="Введите имя сотрудника..."
                multiple
                nullable
                :empty-state="{ icon: 'i-heroicons-magnifying-glass-20-solid', label: 'По вашему запросу ничего не найдено.', queryLabel: 'По вашему запросу ничего не найдено. Попробуйте еще раз.' }"
                :autoselect="false"
                :groups="[{ key: 'people', commands: peoples }]"
                :fuse="{ resultLimit: 6, fuseOptions: { threshold: 0.1 } }"
              />
            </div>
          </div>
        </div>

        <div class="self-center flex justify-center gap-3">
          <UButton
            :loading="loading"
            type="submit"
            class="px-8"
          >
            Изменить
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
import type { IGroup } from '~/utils/types/Group';
import useGroupStore from '~/store/group';
import useUserStore from '~/store/user';
import type { IUser } from '~/utils/types/User';
import { EMPTY_GROUP } from '~/utils/constants/Groups';

const props = defineProps({
  group: {
    type: Object as () => IGroup,
    default: () => ({ ...EMPTY_GROUP }),
  },
});

const groupStore = useGroupStore();
const toast = useToast();
const userStore = useUserStore();
const users = computed(() => userStore.getAllUsers);

const peopleTemplate = (user: Omit<IUser, 'group'>) => ({
  id: String(user.id),
  label: `${user.last_name} ${user.first_name} ${user.middle_name}`,
  suffix: String(user.email),
});

const peoples = computed(() => users.value.map((user) => peopleTemplate(user)));
const peoplesInGroup = computed(() => props.group.users.map((user) => peopleTemplate(user)));
const selected = ref<typeof peoples.value>(peoplesInGroup.value || []);

const emit = defineEmits(['success']);

const loading = ref(false);
const state = ref<IGroup>({ ...props.group });

const schema = z.object({
  name: z.string().min(2, {
    message: 'Название должно быть не короче 2 символов',
  }),
  description: z.string().min(2, {
    message: 'Описание должно быть не короче 2 символов',
  }),
});

type Schema = z.infer<typeof schema>

async function onSubmit(event: FormSubmitEvent<Schema & { [key: string]: string }>) {
  loading.value = true;
  const body: Partial<Omit<IGroup, 'id' | 'users'>> = {};

  for (const key of Object.keys(event.data)) {
    if (key in event.data && props.group[key] !== event.data[key]) {
      body[key] = event.data[key];
    }
  }

  try {
    if (Object.keys(body).length > 0) {
      await groupStore.updateGroup(props.group.id, body);
    }

    const updateUsersToGroup: Promise<any>[] = [];

    if (selected.value && selected.value.length > 0) {
      selected.value.forEach((user) => {
        if (!peoplesInGroup.value.find((item) => item.id === user.id)) {
          // add new users to group
          updateUsersToGroup.push(groupStore.addUserToGroup(props.group.id, user.id));
        }
      });

      peoplesInGroup.value.forEach((user) => {
        if (!selected.value.find((item) => item.id === user.id)) {
          // remove users from group
          updateUsersToGroup.push(groupStore.removeUserFromGroup(props.group.id, user.id));
        }
      });
    } else {
      // remove all users from group
      peoplesInGroup.value.forEach((user) => updateUsersToGroup.push(groupStore.removeUserFromGroup(props.group.id, user.id)));
    }

    await Promise.all(updateUsersToGroup);
    await groupStore.fetchAllGroups();
    await userStore.fetchAllUsers();

    toast.add({
      title: 'Готово',
      description: 'Новая группа успешно создана',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно создать группу, попробуйте позже',
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

onMounted(async () => {
  if (Object.keys(users.value).length === 0) {
    await userStore.fetchAllUsers();
  }
});
</script>

<style scoped></style>
