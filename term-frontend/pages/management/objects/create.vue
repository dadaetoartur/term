<template>
  <main>
    <UDivider
      class="mb-4"
      label="Добавление здания и инженерной системы"
    />

    <UCard>
      <template #header>
        <UProgress
          :value="step"
          :max="[
            'Выбор способа добавления информации',
            'Добавление информации об объекте капитального строительства',
            'Добавление информации о строении (объекте) ',
            'Управление инженерными системами и BIM-моделями',
            'Готово']"
        />
      </template>

      <div
        v-if="step == 0"
        class="flex flex-col gap-4"
      >
        <ClientOnly>
          <URadioGroup
            v-model="radioSelected"
            :ui="{ fieldset: 'p-0' }"
            legend="Выберите способ загрузки информации об объекте капитального строительства"
            :options="radioOptions"
          >
            <template #label="{ option }">
              <p class="flex items-center gap-1 text-md italic">
                <UIcon :name="option.icon" />
                {{ option.label }}
              </p>
            </template>
          </URadioGroup>
        </ClientOnly>

        <StepInfoAboutXml
          v-if="radioSelected === 'xml'"
          @load-xml-file="xmlFormData = $event"
        />

        <p
          v-if="radioSelected === 'manualOKS'"
          class="text-base"
        >
          Нажмите кнопку <UBadge variant="soft">
            далее
          </UBadge> для создания нового объекта капитального строительства (ОКС)
        </p>

        <p
          v-if="radioSelected === 'manualObject'"
          class="text-base"
        >
          Нажмите кнопку <UBadge variant="soft">
            далее
          </UBadge> для добавления нового объекта к текущему ОКС - <UBadge variant="soft">
            {{ currentBuilding.name }}
          </UBadge>
        </p>

        <p
          v-if="radioSelected === 'bimModel'"
          class="text-base"
        >
          Нажмите кнопку <UBadge variant="soft">
            далее
          </UBadge> для добавления или удаления инженерной системы и BIM-модели текущего объекта (строения) - <UBadge
            variant="soft"
          >
            {{ currentConstructionPart.name }}
          </UBadge>
        </p>
      </div>

      <StepInfoAboutOKSManual
        v-if="step == 1"
        @load-manual-info="manualOKSInfo = $event"
      />

      <StepInfoAboutObjectManual
        v-if="step == 2"
        :building-name="currentBuilding.name"
        @updated-data="manualObjectInfo = $event"
      />

      <div v-if="step == 3">
        <p class="mb-3">
          BIM-модель для ОКС:
          <UBadge variant="soft">
            {{ currentBuilding.name }}
          </UBadge> - объекта:
          <UBadge variant="soft">
            {{ currentConstructionPart.name }}
          </UBadge>
        </p>

        <ClientOnly>
          <StepInfoLoadModel
            @model-loaded="modeLoaded = $event"
            @model-fragments-file="modelFragmentsFile = $event"
            @model-properties-file="modelPropertiesFile = $event"
          />
        </ClientOnly>
      </div>

      <div
        v-if="step == 4"
        class="flex flex-col justify-center items-center gap-7"
      >
        <h3 class="text-xl">
          Все готово!
        </h3>
        <NuxtLink to="/management">
          <UButton color="primary">
            Вернуться на главную
          </UButton>
        </NuxtLink>
      </div>

      <template #footer>
        <div class="w-full flex justify-between">
          <ClientOnly>
            <UButton
              color="gray"
              :loading="loading"
              :disabled="step === 0
                || (step !== 1 && radioSelected === 'manualOKS')
                || (step !== 2 && radioSelected === 'manualObject')
                || (step !== 3 && radioSelected === 'bimModel')
                || step === 4"
              @click.prevent="step = 0, router.replace({ query: undefined })"
            >
              <UIcon
                name="i-heroicons-arrow-left"
                class="w-5 h-5"
              />
              Назад
            </UButton>

            <UButton
              v-if="step !== 4"
              label="Далее"
              :loading="loading"
              :disabled="step > 4
                || (step === 0 && ((radioSelected === 'xml' && !xmlFormData.has('file'))))
                || (step === 1 && Object.keys(manualOKSInfo).length === 0)
                || (step === 3 && (!modeLoaded || !currentConstructionSection.id))
                || step === 4"
              @click.prevent="increaseStep"
            >
              <template #trailing>
                <UIcon
                  name="i-heroicons-arrow-right"
                  class="w-5 h-5"
                />
              </template>
            </UButton>

            <NuxtLink
              v-if="step === 4"
              to="/management"
            >
              <UButton label="Готово" />
            </NuxtLink>
          </ClientOnly>
        </div>
      </template>
    </UCard>
  </main>
</template>

