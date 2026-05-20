<template>
  <UModal>
    <UCard>
      <div class="flex flex-col items-center gap-3">
        <h2 class="text-xl text-center">
          Следующий объект капитального строительства будет полностью удален:
        </h2>
        <p class="font-bold text-center text-lg mb-1">
          {{ building.name }}
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
import useBuildingStore from '~/store/building';
import { EMPTY_BUILDING } from '~/utils/constants/Buildings';
import type { IBuilding } from '~/utils/types/Building';

const props = defineProps({
  building: {
    type: Object as () => IBuilding,
    default: () => ({ ...EMPTY_BUILDING }),
  },
});

const emit = defineEmits(['success']);
const toast = useToast();
const buildingStore = useBuildingStore();
const loading = ref(false);

async function onAccept() {
  loading.value = true;

  try {
    await buildingStore.removeBuilding(props.building.id);
    await buildingStore.fetchAllBuildingInfo();

    toast.add({
      title: 'Готово',
      description: 'Объект капитального строительства успешно удален',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно удалить объект капитального строительства, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
