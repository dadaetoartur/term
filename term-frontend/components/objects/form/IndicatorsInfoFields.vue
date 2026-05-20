<template>
  <UCard>
    <template #header>
      <h4 class="font-semibold">
        {{ title }}
      </h4>
    </template>

    <div class="flex flex-col gap-3">
      <p
        v-if="stateIndicators.length === 0"
        class="italic text-gray-500 text-center"
      >
        Отсутствуют индикаторы и их показатели
      </p>
      <div
        v-for="(indicator, index) of stateIndicators"
        :key="index"
        class="grid grid-cols-12 gap-3 items-end"
      >
        <UFormGroup
          :ui="{ label: { base: 'font-semibold' } }"
          class="col-span-8"
          name="name"
          label="Наименование показателя"
        >
          <UInput
            v-model="indicator.name"
            input-class="disabled:cursor-default"
            :variant="props.readonly ? 'none' : 'outline'"
            :padded="!props.readonly"
            :disabled="props.readonly"
            :placeholder="props.readonly ? 'Нет данных' : 'Пример: Площадь застройки'"
          />
        </UFormGroup>

        <UFormGroup
          :ui="{ label: { base: 'font-semibold' } }"
          class="col-span-3"
          name="value"
          label="Значение показателя"
        >
          <UInput
            v-model="indicator.value"
            input-class="disabled:cursor-default"
            :variant="props.readonly ? 'none' : 'outline'"
            :padded="!props.readonly"
            :disabled="props.readonly"
            :placeholder="props.readonly ? 'Нет данных' : 'Пример: 6340,38'"
          />
        </UFormGroup>

        <UButton
          v-if="!props.readonly"
          size="sm"
          class="flex justify-center text-center"
          color="red"
          @click="removeIndicator(index)"
        >
          Удалить
        </UButton>
      </div>
    </div>

    <template
      v-if="!props.readonly"
      #footer
    >
      <div class="flex justify-center">
        <UButton
          size="sm"
          class="flex justify-center text-center"
          color="primary"
          @click="addIndicator"
        >
          Добавить показатель
        </UButton>
      </div>
    </template>
  </UCard>
</template>

<script setup lang="ts">
import { EMPTY_INDICATOR } from '~/utils/constants/Buildings';
import type { IBuildingIndicator } from '~/utils/types/Building';

const emits = defineEmits<{ updatedData: [value: IBuildingIndicator[]] }>();

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  indicators: {
    type: Array as () => IBuildingIndicator[],
    default: () => [{ ...EMPTY_INDICATOR }],
  },
  readonly: {
    type: Boolean,
    default: false,
  },
});

const stateIndicators = !props.readonly ? ref<IBuildingIndicator[]>([...props.indicators]) : computed(() => props.indicators);

if (!props.readonly) {
  watch(
    stateIndicators.value,
    () => { emits('updatedData', stateIndicators.value); },
  );
}

const addIndicator = () => stateIndicators.value.push({ name: '', value: '', measure: '' });
const removeIndicator = (index: number) => stateIndicators.value.splice(index, 1);
</script>

<style scoped></style>
