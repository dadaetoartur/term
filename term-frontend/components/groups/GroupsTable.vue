<template>
  <UCard>
    <div class="flex justify-between pb-3.5 border-b border-gray-200 dark:border-gray-700">
      <UInput
        v-model="search"
        class="w-80"
        icon="i-heroicons-magnifying-glass-20-solid"
        placeholder="Отфильтровать группы"
      />

      <UButton
        class="self-center"
        label="Создать группу"
        @click="addGroup"
      />
    </div>

    <UTable
      :rows="tableFilter.rows"
      :columns="columns"
      :loading="loading"
      :loading-state="{ icon: 'i-heroicons-arrow-path-20-solid', label: 'Загрузка...' }"
      :progress="{ color: 'primary', animation: 'carousel' }"
    >
      <template #users-data="{ row }">
        <div class="flex items-start flex-wrap gap-1">
          <UBadge
            v-for="item in row.users as IUser[]"
            :key="item.id"
            class="flex items-center gap-2"
          >
            <p>{{ `${item.last_name} ${item.first_name} ${item.middle_name}` }}</p>
          </UBadge>
        </div>
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
          <span class="italic text-sm">Нет ни одной группы!</span>
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
import type { IGroup } from '~/utils/types/Group';
import type { IUser } from '~/utils/types/User';
import CreateGroup from './modals/CreateGroup.vue';
import RemoveGroup from './modals/RemoveGroup.vue';
import EditGroup from './modals/EditGroup.vue';

const props = defineProps({
  groups: {
    type: Array as () => IGroup[],
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const search = ref('');
const page = ref(1);
const pageRowsCount = 10;
const modal = useModal();

const columns = [{
  key: 'name',
  label: 'Наименование',
  sortable: true,
}, {
  key: 'description',
  label: 'Описание',
  sortable: true,
}, {
  key: 'users',
  label: 'Пользователи в группе',
  sortable: true,
}, {
  key: 'actions',
}];

const items = (row: IGroup) => [
  [{
    label: 'Изменить',
    icon: 'i-heroicons-pencil-square-20-solid',
    click: () => modal.open(EditGroup, {
      group: row,
      onSuccess() {
        modal.close();
      },
    }),
  }], [{
    label: 'Удалить',
    icon: 'i-heroicons-trash-20-solid',
    iconClass: 'text-red-500',
    click: () => modal.open(RemoveGroup, {
      group: row,
      onSuccess() {
        modal.close();
      },
    }),
  }],
];

const tableFilter = computed(() => useTableFilter<IGroup>(props.groups, search.value, page.value, pageRowsCount));

function addGroup() {
  modal.open(CreateGroup, {
    onSuccess() {
      modal.close();
    },
  });
}
</script>

<style scoped></style>
