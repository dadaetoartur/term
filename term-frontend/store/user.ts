import { defineStore } from 'pinia';
import { EMPTY_USER } from '~/utils/constants/Users';
import type { IUser } from '~/utils/types/User';

interface IState {
  currentUser: IUser,
  allUsers: IUser[]
}

const useUserStore = defineStore('user', {
  state: (): IState => ({
    currentUser: { ...EMPTY_USER },
    allUsers: [],
  }),

  actions: {
    async fetchCurrentUserInfo() {
      try {
        this.currentUser = await useMyFetch<IUser>('/users/me', { method: 'GET' });
      } catch (error) {
        const toast = useToast();

        toast.add({
          title: 'Ошибка',
          description: 'Невозможно загрузить данные о пользователе',
          icon: 'i-heroicons-exclamation-triangle',
          color: 'red',
        });
      }

      return this.currentUser;
    },

    async fetchAllUsers() {
      try {
        this.allUsers = await useMyFetch<IUser[]>('/users/all-users', { method: 'GET' });
      } catch (error) {
        const toast = useToast();

        toast.add({
          title: 'Ошибка',
          description: 'Невозможно загрузить данные о пользователях',
          icon: 'i-heroicons-exclamation-triangle',
          color: 'red',
        });
      }

      return this.allUsers;
    },

    async updateCurrentUserInfo(body: Partial<Omit<IUser, 'id' | 'groups'>>) {
      try {
        this.currentUser = await useMyFetch<IUser>(`/users/${this.currentUser.id}`, {
          method: 'PATCH',
          body,
        });

        return this.currentUser;
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async createUser(body: Omit<IUser, 'id' | 'groups'>) {
      try {
        return await useMyFetch<IUser>('/users/create-user', {
          method: 'POST',
          body,
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async updateUser(id: string, body: Partial<Omit<IUser, 'id' | 'groups'>>) {
      try {
        return await useMyFetch<IUser>(`/users/${id}`, {
          method: 'PATCH',
          body,
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },

    async removeUser(id: string) {
      try {
        return await useMyFetch<IUser>(`/users/${id}`, {
          method: 'DELETE',
        });
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },

  getters: {
    getCurrentUser: (state) => state.currentUser,
    getAllUsers: (state) => state.allUsers,
  },
});

export default useUserStore;
