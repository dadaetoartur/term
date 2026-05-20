import { defineStore } from 'pinia';
import type { IBuilding } from '~/utils/types/Building';
import useBuildingStore from '.';

const useDocumentArtifactsStore = defineStore('documentArtifacts', {
  actions: {

    async uploadBimArtifact(buildingInfoID: string, body: FormData) {
      const buildingStore = useBuildingStore();

      try {
        const res: IBuilding = await useMyFetch<IBuilding>(`/document_artifacts/${buildingInfoID}/upload_artifact`, {
          method: 'POST',
          body,
        });

        buildingStore.setCurrentBuilding(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async downloadBimArtifact(buildingInfoID: string, filePath: string): Promise<Blob> {
      try {
        return await useMyFetch<Blob>(`/document_artifacts/${buildingInfoID}/download/${filePath}`, {
          method: 'GET',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async removeBimArtifact(buildingInfoID: string, filePath: string) {
      try {
        return await useMyFetch(`/document_artifacts/${buildingInfoID}/delete/${filePath}`, {
          method: 'DELETE',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },
});

export default useDocumentArtifactsStore;
