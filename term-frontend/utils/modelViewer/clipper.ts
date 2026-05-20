import { type Components, EdgesClipper } from 'openbim-components';

export default function clipperModel(components: Components, container: HTMLDivElement) {
  // Инициализация среза модели
  const clipper = new EdgesClipper(components);
  clipper.enabled = true;

  // Слушатель двойного клика на создание среза модели
  container.addEventListener('dblclick', () => {
    clipper.deleteAll();
    clipper.create();
    const newClipper = clipper.get()[0];
    if (newClipper) {
      newClipper.size = 5;
    }
  });

  return { clipper };
}
