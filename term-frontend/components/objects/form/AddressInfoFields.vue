<template>
  <UCard>
    <template #header>
      <h4 class="font-semibold">
        {{ title }}
      </h4>
    </template>

    <div class="grid grid-cols-3 gap-3 items-end">
      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        class="col-span-2"
        name="country"
        label="Страна"
      >
        <UInput
          v-model="stateAddress.country"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: Российская Федерация'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="region"
        label="Код субъекта Российской Федерации"
      >
        <UInput
          v-model="stateAddress.region"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: 47'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="district"
        label="Наименование района"
      >
        <UInput
          v-model="stateAddress.district"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: Всеволожский муниципальный район'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="city"
        label="Город"
      >
        <UInput
          v-model="stateAddress.city"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: д. Новое Девяткино'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="city"
        label="Населенный пункт"
      >
        <UInput
          v-model="stateAddress.settlement"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: Новодевяткинское сельское поселение'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="street"
        label="Улица"
      >
        <UInput
          v-model="stateAddress.street"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: Пушкина'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="building"
        label="Номер здания/сооружения"
      >
        <UInput
          v-model="stateAddress.building"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: 123'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        name="room"
        label="Номер помещения"
      >
        <UInput
          v-model="stateAddress.room"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
          :placeholder="props.readonly ? 'Нет данных' : 'Пример: 45'"
        />
      </UFormGroup>

      <UFormGroup
        :ui="{ label: { base: 'font-semibold' } }"
        class="col-span-3"
        name="note"
        label="Неформализованное описание адреса"
      >
        <UInput
          v-model="stateAddress.note"
          input-class="disabled:cursor-default"
          :variant="props.readonly ? 'none' : 'outline'"
          :padded="!props.readonly"
          :disabled="props.readonly"
        />
      </UFormGroup>
    </div>
  </UCard>
</template>

<script setup lang="ts">
import { EMPTY_ADDRESS } from '~/utils/constants/Buildings';
import type { IBuildingAddress } from '~/utils/types/Building';

const emits = defineEmits<{ updatedData: [value: IBuildingAddress] }>();

const props = defineProps({
  title: {
    type: String,
    default: 'Заголовок',
  },
  address: {
    type: Object as () => IBuildingAddress,
    default: () => ({ ...EMPTY_ADDRESS }),
  },
  readonly: {
    type: Boolean,
    default: false,
  },
});

const stateAddress = !props.readonly ? ref<IBuildingAddress>({ ...props.address }) : computed(() => props.address);

if (!props.readonly) {
  watch(
    stateAddress.value,
    () => { emits('updatedData', stateAddress.value); },
  );
}
</script>

<style scoped></style>
