<template>
  <UDropdown
    class="flex-1"
    :items="items"
    :popper="{ placement: 'bottom' }"
    :ui="{ width: 'w-96', height: 'max-h-72' }"
  >
    <UButton
      v-if="sections.length === 0"
      truncate
      class="w-full flex justify-between"
      disabled
      color="gray"
      label="Нет инженерных систем"
    />

    <UTooltip
      v-if="sections.length > 0"
      :ui="{ base: 'whitespace-normal overflow-visible h-full text-clip', width: 'max-w-full' }"
      class="w-full"
      :text="currentSection.name"
    >
      <UButton
        truncate
        class="w-full flex justify-between"
        :disabled="disabled"
        color="gray"
        :label="currentSection.name"
        trailing-icon="i-heroicons-chevron-down-20-solid"
      />
    </UTooltip>

    <template #item="{ item }">
      <div class="truncate flex items-center gap-1">
        <span
          class="h-2 w-2 rounded-full flex-shrink-0 mt-0.5 border"
          :class="item.labelClass"
        />

        <p class="truncate text-sm">
          {{ item.label }}
        </p>
      </div>

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
import useConstructionPartStore from '~/store/building/constructionPart';
import useConstructionSectionStore from '~/store/building/constructionSection';
import type { IBuildingConstructionSection } from '~/utils/types/Building';

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false,
  },
  sensorsView: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits<{
  changeSection: [value: IBuildingConstructionSection],
}>();

const constructionPartStore = useConstructionPartStore();
const constructionSectionStore = useConstructionSectionStore();
const sections = computed(() => constructionPartStore.getCurrentConstructionPart.sections);
const currentSection = computed(() => constructionSectionStore.getCurrentConstructionSection);

const items = computed(() => {
  const tempObjects: DropdownItem[] = [];

  for (const iterator of sections.value) {
    let labelClass: string = '';

    if (props.sensorsView) {
      labelClass = iterator.hasSensor
        ? 'bg-green-500 dark:bg-green-400 border-green-500 dark:border-green-400'
        : 'bg-white-500 dark:bg-white-400 border-gray-300 dark:border-gray-500';
    } else {
      labelClass = iterator.bimArtifacts.length === 2
        ? 'bg-green-500 dark:bg-green-400 border-green-500 dark:border-green-400'
        : 'bg-white-500 dark:bg-white-400 border-gray-300 dark:border-gray-500';
    }

    tempObjects.push({
      label: iterator.name,
      labelClass,
      icon: currentSection.value.id === iterator.id ? 'i-heroicons-check' : '',
      click: async () => {
        constructionSectionStore.setCurrentConstructionSection(iterator);
        emits('changeSection', iterator);
      },
    });
  }

  return [tempObjects];
});
</script>

<style scoped></style>
