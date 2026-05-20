<template>
  <main>
    <UDivider
      class="mb-4"
      label="Информация о текущей ОКС и объекте (строении)"
    />

    <UTabs
      :items="tabItems"
      class="w-full"
    >
      <template #item="{ item }">
        <UCard>
          <BuildingForm
            v-if="item.key === 'building'"
            readonly
            :info="currentBuilding"
          />

          <ConstructionPartForm
            v-if="item.key === 'constructionPart'"
            readonly
            :info="currentConstructionPart"
          />
        </UCard>
      </template>
    </UTabs>
  </main>
</template>

<script lang="ts" setup>
import BuildingForm from '~/components/objects/form/BuildingForm.vue';
import ConstructionPartForm from '~/components/objects/form/ConstructionPartForm.vue';
import useBuildingStore from '~/store/building';
import useConstructionPartStore from '~/store/building/constructionPart';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});

const buildingStore = useBuildingStore();
const constructionPartStore = useConstructionPartStore();
const currentBuilding = computed(() => buildingStore.getCurrentBuilding);
const currentConstructionPart = computed(() => constructionPartStore.getCurrentConstructionPart);

const tabItems = [{
  key: 'building',
  label: 'Объект капитального строительства (ОКС)',
}, {
  key: 'constructionPart',
  label: 'Объект (строение)',
}];
</script>

<style lang="scss" scoped></style>
