<template>
  <UModal>
    <UCard>
      <div class="flex flex-col items-center gap-3">
        <h2 class="text-xl text-center">
          Следующий докумиент будет полностью удален:
        </h2>
        <p class="font-bold text-center text-lg mb-1">
          {{ props.artifact.filename }}
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
import useDocumentArtifactsStore from '~/store/building/documentArtifacts';
import { EMPTY_ARTIFACT } from '~/utils/constants/Buildings';
import type { IBuildingArtifact } from '~/utils/types/Building';

const props = defineProps({
  artifact: {
    type: Object as () => IBuildingArtifact,
    default: () => ({ ...EMPTY_ARTIFACT }),
  },
});

const emit = defineEmits(['success']);
const documentArtifactsStore = useDocumentArtifactsStore();
const buildingStore = useBuildingStore();
const currentBuilding = computed(() => buildingStore.getCurrentBuilding);
const toast = useToast();
const loading = ref(false);

async function onAccept() {
  loading.value = true;

  try {
    await documentArtifactsStore.removeBimArtifact(currentBuilding.value.id, props.artifact.file_path);
    await buildingStore.fetchAllBuildingInfo();

    toast.add({
      title: 'Готово',
      description: 'Документ успешно удален',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно удалить документ, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
