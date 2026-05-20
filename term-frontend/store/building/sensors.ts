import { defineStore } from 'pinia';
import type { IBuildingSectionSensorData, IBuildingSectionSensors } from '~/utils/types/Building';

interface IState {
  allSensors: IBuildingSectionSensors[]
}

const useSensorsStore = defineStore('sensors', {
  state: (): IState => ({
    allSensors: [],
  }),

  actions: {
    setAllSensors(sensors: IBuildingSectionSensors[]) {
      this.allSensors = sensors;
    },

    async fetchConstructionSectionSensors(constructionSectionID: string): Promise<IBuildingSectionSensors[]> {
      try {
        const res: IBuildingSectionSensors[] = await useMyFetch<IBuildingSectionSensors[]>(`/sensors/${constructionSectionID}/all-sensors`, {
          method: 'GET',
        });

        this.setAllSensors(res);

        return res;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async fetchCurrentSensorData(constructionSectionID: string, sensorID: string, dateRange: { start: Date, end: Date }): Promise<IBuildingSectionSensorData[]> {
      try {
        return await useMyFetch<IBuildingSectionSensorData[]>(
          `/sensors/${constructionSectionID}/get-data/${sensorID}?start=${new Date(dateRange.start).toISOString()}&end=${new Date(dateRange.end).toISOString()}`,
          {
            method: 'GET',
          },
        );
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },

  getters: {
    getAllSensors: (state) => state.allSensors,
  },
});

export default useSensorsStore;
