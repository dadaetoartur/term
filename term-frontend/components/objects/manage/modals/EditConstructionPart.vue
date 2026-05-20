<template>
  <UModal :ui="{ width: 'sm:max-w-6xl' }">
    <UCard>
      <template #header>
        <h2 class="text-xl text-center">
          Изменение данных об объекте капитального строительства
        </h2>
      </template>
      <div class="space-y-4 flex flex-col">
        <ConstructionPartForm
          :info="editObject"
          @updated-data="editObject = $event"
        />

        <div class="self-center flex justify-center gap-3">
          <UButton
            :loading="loading"
            type="submit"
            class="px-8"
            @click="saveEditObject"
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
import type { IBuildingConstructionPart } from '~/utils/types/Building';
import useBuildingStore from '~/store/building';
import useConstructionPartStore from '~/store/building/constructionPart';
import ConstructionPartForm from '../../form/ConstructionPartForm.vue';

const props = defineProps({
  object: {
    type: Object as () => IBuildingConstructionPart,
    default: () => ({ ...EMPTY_BUILDING }),
  },
});

const emit = defineEmits(['success']);

const toast = useToast();
const buildingStore = useBuildingStore();
const constructionPartStore = useConstructionPartStore();
const loading = ref(false);
const editObject = ref<IBuildingConstructionPart>({ ...props.object });

async function saveEditObject() {
  loading.value = true;

  try {
    await constructionPartStore.editConstructionPart(props.object.id, editObject.value);
    await buildingStore.fetchAllBuildingInfo();

    toast.add({
      title: 'Готово',
      description: 'Объект (строение) успешно изменен',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно изменить объект (строение), попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
