<template>
  <UCard>
    <div class="flex justify-between pb-3.5 border-b border-gray-200 dark:border-gray-700">
      <UInput
        v-model="search"
        class="w-80"
        icon="i-heroicons-magnifying-glass-20-solid"
        placeholder="Отфильтровать документы"
      />

      <UButton
        class="self-center "
        label="Добавить документ"
        @click="addDocument"
      />
    </div>

    <a
      ref="downloadRef"
      class="hidden"
      href=""
    />

    <UTable
      :rows="tableFilter.rows"
      :columns="columns"
    >
      <template #last_modified-data="{ row }">
        {{ new Date(row.last_modified).toLocaleString() }}
      </template>

      <template #actions-data="{ row }">
        <div class="flex items-center gap-3">
          <UButton
            class="flex-1 flex justify-center"
            color="primary"
            label="Загрузить"
            icon="i-heroicons-cloud-arrow-down"
            @click="downloadFile(row)"
          />

          <UButton
            class="flex-1 flex justify-center"
            color="red"
            label="Удалить"
            icon="i-heroicons-trash"
            @click="removeDocument(row)"
          />
        </div>
      </template>

      <template #empty-state>
        <div class="flex flex-col items-center justify-center py-6 gap-3">
          <UIcon name="i-heroicons-circle-stack-20-solid" />
          <span class="italic text-sm">Нет ни одного документа!</span>
        </div>
      </template>
    </UTable>

    <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
      <UPagination
        v-model="page"
        :page-count="pageRowsCount"
        :total="tableFilter.filtered.length"
      />
    </div>
  </UCard>
</template>

<script setup lang="ts">
import useBuildingStore from '~/store/building';
import useTableFilter from '~/utils/hooks/useTableFilter';
import type { IBuildingArtifact } from '~/utils/types/Building';
import useDocumentArtifactsStore from '~/store/building/documentArtifacts';
import CreateDocument from './modals/CreateDocument.vue';
import RemoveDocument from './modals/RemoveDocument.vue';

const modal = useModal();
const toast = useToast();
const documentArtifactsStore = useDocumentArtifactsStore();
const buildingStore = useBuildingStore();
const currentBuilding = computed(() => buildingStore.getCurrentBuilding);

const columns = [{
  key: 'filename',
  label: 'Наименование',
  sortable: true,
}, {
  key: 'last_modified',
  label: 'Последнее изменение',
  sortable: true,
}, {
  key: 'actions',
}];

const downloadRef = ref<HTMLAnchorElement>();
const search = ref('');
const page = ref(1);
const pageRowsCount = 10;

const tableFilter = computed(() => useTableFilter<IBuildingArtifact>(currentBuilding.value.documentArtifacts, search.value, page.value, pageRowsCount));

const addDocument = () => modal.open(CreateDocument, {
  async onSuccess() {
    modal.close();
  },
});

const removeDocument = (artifact: IBuildingArtifact) => modal.open(RemoveDocument, {
  artifact,
  async onSuccess() {
    modal.close();
  },
});

const downloadFile = async (artifact: IBuildingArtifact) => {
  if (downloadRef.value) {
    try {
      const documentBlob = await documentArtifactsStore.downloadBimArtifact(currentBuilding.value.id, artifact.file_path);
      const documentFile = new File([documentBlob], artifact.filename);

      downloadRef.value.href = URL.createObjectURL(documentFile);
      downloadRef.value.download = documentFile.name;
      downloadRef.value.click();

      downloadRef.value.href = '';
      downloadRef.value.download = '';
    } catch (error) {
      toast.add({
        title: 'Ошибка',
        description: 'При загрузки документа с сервера, что-то пошло не так',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  }
};
</script>

<style scoped></style>
