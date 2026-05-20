import { defineStore } from 'pinia';
import { EMPTY_CONSTRUCTION_SECTION } from '~/utils/constants/Buildings';
import type { IBuildingConstructionSection } from '~/utils/types/Building';

interface IState {
  currentConstructionSection: IBuildingConstructionSection
}

const useConstructionSectionStore = defineStore('constructionSection', {
  state: (): IState => ({
    currentConstructionSection: { ...EMPTY_CONSTRUCTION_SECTION },
  }),

  actions: {
    setCurrentConstructionSection(section: IBuildingConstructionSection) {
      this.currentConstructionSection = section;
    },

    async fetchCurrentConstructionSection(constructionSectionID: string): Promise<IBuildingConstructionSection> {
      try {
        const res: IBuildingConstructionSection = await useMyFetch<IBuildingConstructionSection>(`/building_project/construction_section/${constructionSectionID}`, {
          method: 'GET',
        });

        this.setCurrentConstructionSection(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async createConstructionSection(constructionPartID: string, body: Partial<IBuildingConstructionSection>) {
      try {
        const res: IBuildingConstructionSection = await useMyFetch<IBuildingConstructionSection>(`/building_project/construction_part/${constructionPartID}/construction_section`, {
          method: 'POST',
          body,
        });

        this.setCurrentConstructionSection(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async updateConstructionSection(constructionSectionID: string, body: Partial<IBuildingConstructionSection>) {
      try {
        const res: IBuildingConstructionSection = await useMyFetch<IBuildingConstructionSection>(`/building_project/construction_section/${constructionSectionID}`, {
          method: 'PATCH',
          body,
        });

        this.setCurrentConstructionSection(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async removeConstructionSection(constructionSectionID: string) {
      try {
        return await useMyFetch(`/building_project/construction_section/${constructionSectionID}`, {
          method: 'DELETE',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },

  getters: {
    getCurrentConstructionSection: (state) => state.currentConstructionSection,
  },
});

export default useConstructionSectionStore;
