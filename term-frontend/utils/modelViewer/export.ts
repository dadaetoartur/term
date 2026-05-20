import { type Components, FragmentManager } from 'openbim-components';

export default function exportModel(components: Components) {
  const fragments = components.tools.get(FragmentManager);

  if (!fragments.groups.length) return null;

  const group = Array.from(fragments.groups.values())[0];
  const data = fragments.export(group);
  const fragmentsFormData = new FormData();
  fragmentsFormData.append('file', new File([new Blob([data])], 'small.frag'));

  const properties = group.getLocalProperties();
  const propertiesFormData = new FormData();
  propertiesFormData.append('file', new File([JSON.stringify(properties)], 'small.json'));

  return { fragmentsFormData, propertiesFormData };
}
