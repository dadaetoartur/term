<template>
  <UPopover :popper="{ placement: 'bottom-start' }">
    <UButton
      :disabled="props.disabled"
      color="primary"
      icon="i-heroicons-calendar-days-20-solid"
    >
      {{ format(selected.start, 'd MMM, yyy', { locale: ru }) }} - {{ format(selected.end, 'd MMM, yyy', { locale: ru })
      }}
    </UButton>

    <template #panel="{ close }">
      <div class="flex items-center sm:divide-x divide-gray-200 dark:divide-gray-800">
        <div class="hidden sm:flex flex-col py-4">
          <UButton
            v-for="(range, index) in ranges"
            :key="index"
            :label="range.label"
            color="gray"
            variant="ghost"
            class="rounded-none px-6"
            :class="[isRangeSelected(range.duration) ? 'bg-gray-100 dark:bg-gray-800' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50']"
            truncate
            @click="selectRange(range.duration)"
          />
        </div>

        <DatePicker
          v-model="selected"
          @change-date="emits('changeDate', $event);"
          @close="close"
        />
      </div>
    </template>
  </UPopover>
</template>

<script setup lang="ts">
import {
  sub, format, isSameDay, type Duration,
} from 'date-fns';
import { ru } from 'date-fns/locale';
import DatePicker from './DatePicker.vue';

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits<{
  changeDate: [value: { start: Date, end: Date }],
}>();

const ranges = [
  { label: 'Последние сутки', duration: { days: 1 } },
  { label: 'Последние 7 дней', duration: { days: 7 } },
  { label: 'Последние 14 дней', duration: { days: 14 } },
  { label: 'Последние 30 дней', duration: { days: 30 } },
];

const selected = ref({ start: sub(new Date(), { days: 1 }), end: new Date() });
emits('changeDate', selected.value);

function isRangeSelected(duration: Duration) {
  return isSameDay(selected.value.start, sub(new Date(), duration)) && isSameDay(selected.value.end, new Date());
}

function selectRange(duration: Duration) {
  selected.value = { start: sub(new Date(), duration), end: new Date() };
  emits('changeDate', selected.value);
}
</script>

<style scoped></style>
