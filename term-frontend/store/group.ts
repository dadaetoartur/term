import { defineStore } from 'pinia';
import type { IGroup } from '~/utils/types/Group';

interface IState {
  allGroups: IGroup[],
}

const useGroupStore = defineStore('group', {
  state: (): IState => ({
    allGroups: [],
  }),

  actions: {
    async fetchAllGroups(): Promise<IGroup[]> {
      try {
        this.allGroups = await useMyFetch<IGroup[]>('/group/all-groups', { method: 'GET' });
      } catch (error) {
        return Promise.reject(error);
      }

      return this.allGroups;
    },

    async createGroup(body: Omit<IGroup, 'id'>): Promise<IGroup> {
      try {
        return await useMyFetch<IGroup>('/group/create', {
          method: 'POST',
          body,
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async updateGroup(id: string, body: Partial<Omit<IGroup, 'id'>>): Promise<IGroup> {
      try {
        return await useMyFetch<IGroup>(`/group/${id}`, {
          method: 'PATCH',
          body,
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async removeGroup(id: string) {
      try {
        return await useMyFetch<IGroup>(`/group/${id}`, {
          method: 'DELETE',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async addUserToGroup(groupID: string, userID: string) {
      try {
        return await useMyFetch<IGroup>(`/group/${groupID}/add-user/${userID}`, {
          method: 'POST',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async removeUserFromGroup(groupID: string, userID: string) {
      try {
        return await useMyFetch<IGroup>(`/group/${groupID}/delete-user/${userID}`, {
          method: 'DELETE',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },

  getters: {
    getAllGroups: (state) => state.allGroups,
  },
});

export default useGroupStore;
