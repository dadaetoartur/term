<template>
  <UModal :ui="{ width: 'sm:max-w-6xl' }">
    <UCard>
      <template #header>
        <h2 class="text-xl text-center">
          Изменение данных об объекте капитального строительства
        </h2>
      </template>
      <div class="space-y-4 flex flex-col">
        <BuildingForm
          :info="editBuilding"
          @updated-data="editBuilding = $event"
        />

        <div class="self-center flex justify-center gap-3">
          <UButton
            :loading="loading"
            type="submit"
            class="px-8"
            @click="saveEditBuilding"
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
      </div>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
import { EMPTY_BUILDING } from '~/utils/constants/Buildings';
import type { IBuilding } from '~/utils/types/Building';
import useBuildingStore from '~/store/building';
import BuildingForm from '../../form/BuildingForm.vue';

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
const editBuilding = ref<IBuilding>({ ...props.building });

async function saveEditBuilding() {
  loading.value = true;

  try {
    await buildingStore.editBuildingInfo(props.building.id, editBuilding.value);
    await buildingStore.fetchAllBuildingInfo();

    toast.add({
      title: 'Готово',
      description: 'Объект капитального строительства успешно изменен',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно изменить объект капитального строительства, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
