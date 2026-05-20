<template>
  <div class="flex w-full flex-col gap-3">
    <div class="grid grid-cols-3 gap-3 items-end">
      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="id"
        label="Идентификатор объекта (строения)"
      >
        <UInput
          v-model="stateInfo.objectId"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: OBJ_28'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        class="col-span-2"
        name="name"
        label="Наименование объекта (строения), входящего в состав ОКС"
      >
        <UInput
          v-model="stateInfo.name"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: Котельная'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="energyEfficiency"
        label="Сведения о классе энергетической эффективности и о повышении энергетической эффективности"
      >
        <UInput
          v-model="stateInfo.energyEfficiency"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: А'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="fireDangerCategory"
        label="Категория пожарной и взрывопожарной опасности"
      >
        <UInput
          v-model="stateInfo.fireDangerCategory"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: Б'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="responsibilityLevel"
        label="Уровень ответственности"
      >
        <UInput
          v-model="stateInfo.responsibilityLevel"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: нормальный'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        class="col-span-3"
        name="peoplePermanentStay"
        label="Сведения о наличии помещений с постоянным пребыванием людей"
      >
        <UInput
          v-model="stateInfo.peoplePermanentStay"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: Помещения с постоянным пребыванием людей отсутсвуют'"
        />
      </UFormGroup>
    </div>

    <AddressInfoFields
      :readonly="props.readonly"
      :address="info.address ? info.address : { ...EMPTY_ADDRESS }"
      title="Адрес (местоположение) объекта (строения)"
      @updated-data="stateInfo.address = $event"
    />

    <IndicatorsInfoFields
      :readonly="props.readonly"
      :indicators="info.technicalIndicators ? info.technicalIndicators : [{ ...EMPTY_INDICATOR }]"
      title="Технико-экономические показатели объекта (строения)"
      @updated-data="stateInfo.technicalIndicators = $event"
    />

    <IndicatorsInfoFields
      :readonly="props.readonly"
      :indicators="info.powerIndicators ? info.powerIndicators : [{ ...EMPTY_INDICATOR }]"
      title="Данные о проектной мощности объекта (строения)"
      @updated-data="stateInfo.powerIndicators = $event"
    />
  </div>
</template>

<script setup lang="ts">
import { EMPTY_ADDRESS, EMPTY_CONSTRUCTION_PART, EMPTY_INDICATOR } from '~/utils/constants/Buildings';
import type { IBuildingConstructionPart } from '~/utils/types/Building';
import AddressInfoFields from './AddressInfoFields.vue';
import IndicatorsInfoFields from './IndicatorsInfoFields.vue';

const props = defineProps({
  info: {
    type: Object as () => IBuildingConstructionPart,
    default: () => ({ ...EMPTY_CONSTRUCTION_PART }),
  },
  readonly: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits<{ updatedData: [value: IBuildingConstructionPart] }>();

const stateInfo = !props.readonly ? ref<IBuildingConstructionPart>({ ...props.info }) : computed(() => props.info);

if (!props.readonly) {
  watch(
    stateInfo.value,
    () => { emits('updatedData', stateInfo.value); },
  );
}
</script>

<style scoped></style>
