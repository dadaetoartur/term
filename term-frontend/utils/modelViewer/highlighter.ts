import { type Components, FragmentHighlighter } from 'openbim-components';
import { MeshBasicMaterial } from 'three';

export default function highlighterModel(components: Components) {
  // Инициализация подсветки фрагментов BIM-модели
  const highlighter = new FragmentHighlighter(components);
  highlighter.setup();
  highlighter.outlineEnabled = true;

  // Параметры подсветки фрагментов
  const highlightMaterial = new MeshBasicMaterial({
    color: '#0066CC',
    depthTest: false,
    opacity: 0.8,
    transparent: true,
  });

  // Добавление имени и типа подсветки
  // Далее на это имя будет везде ссылатся, чтобы подсветитть фрагмент
  highlighter.add('default', [highlightMaterial]);
  highlighter.outlineMaterial.color.set(0x004080);

  highlighter.updateHighlight();

  return { highlighter };
}
