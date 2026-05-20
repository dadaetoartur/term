<template>
  <div>
    <div class="flex w-full gap-5 justify-between mb-3">
      <div class="flex w-full flex-col gap-3 self-center">
        <h3 class="text-base">
          Загрузка и предпросмотр модели
        </h3>

        <UTooltip text="Загрузить новую модель">
          <UInput
            class="w-full"
            type="file"
            @change="loadModel"
          />
        </UTooltip>
      </div>

      <UDivider orientation="vertical" />

      <div class="flex w-full flex-col gap-3 self-center">
        <h3 class="text-base">
          Управление инженерными системами:
        </h3>

        <div class="flex justify-stretch w-full gap-3">
          <SectionsSwitcher
            :disabled="loadingModel"
            @change-section="loadModelToSection"
          />

          <UTooltip text="Создать новую инженерную систему">
            <UButton @click="createSection">
              Создать
            </UButton>
          </UTooltip>

          <UTooltip text="Удалить выбранную инженерную систему">
            <UButton
              color="red"
              @click="removeSection"
            >
              Удалить
            </UButton>
          </UTooltip>
        </div>
      </div>
    </div>

    <div
      ref="modelContainer"
      class="modelContainer mb-3"
    >
      <ModelLoading v-if="loadingModel" />
    </div>

    <UCard
      v-if="currentConstructionSection.bimArtifacts && currentConstructionSection.bimArtifacts.length === 2"
      :ui="{ body: { base: 'flex items-center justify-between gap-3' } }"
    >
      <p>
        У инженерной системы <UBadge variant="soft">
          {{ currentConstructionSection.name }}
        </UBadge> уже загружена BIM-модель. Вы можете
        ее
        удалить или загрузить новую.
      </p>
      <UButton
        color="red"
        @click="removeModel"
      >
        Удалить модель
      </UButton>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { Components } from 'openbim-components';
import { Color, type Scene } from 'three';
import generateModel from '~/utils/modelViewer/generate';
import { loadModelFromFragments, loadModelFromIfc } from '~/utils/modelViewer/load';
import { FragmentsGroup } from 'bim-fragment';
import ModelLoading from '~/components/objects/model/ModelLoading.vue';
import exportModel from '~/utils/modelViewer/export';
import SectionsSwitcher from '~/components/management/SectionsSwitcher.vue';
import useConstructionPartStore from '~/store/building/constructionPart';
import type { IBuildingConstructionSection } from '~/utils/types/Building';
import useConstructionSectionStore from '~/store/building/constructionSection';
import useBimArtifactsStore from '~/store/building/bimArtifacts';
import { mapOfBimArtifacts, removeModelFromSection } from '~/utils/artifacts';
import AddSectionModal from './AddSectionModal.vue';
import RemoveSectionModal from './RemoveSectionModal.vue';

const emits = defineEmits<{
  modelLoaded: [value: boolean],
  modelFragmentsFile: [value: FormData]
  modelPropertiesFile: [value: FormData]
}>();

const modelContainer = ref<HTMLDivElement | null>(null);
const modelFragmentsGroup = ref<FragmentsGroup>(new FragmentsGroup());
const sceneGlobal = ref<Scene | null>(null);
const loadingModel = ref(false);

const toast = useToast();
const modal = useModal();
const constructionPartStore = useConstructionPartStore();
const constructionSectionStore = useConstructionSectionStore();
const bimArtifactsStore = useBimArtifactsStore();
const components = new Components();
const colorMode = useColorMode();
const isDark = computed(() => colorMode.value === 'dark');
const currentConstructionPart = computed(() => constructionPartStore.getCurrentConstructionPart);
const currentConstructionSection = computed(() => constructionSectionStore.getCurrentConstructionSection);

const createSection = () => modal.open(AddSectionModal, {
  constructionPart: currentConstructionPart.value,
  onSuccess() {
    constructionPartStore.fetchCurrentConstructionPartInfo(currentConstructionPart.value.id);
    modal.close();
  },
  onClose() {
    modal.close();
  },
});

const removeSection = () => modal.open(RemoveSectionModal, {
  onSuccess() {
    constructionPartStore.fetchCurrentConstructionPartInfo(currentConstructionPart.value.id);
    modal.close();
  },
  onClose() {
    modal.close();
  },
});

async function loadModel(fileList: FileList) {
  try {
    emits('modelLoaded', false);
    loadingModel.value = true;
    const fileNameSplit = fileList[0].name.split('.');

    if (fileNameSplit[fileNameSplit.length - 1] !== 'ifc') {
      toast.add({
        title: 'Ошибка формата файла',
        description: 'Данный формат файла не подходит. Выберите файл с расширением *.ifc',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });

      return;
    }

    if (modelFragmentsGroup) {
      sceneGlobal.value?.remove(modelFragmentsGroup.value);
    }

    const { modelLoad } = await loadModelFromIfc(components, fileList[0]);
    modelFragmentsGroup.value = modelLoad;
    sceneGlobal.value?.add(modelFragmentsGroup.value);

    const exportData = exportModel(components);

    if (exportData) {
      emits('modelLoaded', true);
      emits('modelFragmentsFile', exportData.fragmentsFormData);
      emits('modelPropertiesFile', exportData.propertiesFormData);
    } else {
      toast.add({
        title: 'Ошибка',
        description: 'При экспорте модели, что-то пошло не так',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Ошибка загрузки модели, попробуйте еще раз или убедитесь, что загружаете модель с расширением *.ifc',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  } finally {
    loadingModel.value = false;
  }
}

async function loadModelToSection(constructionSection: IBuildingConstructionSection) {
  loadingModel.value = true;

  if (modelFragmentsGroup) {
    sceneGlobal.value?.remove(modelFragmentsGroup.value);
  }

  if (constructionSection.bimArtifacts && constructionSection.bimArtifacts.length === 2) {
    const mapArtifacts = mapOfBimArtifacts(constructionSection.bimArtifacts);

    try {
      const fragments = await bimArtifactsStore.downloadBimArtifact(currentConstructionSection.value.id, mapArtifacts.frag);
      const properties = await bimArtifactsStore.downloadBimArtifact(currentConstructionSection.value.id, mapArtifacts.json);

      const { modelLoad } = await loadModelFromFragments(components, fragments, properties);
      modelFragmentsGroup.value = modelLoad;
      sceneGlobal.value?.add(modelFragmentsGroup.value);
    } catch (error) {
      toast.add({
        title: 'Ошибка',
        description: 'Не удается загрузить данные модели с сервера, попробуйте позже',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  }

  loadingModel.value = false;
}

const removeModel = async () => {
  try {
    await removeModelFromSection(currentConstructionSection.value);
    await constructionPartStore.fetchCurrentConstructionPartInfo(currentConstructionPart.value.id);

    await loadModelToSection(currentConstructionSection.value);
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'При удалении модели с сервера, что-то пошло не так',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  }
};

onMounted(async () => {
  if (modelContainer.value) {
    const { scene } = generateModel(components, modelContainer.value);
    sceneGlobal.value = scene;
    loadModelToSection(currentConstructionSection.value);

    watchEffect(() => {
      if (isDark.value) {
        scene.background = new Color(0x202932);
      } else {
        scene.background = new Color('#f5f5f5');
      }
    });
  }
});

onUnmounted(() => {
  components.dispose();
});
</script>

<style scoped>
.modelContainer {
  position: relative;
  width: 100%;
  height: 40rem;
}
</style>
