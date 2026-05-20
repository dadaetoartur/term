<template>
  <UModal>
    <UCard :ui="{ body: { base: 'flex flex-col  gap-5' } }">
      <h2 class="text-xl text-center">
        Добавление документа в хранилище
      </h2>

      <UCard :ui="{ body: { base: 'p-0' } }">
        <div class="flex flex-col gap-1">
          <p>В хранилище вы можете добавить только файлы следующих форматов:</p>
          <div class="flex flex-row gap-1">
            <UBadge
              v-for="(format, index) in docFormats"
              :key="index"
            >
              {{ format }}
            </UBadge>
          </div>
        </div>
      </UCard>

      <div class="flex flex-col gap-3">
        <UTooltip text="Загрузить новую модель">
          <UInput
            v-model="inputFile"
            class="w-full"
            type="file"
            @change="loadDocument"
          />
        </UTooltip>
      </div>

      <div class="self-center flex justify-center gap-3">
        <UButton
          :disabled="!documentFormData.get('file')"
          :loading="loading"
          class="px-8"
          @click="saveDocument"
        >
          Загрузить
        </UButton>

        <UButton
          variant="outline"
          class="px-8"
          @click="emit('success')"
        >
          Отменить
        </UButton>
      </div>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
import useBuildingStore from '~/store/building';
import useDocumentArtifactsStore from '~/store/building/documentArtifacts';

const emit = defineEmits(['success']);

const toast = useToast();
const documentArtifactsStore = useDocumentArtifactsStore();
const buildingStore = useBuildingStore();
const currentBuilding = computed(() => buildingStore.getCurrentBuilding);

const inputFile = ref<FileList>();
const documentFormData = ref<FormData>(new FormData());
const loading = ref(false);

const docFormats = ['PDF', 'DOC', 'DOCX', 'XLS', 'XLSX'];

const loadDocument = (fileList: FileList) => {
  documentFormData.value = new FormData();
  const fileNameSplit = fileList[0].name.toLocaleUpperCase().split('.');

  if (!docFormats.includes(fileNameSplit[fileNameSplit.length - 1])) {
    inputFile.value = undefined;

    toast.add({
      title: 'Ошибка формата файла',
      description: 'Данный формат файла не подходит',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });

    return;
  }

  documentFormData.value?.append('file', fileList[0]);
};

async function saveDocument() {
  loading.value = true;

  try {
    if (documentFormData.value?.get('file')) {
      await documentArtifactsStore.uploadBimArtifact(currentBuilding.value.id, documentFormData.value);
      await buildingStore.fetchAllBuildingInfo();

      toast.add({
        title: 'Готово',
        description: 'Новый документ успешно добавлен',
        icon: 'i-heroicons-check-circle',
        color: 'green',
      });

      emit('success');
    } else {
      toast.add({
        title: 'Ошибка',
        description: 'Вы не добавили ни один файл для отправки',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно сохранить документ на сервере, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}
</script>

<style scoped></style>
