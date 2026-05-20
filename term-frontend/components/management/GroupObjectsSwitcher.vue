<template>
  <UDropdown
    :items="items"
    :popper="{ placement: 'bottom' }"
    :ui="{ width: 'w-72' }"
  >
    <UButton
      color="gray"
      :label="props.title"
      trailing-icon="i-heroicons-chevron-down-20-solid"
    />

    <template #item="{ item }">
      <span class="truncate">{{ item.label }}</span>

      <UIcon
        v-if="item.icon"
        :name="item.icon"
        class="flex-shrink-0 h-4 w-4 text-gray-400 dark:text-gray-500 ms-auto"
      />
    </template>
  </UDropdown>
</template>

<script setup lang="ts">
import type { DropdownItem } from '#ui/types';
import useBuildingStore from '~/store/building';

const props = defineProps({
  title: {
    type: String,
    default: 'Объекты капитального строительства (ОКС)',
  },
  managementBtn: {
    type: Boolean,
    default: true,
  },
});

const router = useRouter();
const buildingStore = useBuildingStore();
const allBuildings = computed(() => buildingStore.getAllBuildings);
const currentBuilding = computed(() => buildingStore.currentBuilding);

const items = computed(() => {
  const tempObjects: DropdownItem[] = [];

  if (allBuildings.value.length > 0) {
    for (const iterator of allBuildings.value) {
      tempObjects.push({
        label: iterator.name,
        icon: currentBuilding.value.id === iterator.id ? 'i-heroicons-check' : '',
        click: () => {
          buildingStore.setCurrentBuilding(iterator);
        },
      });
    }
  } else {
    tempObjects.push({
      label: 'Нет существующих ОКС',
      disabled: true,
      class: 'italic',
    });
  }

  if (props.managementBtn) {
    return [tempObjects, [{
      label: 'Создать ОКС',
      icon: 'i-heroicons-plus',
      click: () => { router.push('/management/objects/create?step=1'); },
    }]];
  }

  return [tempObjects];
});
</script>

<style scoped></style>
