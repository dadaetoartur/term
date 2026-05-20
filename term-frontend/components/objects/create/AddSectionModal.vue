<template>
  <UModal>
    <UCard>
      <template #header>
        <h2 class="text-xl text-center">
          Добавление инженерной системы
        </h2>
      </template>

      <UForm
        :schema="schema"
        :state="state"
        class="space-y-4 flex flex-col"
        @submit="onSubmit"
        @error="onError"
      >
        <div class="flex flex-col gap-3">
          <UFormGroup
            v-slot="{ error }"
            name="name"
            label="Наименование инженерной системы"
          >
            <UInputMenu
              v-model="state.name"
              v-model:query="state.name"
              :options="systems"
              placeholder="Инженерные системы"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : 'i-heroicons-cog-6-tooth'"
            >
              <template #option-empty="{ query }">
                <q>{{ query }}</q> не найден. Нажмите <UKbd>Enter</UKbd>, чтобы оставить эту инженерную систему.
              </template>
            </UInputMenu>
          </UFormGroup>

          <UFormGroup
            v-slot="{ error }"
            name="description"
            label="Описание инженерной системы"
          >
            <UInput
              v-model="state.description"
              :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined"
            />
          </UFormGroup>
        </div>

        <div class="self-center flex justify-center gap-3">
          <UButton
            :loading="loading"
            type="submit"
            class="px-8"
          >
            Создать
          </UButton>

          <UButton
            variant="outline"
            class="px-8"
            @click="emit('close')"
          >
            Отменить
          </UButton>
        </div>
      </UForm>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
import { z } from 'zod';
import type { FormErrorEvent, FormSubmitEvent } from '#ui/types';
import type { IBuildingConstructionPart, IBuildingConstructionSection } from '~/utils/types/Building';
import { EMPTY_CONSTRUCTION_PART, EMPTY_CONSTRUCTION_SECTION } from '~/utils/constants/Buildings';
import useConstructionSectionStore from '~/store/building/constructionSection';

const props = defineProps({
  constructionPart: {
    type: Object as () => IBuildingConstructionPart,
    default: () => ({ ...EMPTY_CONSTRUCTION_PART }),
  },
});

const emit = defineEmits(['success', 'close']);

const toast = useToast();
const constructionSectionStore = useConstructionSectionStore();

const loading = ref(false);
const systems = [
  'Архитектурные решения (АР)',
  'Конструктивные решения (КР)',
  'Вентиляция',
  'Кондиционирование',
  'Холодоснабжение',
  'Водоснабжение',
  'Водоотведение/Канализация',
  'Отопление',
  'Тепломеханические решения',
  'Сети связи (СС)',
  'Электрическое освещение и силовое электрооборудование (ЭОМ)',
  'Пожаротушение',
  'Другое',
];
const state = ref<IBuildingConstructionSection>({ ...EMPTY_CONSTRUCTION_SECTION });

const schema = z.object({
  name: z.string({ message: 'Обязательное поле' }).min(2, {
    message: 'Название должно быть не короче 2 символов',
  }),
  description: z.string({ message: 'Обязательное поле' }).min(2, {
    message: 'Описание должно быть не короче 2 символов',
  }),
});

type Schema = z.infer<typeof schema>

async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true;

  try {
    await constructionSectionStore.createConstructionSection(props.constructionPart.id, event.data);

    toast.add({
      title: 'Готово',
      description: 'Инженерная система успешно создана',
      icon: 'i-heroicons-check-circle',
      color: 'green',
    });

    emit('success');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Невозможно создать инженерную систему, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id);
  element?.focus();
  element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
</script>

<style scoped></style>
