<template>
  <div>
    <div class="flex items-center justify-end gap-3 mb-3">
      <UInput
        v-model="search"
        class="w-full"
        icon="i-heroicons-magnifying-glass-20-solid"
        placeholder="Отфильтровать объекты"
      />
    </div>

    <UTable
      :loading="props.loading"
      :rows="tableFilter.rows"
      :columns="columns"
    >
      <template #switch-data="{ row }">
        <UButton
          v-if="row.name !== currentConstructionPart.name"
          color="gray"
          label="Выбрать объект"
          @click="constructionPartStore.setCurrentConstructionPart(row)"
        />
        <UButton
          v-else
          :disabled="true"
          color="gray"
          variant="outline"
          label="Используется"
        />
      </template>

      <template #actions-data="{ row }">
        <UDropdown
          :ui="{ width: 'w-32' }"
          :items="items(row)"
        >
          <UButton
            color="gray"
            variant="ghost"
            icon="i-heroicons-ellipsis-horizontal-20-solid"
          />
        </UDropdown>
      </template>

      <template #empty-state>
        <div class="flex flex-col items-center justify-center py-6 gap-3">
          <UIcon name="i-heroicons-circle-stack-20-solid" />
          <span class="italic text-sm">Нет ни одного объекта!</span>
        </div>
      </template>
    </UTable>

    <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700 ">
      <UPagination
        v-model="page"
        :page-count="pageRowsCount"
        :total="tableFilter.filtered.length"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import useTableFilter from '~/utils/hooks/useTableFilter';
import type { DropdownItem } from '#ui/types';
import type { IBuildingConstructionPart } from '~/utils/types/Building';
import useConstructionPartStore from '~/store/building/constructionPart';
import useBuildingStore from '~/store/building';
import EditConstructionPart from './modals/EditConstructionPart.vue';
import RemoveConstructionPart from './modals/RemoveConstructionPart.vue';

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
});

const modal = useModal();

const buildingStore = useBuildingStore();
const constructionPartStore = useConstructionPartStore();
const constructionParts = computed(() => buildingStore.getCurrentBuilding.constructionParts);
const currentConstructionPart = computed(() => constructionPartStore.getCurrentConstructionPart);

const search = ref('');
const page = ref(1);
const pageRowsCount = 10;

const columns = [{
  key: 'name',
  label: 'Наименование',
  sortable: true,
}, {
  key: 'address.city',
  label: 'Город',
}, {
  key: 'address.street',
  label: 'Улица',
}, {
  key: 'address.building',
  label: 'Дом',
}, {
  key: 'switch',
  label: 'Переключить объект',
}, {
  key: 'actions',
}];

const items = (row: IBuildingConstructionPart): DropdownItem[][] => [
  [{
    label: 'Изменить',
    icon: 'i-heroicons-pencil-square-20-solid',
    click: () => modal.open(EditConstructionPart, {
      object: row,
      onSuccess() {
        modal.close();
      },
    }),
  }], [{
    label: 'Удалить',
    icon: 'i-heroicons-trash-20-solid',
    iconClass: 'text-red-500',
    click: () => modal.open(RemoveConstructionPart, {
      object: row,
      onSuccess() {
        modal.close();
      },
    }),
  }],
];

const tableFilter = computed(() => useTableFilter<IBuildingConstructionPart>(constructionParts.value, search.value, page.value, pageRowsCount));
</script>

<style scoped></style>