<script setup lang="ts">
import StepInfoAboutOKSManual from '~/components/objects/create/StepInfoAboutOKSManual.vue';
import StepInfoAboutXml from '~/components/objects/create/StepInfoAboutXml.vue';
import StepInfoLoadModel from '~/components/objects/create/StepInfoLoadModel.vue';
import type { IBuilding, IBuildingConstructionPart } from '~/utils/types/Building';
import useBuildingStore from '~/store/building';
import StepInfoAboutObjectManual from '~/components/objects/create/StepInfoAboutObjectManual.vue';
import useConstructionPartStore from '~/store/building/constructionPart';
import useConstructionSectionStore from '~/store/building/constructionSection';
import { removeModelFromSection } from '~/utils/artifacts';
import useBimArtifactsStore from '~/store/building/bimArtifacts';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});

const step = ref(0);
const buildingStore = useBuildingStore();
const constructionPartStore = useConstructionPartStore();
const constructioSectionStore = useConstructionSectionStore();
const bimArtifactsStore = useBimArtifactsStore();
const toast = useToast();
const route = useRoute();
const router = useRouter();
const currentBuilding = computed(() => buildingStore.getCurrentBuilding);
const currentConstructionPart = computed(() => constructionPartStore.getCurrentConstructionPart);
const currentConstructionSection = computed(() => constructioSectionStore.getCurrentConstructionSection);

const radioOptions = computed(() => [
  { value: 'xml', label: 'XML-файл пояснительная записка (Раздел 1 проектной документации)', icon: 'i-heroicons-document-arrow-up' },
  { value: 'manualOKS', label: 'Создать новый объект капитального строительства (ОКС)', icon: 'i-heroicons-building-office-2' },
  {
    value: 'manualObject', label: 'Добавить объект к текущему ОКС', icon: 'i-heroicons-plus', disabled: !currentBuilding.value.id,
  },
  {
    value: 'bimModel', label: 'Управление инженерными системами и BIM-моделями текущего объекта (строения)', icon: 'i-heroicons-cube', disabled: !currentConstructionPart.value.id,
  },
]);

const radioSelected = ref('xml');
const xmlFormData = ref<FormData>(new FormData());
const modelFragmentsFile = ref<FormData>();
const modelPropertiesFile = ref<FormData>();
const manualOKSInfo = ref<Partial<IBuilding>>({});
const manualObjectInfo = ref<Partial<IBuildingConstructionPart>>({});

const modeLoaded = ref(false);
const loading = ref(false);

async function increaseStep() {
  loading.value = true;

  if (step.value === 0) {
    if (xmlFormData.value.has('file') && radioSelected.value === 'xml') {
      try {
        await buildingStore.createBuildingInfoXml(xmlFormData.value);
        router.replace({ query: { step: 3 } });
      } catch (error) {
        toast.add({
          title: 'Ошибка',
          description: 'Допущена ошибка в файле XML',
          icon: 'i-heroicons-exclamation-triangle',
          color: 'red',
        });
      }
    } else if (radioSelected.value === 'manualOKS') {
      router.replace({ query: { step: 1 } });
    } else if (radioSelected.value === 'manualObject') {
      router.replace({ query: { step: 2 } });
    } else if (radioSelected.value === 'bimModel') {
      router.replace({ query: { step: 3 } });
    }
  } else if (step.value === 1) {
    try {
      await buildingStore.createBuildingInfoManual(manualOKSInfo.value);
      router.replace({ query: { step: step.value + 1 } });
    } catch (error) {
      toast.add({
        title: 'Ошибка',
        description: 'Не удается создать объект капитального страительства, проверьте правильность заполнения полей',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  } else if (step.value === 2) {
    try {
      await constructionPartStore.createConstructionPart(buildingStore.currentBuilding.id, manualObjectInfo.value);
      router.replace({ query: { step: step.value + 1 } });
    } catch (error) {
      toast.add({
        title: 'Ошибка',
        description: 'Не удается добавить объект (строение) к данному ОКС, проверьте правильность заполнения полей',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  } else if (step.value === 3 && modelPropertiesFile.value && modelFragmentsFile.value) {
    try {
      if (currentConstructionSection.value.bimArtifacts.length === 2) {
        await removeModelFromSection(currentConstructionSection.value);
      }

      await bimArtifactsStore.uploadBimArtifact(currentConstructionSection.value.id, modelFragmentsFile.value);
      await bimArtifactsStore.uploadBimArtifact(currentConstructionSection.value.id, modelPropertiesFile.value);

      router.replace({ query: { step: step.value + 1 } });
    } catch (error) {
      toast.add({
        title: 'Ошибка',
        description: 'Не удается добавить BIM-модель объекта (строение) к данному ОКС',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  }

  try {
    await buildingStore.fetchAllBuildingInfo();
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Не удается обновить список ОКС и объектов',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }

  loading.value = false;
}

watchEffect(() => {
  const queryStep = Number(route.query.step);

  switch (queryStep) {
    case 1:
      radioSelected.value = 'manualOKS';
      step.value = queryStep;
      break;

    case 2:
      if (currentBuilding.value.id) {
        radioSelected.value = 'manualObject';
        step.value = queryStep;
      }
      break;

    case 3:
      if (currentConstructionPart.value.id) {
        radioSelected.value = 'bimModel';
        step.value = queryStep;
      }
      break;

    case 4:
      step.value = queryStep;
      break;

    default:
      step.value = 0;
      break;
  }
});
</script>

<style scoped></style>
