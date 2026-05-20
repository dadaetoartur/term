<template>
  <div class="flex flex-col gap-3">
    <h4 class="text-center italic">
      Мониторинг датчиков с оборудования по инженерным секциям
    </h4>

    <div class="grid grid-cols-2 gap-3 items-center">
      <div class="flex gap-3 justify-between items-center">
        <SectionsSwitcher
          :sensors-view="true"
          @change-section="fetchAllSensors"
        />

        <UBadge
          variant="soft"
          class="flex gap-2 px-5 py-2.5"
        >
          <ClientOnly>
            <UToggle
              v-model="sensorState"
              :disabled="disabledSensorToggle || !currentConstructionSection.id"
            />
          </ClientOnly>
          <p>Прием данных с сенсора</p>
        </UBadge>
      </div>

      <div class="flex items-center gap-1 justify-self-end">
        <ClientOnly>
          <DateRangePicker
            :disabled="disabledSensorToggle || !currentConstructionSection.id || !sensorState"
            @change-date="currentDateRange = $event"
          />
        </ClientOnly>
      </div>
    </div>

    <UCard
      v-if="sensorState"
      :ui="{ body: { base: 'flex items-center justify-center gap-3' } }"
    >
      <UIcon
        class="text-3xl cursor-pointer text-yellow-500"
        name="i-heroicons-information-circle"
      />

      <p>
        Используйте ID данной инженерной секции <UBadge variant="soft">
          {{ currentConstructionSection.id }}
        </UBadge> для подключения к ней датчиков
      </p>
    </UCard>

    <div class="grid grid-cols-2 gap-3">
      <SensorCard
        v-for="(item, index) in currentSensors"
        :key="index"
        :sensor-item="item"
        :date-range="currentDateRange"
      />

      <UCard
        v-if="!loadingSensors && !sensorState"
        class="col-span-2"
        :ui="{ body: { base: 'flex justify-center gap-3' } }"
      >
        <p class="italic">
          Данная инженерная секция не активирована для приема данных с датчиков
        </p>
      </UCard>

      <div
        v-if="loadingSensors"
        class="col-span-2 grid grid-cols-2 gap-3"
      >
        <USkeleton class="h-52 w-full" />
        <USkeleton class="h-52 w-full" />
        <USkeleton class="h-52 w-full" />
        <USkeleton class="h-52 w-full" />
      </div>

      <UCard
        v-if="!loadingSensors && sensorState && currentSensors.length === 0"
        class="col-span-2"
        :ui="{ body: { base: 'flex justify-center gap-3' } }"
      >
        <p class="italic">
          Для данной инженерной секции отсутствуют подключенные датчики. Используйте информацию выше.
        </p>
      </UCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import useConstructionPartStore from '~/store/building/constructionPart';
import useConstructionSectionStore from '~/store/building/constructionSection';
import useSensorsStore from '~/store/building/sensors';
import SectionsSwitcher from '../management/SectionsSwitcher.vue';
import SensorCard from './SensorCard.vue';
import DateRangePicker from './calendar/DateRangePicker.vue';

const toast = useToast();
const constructionPartStore = useConstructionPartStore();
const constructionSectionStore = useConstructionSectionStore();
const sensorsStore = useSensorsStore();
const currentConstructionPart = computed(() => constructionPartStore.getCurrentConstructionPart);
const currentConstructionSection = computed(() => constructionSectionStore.getCurrentConstructionSection);
const currentSensors = computed(() => sensorsStore.getAllSensors);

const currentDateRange = ref({ start: new Date(), end: new Date() });
const disabledSensorToggle = ref(false);
const loadingSensors = ref(false);

const fetchAllSensors = async () => {
  loadingSensors.value = true;

  if (currentConstructionSection.value.hasSensor) {
    try {
      await sensorsStore.fetchConstructionSectionSensors(currentConstructionSection.value.id);
    } catch (error) {
      toast.add({
        title: 'Ошибка',
        description: 'Нет датчиков для этой секции',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  } else {
    sensorsStore.setAllSensors([]);
  }

  loadingSensors.value = false;
};

const sensorState = computed({
  get: () => currentConstructionSection.value.hasSensor,
  set: async (val) => {
    disabledSensorToggle.value = true;

    try {
      await constructionSectionStore.updateConstructionSection(currentConstructionSection.value.id, { hasSensor: val });
      await constructionPartStore.fetchCurrentConstructionPartInfo(currentConstructionPart.value.id);
      await fetchAllSensors();
    } catch (error) {
      toast.add({
        title: 'Ошибка',
        description: 'Невозможно изменить состояние приема данных с сенсора, попробуйте позже',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }

    disabledSensorToggle.value = false;
  },
});

onMounted(async () => {
  await fetchAllSensors();
});
</script>

<style scoped></style>
