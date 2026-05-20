/* eslint-disable no-param-reassign */
import {
  type Components, SimpleScene, PostproductionRenderer, OrthoPerspectiveCamera, SimpleRaycaster, SimpleGrid,
  CubeMap,
} from 'openbim-components';
import { DirectionalLight, AmbientLight, Color } from 'three';

export default function generateModel(components: Components, container: HTMLDivElement, sceneColor: Color = new Color('#f5f5f5')) {
  // Создание сцены, типа рендера модели, инициализция камеры, трассировка лучей
  const sceneComponent = new SimpleScene(components);
  sceneComponent.get().background = sceneColor;
  components.scene = sceneComponent;
  const renderer = new PostproductionRenderer(components, container);
  components.renderer = renderer;
  const camera = new OrthoPerspectiveCamera(components);
  components.camera = camera;
  components.raycaster = new SimpleRaycaster(components);

  // Инициализация всего выше созданного
  components.init();

  // Местонахождение камеры при инициализации
  camera.controls.setLookAt(10, 15, 30, 11, 10, 0);

  // Установка сцены
  const scene = components.scene.get();
  sceneComponent.setup();

  // Параметры постобработки объекта
  renderer.postproduction.enabled = true;
  renderer.postproduction.customEffects.outlineEnabled = true;

  // Добавление красивого света на сцене
  const directionalLight = new DirectionalLight();
  directionalLight.position.set(5, 10, 3);
  directionalLight.intensity = 0.5;
  scene.add(directionalLight);
  const ambientLight = new AmbientLight();
  ambientLight.intensity = 0.5;
  scene.add(ambientLight);

  // Создание сетки на сцене
  const grid = new SimpleGrid(components);
  const gridMesh = grid.get();
  const effects = renderer.postproduction.customEffects;
  effects.excludedMeshes.push(gridMesh);

  // Добавление навигационного куба
  const navCube = new CubeMap(components);
  navCube.offset = 1;
  navCube.setSize('750');
  navCube.setPosition('bottom-right');

  return { scene };
}
