<template>
  <UCard>
    <template #header>
      <h4 class="font-semibold">
        Дополнительные сведения специфичные для линейных объектов
      </h4>
    </template>

    <div class="flex flex-col gap-3">
      <div class="flex flex-col gap-3">
        <UDivider
          :ui="{ label: 'font-semibold' }"
          label="Сведения о категории линейного объекта"
        />

        <UFormGroup
          :ui="{ label: { base: 'font-semibold' } }"
          name="categoryTitle"
          label="Заголовок сведений"
        >
          <UInput
            v-model="stateExtraInfo.objectCategory.title"
            input-class="disabled:cursor-default"
            :variant="props.readonly ? 'none' : 'outline'"
            :padded="!props.readonly"
            :disabled="props.readonly"
            :placeholder="props.readonly ? 'Нет данных' : ''"
          />
        </UFormGroup>

        <UFormGroup
          :ui="{ label: { base: 'font-semibold' } }"
          name="categoryText"
          label="Описание"
        >
          <UTextarea
            v-model="stateExtraInfo.objectCategory.text"
            input-class="disabled:cursor-default"
            :variant="props.readonly ? 'none' : 'outline'"
            :padded="!props.readonly"
            :disabled="props.readonly"
            :placeholder="props.readonly ? 'Нет данных' : ''"
          />
        </UFormGroup>

        <UDivider
          :ui="{ label: 'font-semibold' }"
          label="Сведения о классе линейного объекта"
        />

        <UFormGroup
          :ui="{ label: { base: 'font-semibold' } }"
          name="classTitle"
          label="Заголовок сведений"
        >
          <UInput
            v-model="stateExtraInfo.objectClass.title"
            input-class="disabled:cursor-default"
            :variant="props.readonly ? 'none' : 'outline'"
            :padded="!props.readonly"
            :disabled="props.readonly"
            :placeholder="props.readonly ? 'Нет данных' : ''"
          />
        </UFormGroup>

        <UFormGroup
          :ui="{ label: { base: 'font-semibold' } }"
          name="classText"
          label="Описание"
        >
          <UTextarea
            v-model="stateExtraInfo.objectClass.text"
            input-class="disabled:cursor-default"
            :variant="props.readonly ? 'none' : 'outline'"
            :padded="!props.readonly"
            :disabled="props.readonly"
            :placeholder="props.readonly ? 'Нет данных' : ''"
          />
        </UFormGroup>

        <UDivider
          :ui="{ label: 'font-semibold' }"
          label="Сведения о линейном объекте"
        />

        <UFormGroup
          :ui="{ label: { base: 'font-semibold' } }"
          name="noteTitle"
          label="Заголовок сведений"
        >
          <UInput
            v-model="stateExtraInfo.objectNote.title"
            input-class="disabled:cursor-default"
            :variant="props.readonly ? 'none' : 'outline'"
            :padded="!props.readonly"
            :disabled="props.readonly"
            :placeholder="props.readonly ? 'Нет данных' : ''"
          />
        </UFormGroup>

        <UFormGroup
          :ui="{ label: { base: 'font-semibold' } }"
          name="noteText"
          label="Описание"
        >
          <UTextarea
            v-model="stateExtraInfo.objectNote.text"
            input-class="disabled:cursor-default"
            :variant="props.readonly ? 'none' : 'outline'"
            :padded="!props.readonly"
            :disabled="props.readonly"
            :placeholder="props.readonly ? 'Нет данных' : ''"
          />
        </UFormGroup>
      </div>
    </div>
  </UCard>
</template>

<script setup lang="ts">
import { EMPTY_EXTRA } from '~/utils/constants/Buildings';
import type { IBuildingExtra } from '~/utils/types/Building';

const emits = defineEmits<{ updatedData: [value: IBuildingExtra] }>();

const props = defineProps({
  extraInfo: {
    type: Object as () => IBuildingExtra,
    default: () => ({ ...EMPTY_EXTRA }),
  },
  readonly: {
    type: Boolean,
    default: false,
  },
});

const stateExtraInfo = !props.readonly ? ref<IBuildingExtra>({ ...props.extraInfo }) : computed(() => props.extraInfo);

if (!props.readonly) {
  watch(
    stateExtraInfo.value,
    () => { emits('updatedData', stateExtraInfo.value); },
  );
}
</script>

<style scoped></style>
