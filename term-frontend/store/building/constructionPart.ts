import { defineStore } from 'pinia';
import { EMPTY_CONSTRUCTION_PART, EMPTY_CONSTRUCTION_SECTION } from '~/utils/constants/Buildings';
import type { IBuildingConstructionPart } from '~/utils/types/Building';
import useConstructionSectionStore from './constructionSection';

interface IState {
  currentConstructionPart: IBuildingConstructionPart
}

const useConstructionPartStore = defineStore('constructionPart', {
  state: (): IState => ({
    currentConstructionPart: { ...EMPTY_CONSTRUCTION_PART },
  }),

  actions: {
    setCurrentConstructionPart(object: IBuildingConstructionPart) {
      const constructionSectionStore = useConstructionSectionStore();
      this.currentConstructionPart = object;

      if (object.sections.length > 0) {
        const updatedCurrentConstructionSection = object.sections.find(
          (item) => item.id === constructionSectionStore.currentConstructionSection.id,
        );

        if (updatedCurrentConstructionSection) {
          constructionSectionStore.setCurrentConstructionSection(updatedCurrentConstructionSection);
        } else {
          constructionSectionStore.setCurrentConstructionSection(object.sections[0]);
        }
      } else {
        constructionSectionStore.setCurrentConstructionSection({ ...EMPTY_CONSTRUCTION_SECTION });
      }
    },

    async fetchCurrentConstructionPartInfo(constructionPartID: string): Promise<IBuildingConstructionPart> {
      try {
        const res: IBuildingConstructionPart = await useMyFetch<IBuildingConstructionPart>(`/building_project/construction_part/${constructionPartID}`, {
          method: 'GET',
        });

        this.setCurrentConstructionPart(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async createConstructionPart(buildingID: string, body: Partial<IBuildingConstructionPart>): Promise<IBuildingConstructionPart> {
      try {
        const res: IBuildingConstructionPart = await useMyFetch<IBuildingConstructionPart>(`/building_project/building_info/${buildingID}/construction_part`, {
          method: 'POST',
          body,
        });

        this.setCurrentConstructionPart(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async editConstructionPart(constructionPartID: string, body: IBuildingConstructionPart) {
      try {
        const res: IBuildingConstructionPart = await useMyFetch<IBuildingConstructionPart>(`/building_project/construction_part/${constructionPartID}`, {
          method: 'PATCH',
          body,
        });

        this.setCurrentConstructionPart(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async removeConstructionPart(constructionPartID: string) {
      try {
        return await useMyFetch(`/building_project/construction_part/${constructionPartID}`, {
          method: 'DELETE',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },

  getters: {
    getCurrentConstructionPart: (state) => state.currentConstructionPart,
  },
});

export default useConstructionPartStore;
