import { defineStore } from 'pinia';
import { EMPTY_CONSTRUCTION_PART, EMPTY_BUILDING } from '~/utils/constants/Buildings';
import type { IBuilding } from '~/utils/types/Building';
import useConstructionPartStore from './constructionPart';

interface IState {
  allBuildings: IBuilding[]
  currentBuilding: IBuilding
}

const useBuildingStore = defineStore('building', {
  state: (): IState => ({
    allBuildings: [],
    currentBuilding: { ...EMPTY_BUILDING },
  }),

  actions: {
    setAllBuildings(buildings: IBuilding[]) {
      this.allBuildings = buildings;
    },

    setCurrentBuilding(building: IBuilding) {
      const constructionPartStore = useConstructionPartStore();
      this.currentBuilding = building;

      if (building.constructionParts.length > 0) {
        const updatedCurrentConstructionPart = building.constructionParts.find(
          (item) => item.id === constructionPartStore.currentConstructionPart.id,
        );

        if (updatedCurrentConstructionPart) {
          constructionPartStore.setCurrentConstructionPart(updatedCurrentConstructionPart);
        } else {
          constructionPartStore.setCurrentConstructionPart(building.constructionParts[0]);
        }
      } else {
        constructionPartStore.setCurrentConstructionPart({ ...EMPTY_CONSTRUCTION_PART });
      }
    },

    async fetchAllBuildingInfo(): Promise<IBuilding[]> {
      try {
        const res: IBuilding[] = await useMyFetch<IBuilding[]>('/building_project/all_building_info', {
          method: 'GET',
        });

        this.setAllBuildings(res);

        if (res.length > 0) {
          const updatedCurrentBuilding = res.find((item) => item.id === this.currentBuilding.id);

          if (updatedCurrentBuilding) {
            this.setCurrentBuilding(updatedCurrentBuilding);
          } else {
            this.setCurrentBuilding(res[0]);
          }
        } else {
          this.setCurrentBuilding({ ...EMPTY_BUILDING });
        }

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async createBuildingInfoManual(body: Partial<IBuilding>) {
      try {
        const res: IBuilding = await useMyFetch<IBuilding>('/building_project/building_info', {
          method: 'POST',
          body,
        });

        this.setCurrentBuilding(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async createBuildingInfoXml(body: FormData) {
      try {
        const res: IBuilding = await useMyFetch<IBuilding>('/building_project/building_info/xml', {
          method: 'POST',
          body,
        });

        this.setCurrentBuilding(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async editBuildingInfo(buildingID: string, body: IBuilding) {
      try {
        const res: IBuilding = await useMyFetch<IBuilding>(`/building_project/building_info/${buildingID}`, {
          method: 'PATCH',
          body,
        });

        this.setCurrentBuilding(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async removeBuilding(buildingID: string) {
      try {
        return await useMyFetch(`/building_project/building_info/${buildingID}`, {
          method: 'DELETE',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },

  getters: {
    getAllBuildings: (state) => state.allBuildings,
    getCurrentBuilding: (state) => state.currentBuilding,
  },
});

export default useBuildingStore;
