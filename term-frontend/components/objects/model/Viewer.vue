<template>
  <UCard class="relative">
    <template #header>
      <div class="flex justify-between gap-3 items-center">
        <UButton
          color="gray"
          class="flex flex-row gap-3 px-3 py-2 mr-32"
          :disabled="loading"
        >
          <UToggle v-model="modelOptimiztaion" />
          <p
            class="cursor-pointer"
            @click="modelOptimiztaion = !modelOptimiztaion"
          >
            Оптимизировать производительность модели
          </p>
        </UButton>

        <div class="flex gap-3 items-center w-full">
          <p>Инженерная система: </p>
          <SectionsSwitcher
            class="w-1/2"
            :disabled="loading"
            @change-section="changeModel"
          />
        </div>
      </div>
    </template>

    <ModelLoading v-if="loading" />

    <div
      v-show="currentConstructionSection.bimArtifacts.length === 2"
      ref="modelContainer"
      class="modelContainer"
    />
    <div
      v-show="currentConstructionSection.bimArtifacts.length === 0"
      class="flex flex-col gap-3 items-center"
    >
      <p class="italic">
        Для данной инженерной системы еще не добавлена BIM-модель
      </p>
      <NuxtLink to="/management/objects/create?step=3">
        <UButton>Добавить</UButton>
      </NuxtLink>
    </div>
  </UCard>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import SectionsSwitcher from '~/components/management/SectionsSwitcher.vue';
import ModelLoading from '~/components/objects/model/ModelLoading.vue';
import {
  Button, Components, ScreenCuller, Toolbar,
} from 'openbim-components';
import generateModel from '~/utils/modelViewer/generate';
import { loadModelFromFragments } from '~/utils/modelViewer/load';
import clipperModel from '~/utils/modelViewer/clipper';
import highlighterModel from '~/utils/modelViewer/highlighter';
import modelTree from '~/utils/modelViewer/tools/tree';
import { modelPropertiesFinder, modelPropertiesViewer } from '~/utils/modelViewer/tools/properties';
import { Color } from 'three';
import type { IBuildingConstructionSection } from '~/utils/types/Building';
import useConstructionSectionStore from '~/store/building/constructionSection';
import useBimArtifactsStore from '~/store/building/bimArtifacts';

const loading = ref(true);
const modelOptimiztaion = ref(false);
const constructionSectionStore = useConstructionSectionStore();
const bimArtifactsStore = useBimArtifactsStore();
const currentConstructionSection = computed(() => constructionSectionStore.getCurrentConstructionSection);

const modelContainer = ref<HTMLDivElement | null>(null);
// Создание нового компонента BIM-модели
let components = new Components();
const colorMode = useColorMode();
const toast = useToast();
const isDark = computed(() => colorMode.value === 'dark');

async function loadModelForSection(constructionSection: IBuildingConstructionSection, container: HTMLDivElement) {
  loading.value = true;

  if (constructionSection.bimArtifacts.length === 2) {
    components.dispose();
    const mapArtifacts = new Map();

    for (const artifact of constructionSection.bimArtifacts) {
      if (artifact.file_path.includes('json')) {
        mapArtifacts.set('json', artifact.file_path);
      } else if (artifact.file_path.includes('frag')) {
        mapArtifacts.set('frag', artifact.file_path);
      }
    }

    try {
      const fragments = await bimArtifactsStore.downloadBimArtifact(currentConstructionSection.value.id, mapArtifacts.get('frag'));
      const properties = await bimArtifactsStore.downloadBimArtifact(currentConstructionSection.value.id, mapArtifacts.get('json'));

      components = new Components();
      const { scene } = generateModel(components, container);
      const { modelLoad } = await loadModelFromFragments(components, fragments, properties);
      scene.add(modelLoad);

      const { highlighter } = highlighterModel(components);
      const { tree } = await modelTree(components, modelLoad);
      const { propsProcessor, renderPropertiesProcessor } = modelPropertiesViewer(components, modelLoad);
      const { propsFinder } = modelPropertiesFinder(components);

      watchEffect(() => {
        if (isDark.value) {
          scene.background = new Color(0x202932);
        } else {
          scene.background = new Color('#f5f5f5');
        }
      });

      tree.onSelected.add(async ({ items, visible }) => {
        if (visible) {
          highlighter.clear();
          await highlighter.highlightByID('default', items, true, true);

          renderPropertiesProcessor(items);
        }
      });

      propsFinder.onFound.add((result) => {
        highlighter.highlightByID('default', result);

        renderPropertiesProcessor(result);
      });

      highlighter.events.select.onClear.add(() => {
        highlighter.highlight('default', true);
        propsProcessor.cleanPropertiesList();
        if (propsProcessor) propsProcessor.uiElement.get('propertiesWindow').visible = false;
      });

      // Действия при нажатии на элемент на модели
      highlighter.events.select.onHighlight.add((selection) => {
        highlighter.clear();
        highlighter.highlight('default', true);

        renderPropertiesProcessor(selection);
        if (propsProcessor) propsProcessor.uiElement.get('propertiesWindow').visible = true;
      });

      // Требуется для вкл/выкл оптимизации модели
      const culler = new ScreenCuller(components);
      culler.setup();
      const cullerListener = () => { culler.elements.needsUpdate = true; };

      clipperModel(components, container);

      const cubeTools = new Button(components);
      cubeTools.materialIcon = 'info';
      cubeTools.tooltip = 'Двойное нажатие левой кнопки мыши создаст срез объекта';

      const mainToolbar = new Toolbar(components);
      components.ui.addToolbar(mainToolbar);
      mainToolbar.addChild(
        cubeTools,
        propsFinder.uiElement.get('main'),
        propsProcessor.uiElement.get('main'),
        tree.uiElement.get('main'),
      );

      // Включение и отключение оптимизации
      watchEffect(() => {
        if (modelOptimiztaion.value) {
          if (culler.get().size === 0) {
            for (const fragment of modelLoad.items) {
              culler.elements.add(fragment.mesh);
            }
          }
          container.addEventListener('mouseup', cullerListener);
          container.addEventListener('wheel', cullerListener);
          cullerListener();
        } else {
          for (const fragment of modelLoad.items) {
            fragment.mesh.visible = true;
          }
          container.removeEventListener('mouseup', cullerListener);
          container.removeEventListener('wheel', cullerListener);
        }
      });
    } catch (error) {
      toast.add({
        title: 'Ошибка',
        description: 'Не удается загрузить данные модели с сервера, попробуйте позже',
        icon: 'i-heroicons-exclamation-triangle',
        color: 'red',
      });
    }
  }

  loading.value = false;
}

const changeModel = async (section: IBuildingConstructionSection) => { if (modelContainer.value) loadModelForSection(section, modelContainer.value); };

onMounted(async () => {
  if (modelContainer.value) {
    await loadModelForSection(currentConstructionSection.value, modelContainer.value);
  }

  loading.value = false;
});

onUnmounted(() => {
  components.dispose();
});
</script>

<style lang="scss">
.modelContainer {
  width: 100%;
  height: 70vh;

  & #cube-map-front:before {
    content: "F";
  }
}
</style>
