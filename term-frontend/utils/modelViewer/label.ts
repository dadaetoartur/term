import { type Components, DimensionLabelClassName, Simple2DMarker } from 'openbim-components';
import { type Matrix4 } from 'three';

export default function createLabelModel(components: Components, matrixPosition: Matrix4[], text: string, expressId: number, className: string = '') {
  const htmlText = document.createElement('div');
  htmlText.className = `${DimensionLabelClassName} ${className}`;
  const labelMarker = new Simple2DMarker(components, htmlText);
  labelMarker.get().position.setFromMatrixPosition(matrixPosition[0]);
  labelMarker.get().element.textContent = text;
}
