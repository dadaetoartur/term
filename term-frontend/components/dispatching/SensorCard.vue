<template>
  <UCard>
    <div class="mb-2">
      <p class="text-center">
        {{ sensorItem.sensor_name }}
      </p>
      <p class="text-center">
        {{ sensorItem.sensor_description }}
      </p>
    </div>

    <USkeleton
      v-if="loadingSensorsData"
      class="h-52 w-full"
    />

    <ClientOnly>
      <Chart
        v-if="!loadingSensorsData"
        ax-y-label="Температура, °C"
        :chart-title="sensorItem.sensor_id"
        :chart-values="sensorDataValues"
      />
    </ClientOnly>
  </UCard>
</template>

<script setup lang="ts">
import { EMPTY_SENSOR } from '~/utils/constants/Buildings';
import type { IBuildingSectionSensorData, IBuildingSectionSensors } from '~/utils/types/Building';
import useSensorsStore from '~/store/building/sensors';
import useConstructionSectionStore from '~/store/building/constructionSection';
import Chart from './Chart.vue';

const props = defineProps({
  sensorItem: {
    type: Object as () => IBuildingSectionSensors,
    default: () => ({ ...EMPTY_SENSOR }),
  },
  dateRange: {
    type: Object as () => { start: Date, end: Date },
    default: () => ({ start: new Date(), end: new Date() }),
  },
});

const toast = useToast();
const sensorsStore = useSensorsStore();
const constructionSectionStore = useConstructionSectionStore();
const currentConstructionSection = computed(() => constructionSectionStore.getCurrentConstructionSection);

const loadingSensorsData = ref(false);
const sensorData = ref<IBuildingSectionSensorData[]>([]);

const sensorDataValues = computed(() => sensorData.value.map((item) => ({ x: new Date(item.time), y: item.value })));

async function updateSensorData(dateRange: { start: Date, end: Date }) {
  loadingSensorsData.value = true;

  try {
    sensorData.value = await sensorsStore.fetchCurrentSensorData(currentConstructionSection.value.id, props.sensorItem.sensor_id, dateRange);
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Не удалось получить данные с датчиков',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }
  loadingSensorsData.value = false;
}

watchEffect(async () => {
  await updateSensorData(props.dateRange);
});
</script>

<style scoped></style>
