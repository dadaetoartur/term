<template>
  <UDropdown
    :items="items"
    :popper="{ placement: 'bottom' }"
    :ui="{ width: 'w-64' }"
  >
    <UButton
      color="gray"
      label="Панель администратора"
      trailing-icon="i-heroicons-chevron-down-20-solid"
    />
  </UDropdown>
</template>

<script setup lang="ts">
import useBuildingStore from '~/store/building';

const router = useRouter();
const buildingStore = useBuildingStore();
const allBuildings = computed(() => buildingStore.getAllBuildings);

const items = computed(() => [
  [{
    label: 'Группы сотрудников',
    icon: 'i-heroicons-user-group',
    to: '/management/groups',
  }, {
    label: 'Все сотрудники',
    icon: 'i-heroicons-users',
    to: '/management/users',
  }], [{
    label: 'Управление ОКС и объектами',
    icon: 'i-heroicons-adjustments-horizontal',
    disabled: allBuildings.value.length === 0,
    click: () => { router.push('/management/objects'); },
  }],
]);
</script>

<style scoped></style>
