<template>
  <UCard>
    <div class="flex justify-between pb-3.5 border-b border-gray-200 dark:border-gray-700">
      <UInput
        v-model="search"
        class="w-80"
        icon="i-heroicons-magnifying-glass-20-solid"
        placeholder="Отфильтровать договоры"
      />

      <UButton
        class="self-center "
        label="Добавить договор"
      />
    </div>

    <UTable
      :rows="tableFilter.rows"
      :columns="columns"
    >
      <template #url-data="{ row }">
        <ULink
          :to="row.url"
          target="_blank"
          active-class="text-primary"
          inactive-class="underline text-gray-500 dark:text-gray-400 hover:text-primary dark:hover:text-primary"
        >
          {{ row.url }}
        </ULink>
      </template>

      <template #date-data="{ row }">
        {{ new Date(row.date).toLocaleString() }}
      </template>

      <template #version-data="{ row }">
        <UBadge variant="outline">
          {{ row.version }}
        </UBadge>
      </template>

      <template #actions-data="{ row }">
        <UDropdown :items="items(row)">
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
          <span class="italic text-sm">Нет ни одного договора!</span>
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
import useTableFilter from '~/utils/hooks/useTableFilter';

interface ITableRow {
  id: number
  name: string
  url: string
  agent: string
  date: Date
  version: number
}

const columns = [{
  key: 'id',
  label: 'ID',
}, {
  key: 'name',
  label: 'Наименование',
  sortable: true,
}, {
  key: 'url',
  label: 'Ссылка',
}, {
  key: 'agent',
  label: 'Контр. Агент',
}, {
  key: 'date',
  label: 'Дата',
  sortable: true,
}, {
  key: 'version',
  label: 'Версия',
}, {
  key: 'actions',
}];

const contracts: ITableRow[] = [{
  id: 1,
  name: 'Клининг',
  url: 'http://localhost:3000',
  agent: 'ООО "Кристалл"',
  date: new Date(2023),
  version: 1.01,
}, {
  id: 2,
  name: 'Аренда помещения',
  url: 'http://localhost:3000',
  agent: 'АНО "АСИ"',
  date: new Date(2022),
  version: 1.02,
}, {
  id: 3,
  name: 'Клининг',
  url: 'http://localhost:3000',
  agent: 'ООО "Кристалл"',
  date: new Date(),
  version: 1.1,
}];

const items = (row: ITableRow) => [
  [{
    label: 'Удалить',
    icon: 'i-heroicons-trash-20-solid',
    iconClass: 'text-red-500',
    click: () => console.log('Delete', row.id),
  }],
];

const search = ref('');
const page = ref(1);
const pageRowsCount = 10;

const tableFilter = computed(() => useTableFilter<ITableRow>(contracts, search.value, page.value, pageRowsCount));
</script>

<style scoped></style>
