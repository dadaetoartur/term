<template>
  <UCard>
    <div class="flex justify-between pb-3.5 border-b border-gray-200 dark:border-gray-700">
      <UInput
        v-model="search"
        class="w-80"
        icon="i-heroicons-magnifying-glass-20-solid"
        placeholder="Отфильтровать задачи"
      />

      <UButton
        class="self-center "
        label="Добавить задачу"
      />
    </div>

    <UTable
      :rows="tableFilter.rows"
      :columns="columns"
    >
      <template #date-data="{ row }">
        {{ new Date(row.date).toLocaleString() }}
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
          <span class="italic text-sm">Нет ни одной задачи!</span>
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
  worker: string
  status: string
  date: Date
  failed: string
  delta: string
}

const columns = [{
  key: 'id',
  label: 'ID',
}, {
  key: 'name',
  label: 'Наименование',
}, {
  key: 'worker',
  label: 'Сотрудник',
  sortable: true,
}, {
  key: 'status',
  label: 'Статус',
  sortable: true,
}, {
  key: 'date',
  label: 'Дата',
  sortable: true,
}, {
  key: 'failed',
  label: 'Повторные отказы',
}, {
  key: 'delta',
  label: 'Дельта',
}, {
  key: 'actions',
}];

const tasks: ITableRow[] = [{
  id: 1,
  name: 'Отремонтировать проводку',
  worker: 'Петров А.А.',
  status: 'В работе',
  date: new Date(),
  failed: '50%',
  delta: '3%',
},
{
  id: 2,
  name: 'Проверить работу систем отопления',
  worker: 'Петров А.А.',
  status: 'Выполнено',
  date: new Date(),
  failed: '10%',
  delta: '4%',
}];

const items = (row: ITableRow) => [
  [{
    label: 'Изменить',
    icon: 'i-heroicons-pencil-square-20-solid',
    click: () => console.log('Edit', row.id),
  }], [{
    label: 'Удалить',
    icon: 'i-heroicons-trash-20-solid',
    iconClass: 'text-red-500',
    click: () => console.log('Delete', row.id),
  }],
];

const search = ref('');
const page = ref(1);
const pageRowsCount = 10;

const tableFilter = computed(() => useTableFilter<ITableRow>(tasks, search.value, page.value, pageRowsCount));
</script>

<style scoped></style>
~/utils/hooks/useTableFilter
