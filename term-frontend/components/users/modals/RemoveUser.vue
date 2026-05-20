<template>
  <UModal>
    <UCard>
      <div class="flex flex-col items-center gap-3">
        <h2 class="text-xl text-center">
          Следующий сотрудник будет полностью удален:
        </h2>
        <p class="font-bold text-center text-lg mb-1">
          {{ `${user.last_name} ${user.first_name} ${user.middle_name}` }}
        </p>

        <div class="self-center flex justify-center gap-3">
          <UButton
            :loading="loading"
            type="submit"
            class="px-8"
            @click="onAccept"
          >
            Удалить
          </UButton>

          <UButton
            variant="outline"
            class="px-8"
            @click="emit('success')"
          >
            Отменить
          </UButton>
        </div>
      </div>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
import useUserStore from '~/store/user';
import { EMPTY_USER } from '~/utils/constants/Users';
import type { IUser } from '~/utils/types/User';

const props = defineProps({
  user: {
    type: Object as () => IUser,
    default: () => ({ ...EMPTY_USER }),
  },
});

const emit = defineEmits(['success']);
const userStore = useUserStore();
const toast = useToast();
const loading = ref(false);

async function onAccept() {
  loading.value = true;

  try {
    await userStore.removeUser(props.user.id);
    await userStore.fetchAllUsers();

    toast.add({
      title: 'Готово',
      description: 'Сотрудник успешно удален',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно удалить сотрудника, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
