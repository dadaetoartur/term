<template>
  <UModal>
    <UCard>
      <div class="flex flex-col items-center gap-3">
        <h2 class="text-xl text-center">
          Инженерная система будет удалена вместе с сохраненной BIM-моделью:
        </h2>
        <p class="font-bold text-center text-lg mb-1">
          {{ currentConstructionSection.name }}
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
import useConstructionSectionStore from '~/store/building/constructionSection';

const emit = defineEmits(['success']);
const toast = useToast();
const constructionSectionStore = useConstructionSectionStore();
const currentConstructionSection = computed(() => constructionSectionStore.getCurrentConstructionSection);
const loading = ref(false);

async function onAccept() {
  loading.value = true;

  try {
    await constructionSectionStore.removeConstructionSection(currentConstructionSection.value.id);

    toast.add({
      title: 'Готово',
      description: 'Инженерная секция успешно удалена',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно удалить инженерную секцию, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
