<template>
  <div class="flex w-full gap-14 justify-between">
    <div class="flex w-full flex-col gap-3">
      <h3 class="text-lg mb-3">
        Введите информацию об объекте капитального строительства (ОКС) вручную
      </h3>

      <BuildingForm @updated-data="emits('loadManualInfo', $event)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { IBuilding } from '~/utils/types/Building';
import BuildingForm from '../form/BuildingForm.vue';

const emits = defineEmits<{ loadManualInfo: [value: IBuilding] }>();
</script>

<style scoped></style>
