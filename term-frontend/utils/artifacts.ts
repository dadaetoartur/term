import useBimArtifactsStore from '~/store/building/bimArtifacts';
import type { IBuildingArtifact, IBuildingConstructionSection } from './types/Building';

export function mapOfBimArtifacts(bimArtifacts: IBuildingArtifact[]) {
  const mapArtifacts = {
    json: '',
    frag: '',
  };

  for (const artifact of bimArtifacts) {
    if (artifact.file_path.includes('json')) {
      mapArtifacts.json = artifact.file_path;
    } else if (artifact.file_path.includes('frag')) {
      mapArtifacts.frag = artifact.file_path;
    }
  }

  return mapArtifacts;
}

export async function removeModelFromSection(constructionSection: IBuildingConstructionSection) {
  const bimArtifactsStore = useBimArtifactsStore();

  const mapArtifacts = mapOfBimArtifacts(constructionSection.bimArtifacts);

  await bimArtifactsStore.removeBimArtifact(constructionSection.id, mapArtifacts.frag);
  await bimArtifactsStore.removeBimArtifact(constructionSection.id, mapArtifacts.json);
}
