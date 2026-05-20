<template>
  <UModal>
    <UCard>
      <div class="flex flex-col items-center gap-3">
        <h2 class="text-xl text-center">
          Следующий объект (строение) будет удален из данного ОКС:
        </h2>
        <p class="font-bold text-center text-lg mb-1">
          {{ object.name }}
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
import useConstructionPartStore from '~/store/building/constructionPart';
import { EMPTY_CONSTRUCTION_PART } from '~/utils/constants/Buildings';
import type { IBuildingConstructionPart } from '~/utils/types/Building';

const props = defineProps({
  object: {
    type: Object as () => IBuildingConstructionPart,
    default: () => ({ ...EMPTY_CONSTRUCTION_PART }),
  },
});

const emit = defineEmits(['success']);
const toast = useToast();
const buildingStore = useBuildingStore();
const constructionPartStore = useConstructionPartStore();
const loading = ref(false);

async function onAccept() {
  loading.value = true;

  try {
    await constructionPartStore.removeConstructionPart(props.object.id);
    await buildingStore.fetchAllBuildingInfo();

    toast.add({
      title: 'Готово',
      description: 'Объект (строение) успешно удален',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно удалить объект (строение), попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
