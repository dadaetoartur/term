import type { FragmentsGroup } from 'bim-fragment';
import { type Components, FragmentClassifier, FragmentTree } from 'openbim-components';
import * as WEBIFC from 'web-ifc';

export default async function modelTree(components: Components, modelLoad: FragmentsGroup) {
  const classifier = new FragmentClassifier(components);
  // await classifier.byIfcRel(modelLoad, WEBIFC.IFCRELCONTAINEDINSPATIALSTRUCTURE, 'level');
  classifier.byEntity(modelLoad);
  await classifier.byIfcRel(modelLoad, WEBIFC.IFCRELDEFINESBYTYPE, 'element');

  const tree = new FragmentTree(components);
  tree.init();
  await tree.update(['entities', 'element']);
  tree.uiElement.get('window').domElement.style.height = '90%';
  tree.uiElement.get('window').domElement.style.width = '50%';
  tree.uiElement.get('window').domElement.style.left = 'auto';
  tree.uiElement.get('window').domElement.style.right = '1rem';
  tree.uiElement.get('window').domElement.classList.remove('backdrop-blur-xl');
  tree.uiElement.get('window').domElement.classList.add('backdrop-blur-sm');
  tree.uiElement.get('main').innerElements.tooltip.innerText = 'Дерево элементов';
  tree.uiElement.get('window').innerElements.title.innerText = 'Дерево элементов';

  return { tree, classifier };
}
