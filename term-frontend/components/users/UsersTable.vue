<template>
  <UCard>
    <div class="flex justify-between pb-3.5 border-b border-gray-200 dark:border-gray-700">
      <UInput
        v-model="search"
        class="w-80"
        icon="i-heroicons-magnifying-glass-20-solid"
        placeholder="Отфильтровать сотрудников"
      />

      <UButton
        class="self-center"
        label="Добавить сотрудника"
        @click="addUser"
      />
    </div>

    <UTable
      :rows="tableFilter.rows"
      :columns="columns"
      :loading="loading"
      :loading-state="{ icon: 'i-heroicons-arrow-path-20-solid', label: 'Загрузка...' }"
      :progress="{ color: 'primary', animation: 'carousel' }"
    >
      <template #role-data="{ row }">
        <span>{{ computeRole(row) }}</span>
      </template>

      <template #groups-data="{ row }">
        <div class="flex items-start flex-wrap gap-1">
          <UBadge
            v-for="item in row.groups as IGroup[]"
            :key="item.id"
            class="flex items-center gap-2"
          >
            <p>{{ item.name }}</p>
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
          <span class="italic text-sm">Нет ни одного сотрудника!</span>
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
import type { IUser } from '~/utils/types/User';
import type { IGroup } from '~/utils/types/Group';
import { USER_ROLES } from '~/utils/constants/Users';
import CreateUser from './modals/CreateUser.vue';
import RemoveUser from './modals/RemoveUser.vue';
import EditUser from './modals/EditUser.vue';

const props = defineProps({
  users: {
    type: Array as () => IUser[],
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const modal = useModal();

const search = ref('');
const page = ref(1);
const pageRowsCount = 10;

const columns = [{
  key: 'last_name',
  label: 'Фамилия',
  sortable: true,
}, {
  key: 'first_name',
  label: 'Имя',
  sortable: true,
}, {
  key: 'middle_name',
  label: 'Отчество',
  sortable: true,
}, {
  key: 'mobile_phone',
  label: 'Телефон',
}, {
  key: 'email',
  label: 'Email',
}, {
  key: 'role',
  label: 'Должность',
  sortable: true,
}, {
  key: 'groups',
  label: 'Группы',
}, {
  key: 'actions',
}];

const items = (row: IUser) => [
  [{
    label: 'Изменить',
    icon: 'i-heroicons-pencil-square-20-solid',
    click: () => modal.open(EditUser, {
      user: row,
      onSuccess() {
        modal.close();
      },
    }),
  }], [{
    label: 'Удалить',
    icon: 'i-heroicons-trash-20-solid',
    iconClass: 'text-red-500',
    click: () => modal.open(RemoveUser, {
      user: row,
      onSuccess() {
        modal.close();
      },
    }),
  }],
];

const computeRole = (row: IUser): string => {
  const findRole = USER_ROLES.find((item) => row.role === item.role);

  if (findRole) {
    return findRole.name;
  }

  return 'нет данных';
};
const tableFilter = computed(() => useTableFilter<IUser>(props.users, search.value, page.value, pageRowsCount));

function addUser() {
  modal.open(CreateUser, {
    onSuccess() {
      modal.close();
    },
  });
}
</script>

<style scoped></style>
