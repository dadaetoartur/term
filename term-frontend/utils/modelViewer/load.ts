import type { IfcProperties } from 'bim-fragment';
import { type Components, FragmentIfcLoader, FragmentManager } from 'openbim-components';
import * as WEBIFC from 'web-ifc';

export async function loadModelFromIfc(components: Components, file: File) {
  let fragmentIfcLoader = components.tools.get(FragmentIfcLoader);

  if (!fragmentIfcLoader) {
    fragmentIfcLoader = new FragmentIfcLoader(components);
  }

  await fragmentIfcLoader.setup();

  const excludedCats = [
    WEBIFC.IFCTENDONANCHOR,
    WEBIFC.IFCREINFORCINGBAR,
    WEBIFC.IFCREINFORCINGELEMENT,
  ];
  for (const cat of excludedCats) {
    fragmentIfcLoader.settings.excludedCategories.add(cat);
  }

  fragmentIfcLoader.settings.webIfc.COORDINATE_TO_ORIGIN = true;
  fragmentIfcLoader.settings.webIfc.OPTIMIZE_PROFILES = true;

  const data = await file.arrayBuffer();
  const buffer = new Uint8Array(data);
  const modelLoad = await fragmentIfcLoader.load(buffer);

  return { modelLoad };
}

export async function loadModelFromFragments(components: Components, fragmentsFile: Blob, propertiesFile: Blob) {
  let fragments = components.tools.get(FragmentManager);

  if (!fragments) {
    fragments = new FragmentManager(components);
  }

  const buffer = new Uint8Array(await fragmentsFile.arrayBuffer());
  const modelLoad = await fragments.load(buffer);

  const properties: IfcProperties = JSON.parse(await propertiesFile.text());
  modelLoad.setLocalProperties(properties);

  return { modelLoad, properties, fragments };
}
