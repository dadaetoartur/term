import type { FragmentsGroup } from 'bim-fragment';
import {
  IfcPropertiesFinder, IfcPropertiesProcessor, type Components, type FragmentIdMap,
} from 'openbim-components';

export function modelPropertiesViewer(components: Components, modelLoad: FragmentsGroup) {
  const propsProcessor = new IfcPropertiesProcessor(components);
  propsProcessor.uiElement.get('propertiesWindow').domElement.style.height = '90%';
  propsProcessor.uiElement.get('propertiesWindow').domElement.classList.remove('backdrop-blur-xl');
  propsProcessor.uiElement.get('propertiesWindow').domElement.classList.add('backdrop-blur-sm');
  propsProcessor.uiElement.get('main').innerElements.tooltip.innerText = 'Свойства элемента';
  propsProcessor.uiElement.get('propertiesWindow').innerElements.title.innerText = 'Свойства элемента';
  propsProcessor.process(modelLoad);

  const renderPropertiesProcessor = (selection: FragmentIdMap) => {
    const fragmentID = Object.keys(selection)[0];
    const expressID = [...selection[fragmentID]][0];
    propsProcessor.renderProperties(modelLoad, expressID);

    return expressID;
  };

  return { propsProcessor, renderPropertiesProcessor };
}

export function modelPropertiesFinder(components: Components) {
  const propsFinder = new IfcPropertiesFinder(components);
  propsFinder.init();
  propsFinder.uiElement.get('queryWindow').domElement.style.width = '60%';
  propsFinder.uiElement.get('queryWindow').domElement.classList.remove('backdrop-blur-xl');
  propsFinder.uiElement.get('queryWindow').domElement.classList.add('backdrop-blur-sm');
  propsFinder.uiElement.get('main').innerElements.tooltip.innerText = 'Поиск элемента';
  propsFinder.uiElement.get('queryWindow').innerElements.title.innerText = 'Поиск элемента';

  return { propsFinder };
}
