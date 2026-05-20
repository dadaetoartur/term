<template>
  <main class="flex flex-col gap-3">
    <UDivider label="Диспетчеризация" />

    <UCard :ui="{ body: { base: 'flex flex-col gap-3' } }">
      <div class="grid grid-cols-3 gap-3">
        <InfoCard
          icon="i-heroicons-building-office"
          name="Количество объектов (строений)"
          :value="currentBuilding.id ? currentBuilding.constructionParts.length : 0"
        />
        <InfoCard
          icon="i-heroicons-arrow-trending-up"
          name="Задач в работе"
          value="0"
        />
        <InfoCard
          icon="i-heroicons-briefcase"
          name="Загрузка сотрудников"
          value="0%"
        />
      </div>
    </UCard>

    <UCard>
      <Dispatching />
    </UCard>
  </main>
</template>

<script lang="ts" setup>
import InfoCard from '~/components/dispatching/InfoCard.vue';
import useBuildingStore from '~/store/building';
import Dispatching from '~/components/dispatching/Dispatching.vue';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});

const buildingStore = useBuildingStore();
const currentBuilding = computed(() => buildingStore.currentBuilding);
</script>

<style lang="scss" scoped></style>
