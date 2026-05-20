<template>
  <UDropdown
    :items="items"
    :popper="{ placement: 'bottom' }"
    :ui="{ width: 'w-60' }"
  >
    <UButton
      color="gray"
      label="Объекты (строения)"
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
import useConstructionPartStore from '~/store/building/constructionPart';

const router = useRouter();
const buildingsStore = useBuildingStore();
const constructionPartStore = useConstructionPartStore();
const currentBuilding = computed(() => buildingsStore.getCurrentBuilding);
const currentConstructionPart = computed(() => constructionPartStore.getCurrentConstructionPart);

const items = computed(() => {
  const tempLastObjects: DropdownItem[] = [];

  if (currentBuilding.value.constructionParts.length > 0) {
    for (const iterator of currentBuilding.value.constructionParts) {
      tempLastObjects.push({
        label: iterator.name,
        icon: currentConstructionPart.value.id === iterator.id ? 'i-heroicons-check' : '',
        click: () => {
          constructionPartStore.setCurrentConstructionPart(iterator);
        },
      });
    }
  } else {
    tempLastObjects.push({
      label: 'Нет существующих объектов',
      disabled: true,
      class: 'italic',
    });
  }

  const tempObjects: DropdownItem[][] = [
    tempLastObjects, [{
      label: 'Добавить объект (строение)',
      icon: 'i-heroicons-plus',
      click: () => { router.push('/management/objects/create?step=2'); },
    }],
  ];

  return tempObjects;
});
</script>

<style scoped></style>
