<template>
  <UModal>
    <UCard>
      <div class="flex flex-col items-center gap-3">
        <h2 class="text-xl text-center">
          Следующая группа будет полностью удалена:
        </h2>
        <p class="font-bold text-center text-lg mb-1">
          {{ group.name }}
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
import useGroupStore from '~/store/group';
import useUserStore from '~/store/user';
import { EMPTY_GROUP } from '~/utils/constants/Groups';
import type { IGroup } from '~/utils/types/Group';

const props = defineProps({
  group: {
    type: Object as () => IGroup,
    default: () => ({ ...EMPTY_GROUP }),
  },
});

const emit = defineEmits(['success']);
const groupStore = useGroupStore();
const userStore = useUserStore();
const toast = useToast();
const loading = ref(false);

async function onAccept() {
  loading.value = true;

  try {
    await groupStore.removeGroup(props.group.id);
    await groupStore.fetchAllGroups();
    await userStore.fetchAllUsers();

    toast.add({
      title: 'Готово',
      description: 'Группа успешно удалена',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно удалить группу, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
