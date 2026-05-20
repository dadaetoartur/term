<template>
  <div class="flex flex-col gap-3">
    <UFormGroup
      :ui="{ label: { base: 'font-semibold' } }"
      class="col-span-3"
      name="name"
      label="Наименование объекта капитального строительства"
    >
      <UInput
        v-model="stateInfo.name"
        input-class="disabled:cursor-default"
        :variant="props.readonly ? 'none' : 'outline'"
        :padded="!props.readonly"
        :disabled="props.readonly"
        :placeholder="props.readonly ? 'Нет данных' : ''"
      />
    </UFormGroup>

    <div class="grid grid-cols-3 gap-3 items-end">
      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        class="col-span-2"
        name="constructionType"
        label="Вид работ, на который разрабатывается проектная документация"
      >
        <USelectMenu
          v-model="constructionSelected"
          select-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :options="constructionTypes"
          :trailing-icon="props.readonly ? '' : 'i-heroicons-chevron-down-20-solid'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="constructionDuration"
        label="Продолжительность работ (месяцев)"
      >
        <UInput
          v-model="stateInfo.constructionDuration"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
        />
      </UFormGroup>
    </div>

    <AddressInfoFields
      :readonly="props.readonly"
      :address="info.address ? info.address : { ...EMPTY_ADDRESS }"
      title="Адрес (местоположение) объекта капитального строительства"
      @updated-data="stateInfo.address = $event"
    />

    <IndicatorsInfoFields
      :readonly="props.readonly"
      :indicators="info.technicalIndicators ? info.technicalIndicators : [{ ...EMPTY_INDICATOR }]"
      title="Технико-экономические показатели проектируемого объекта капитального строительства"
      @updated-data="stateInfo.technicalIndicators = $event"
    />

    <IndicatorsInfoFields
      :readonly="props.readonly"
      :indicators="info.powerIndicators ? info.powerIndicators : [{ ...EMPTY_INDICATOR }]"
      title="Данные о проектной мощности объекта капитального строительства"
      @updated-data="stateInfo.powerIndicators = $event"
    />

    <ClientOnly>
      <ExtraInfoFields
        :readonly="props.readonly"
        :extra-info="info.extra ? info.extra : { ...EMPTY_EXTRA }"
        @updated-data="stateInfo.extra = $event"
      />
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import type { IBuilding } from '~/utils/types/Building';
import {
  EMPTY_ADDRESS, EMPTY_BUILDING, EMPTY_EXTRA, EMPTY_INDICATOR,
} from '~/utils/constants/Buildings';
import AddressInfoFields from './AddressInfoFields.vue';
import IndicatorsInfoFields from './IndicatorsInfoFields.vue';
import ExtraInfoFields from './ExtraInfoFields.vue';

const emits = defineEmits<{ updatedData: [value: IBuilding] }>();

const props = defineProps({
  info: {
    type: Object as () => IBuilding,
    default: () => ({ ...EMPTY_BUILDING }),
  },
  readonly: {
    type: Boolean,
    default: false,
  },
});

const constructionTypes = ['Эксплуатация', 'Строительство', 'Реконструкция', 'Капитальный ремонт', 'Снос', 'Сохранение объекта культурного наследия'];
const constructionSelected = ref(constructionTypes[0]);

const stateInfo = !props.readonly ? ref<IBuilding>({ ...props.info }) : computed(() => props.info);

watchEffect(() => { stateInfo.value.constructionType = constructionTypes.indexOf(constructionSelected.value) + 1; });

if (!props.readonly) {
  watch(
    stateInfo.value,
    () => { emits('updatedData', stateInfo.value); },
  );
}
</script>

<style scoped></style>
