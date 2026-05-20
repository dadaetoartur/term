<template>
  <div class="flex w-full gap-14 justify-between">
    <div class="flex w-full flex-col gap-3">
      <h3 class="text-lg mb-3">
        Введите вручную информацию об объекте для его добавления к текущему ОКС - <UBadge variant="soft">
          {{ buildingName }}
        </UBadge>
      </h3>

      <ConstructionPartForm @updated-data="emits('updatedData', $event)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { IBuildingConstructionPart } from '~/utils/types/Building';
import ConstructionPartForm from '../form/ConstructionPartForm.vue';

defineProps<{
  buildingName: string
}>();

const emits = defineEmits<{ updatedData: [value: IBuildingConstructionPart] }>();
</script>

<style scoped></style>
