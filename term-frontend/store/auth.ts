import { defineStore } from 'pinia';
import useBuildingStore from './building';
import useUserStore from './user';
import useGroupStore from './group';
import useSensorsStore from './building/sensors';
import useConstructionPartStore from './building/constructionPart';
import useConstructionSectionStore from './building/constructionSection';

export interface IUserCredits {
  username: string;
  password: string;
}

export const useAuthStore = defineStore('auth', {
  actions: {
    async login({ username, password }: IUserCredits) {
      const body = `username=${username}&password=${password}`;

      try {
        await useMyFetch('/auth/login', {
          body,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          method: 'POST',
        });

        return Promise.resolve();
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async logout() {
      try {
        await useMyFetch('/auth/logout', { method: 'POST' });

        this.resetAllStores();

        return Promise.resolve();
      } catch (error) {
        return Promise.reject(error);
      }
    },

    resetAllStores() {
      const buildingStore = useBuildingStore();
      buildingStore.$reset();

      const constructionPartStore = useConstructionPartStore();
      constructionPartStore.$reset();

      const constructionSectionStore = useConstructionSectionStore();
      constructionSectionStore.$reset();

      const userStore = useUserStore();
      userStore.$reset();

      const groupStore = useGroupStore();
      groupStore.$reset();

      const sensorsStore = useSensorsStore();
      sensorsStore.$reset();
    },
  },
});
