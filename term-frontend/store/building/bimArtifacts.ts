import { defineStore } from 'pinia';
import type { IBuildingConstructionSection } from '~/utils/types/Building';
import useConstructionSectionStore from './constructionSection';

const useBimArtifactsStore = defineStore('bimArtifacts', {
  actions: {
    async uploadBimArtifact(constructionSectionID: string, body: FormData) {
      const constructionSectionStore = useConstructionSectionStore();

      try {
        const res: IBuildingConstructionSection = await useMyFetch<IBuildingConstructionSection>(
          `/bim_artifacts/${constructionSectionID}/upload_artifact`,
          {
            method: 'POST',
            body,
          },
        );

        constructionSectionStore.setCurrentConstructionSection(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async downloadBimArtifact(constructionSectionID: string, filePath: string): Promise<Blob> {
      try {
        return await useMyFetch<Blob>(`/bim_artifacts/${constructionSectionID}/download/${filePath}`, {
          method: 'GET',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async removeBimArtifact(constructionSectionID: string, filePath: string) {
      try {
        return await useMyFetch(`/bim_artifacts/${constructionSectionID}/delete/${filePath}`, {
          method: 'DELETE',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },
});

export default useBimArtifactsStore;
