import { useAuthStore } from '~/store/auth';

export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore();
  const token = useCookie('term_backend_auth');

  if (token.value && to?.name === 'login') {
    return navigateTo('/management');
  }

  if (!token.value && to?.name !== 'login') {
    authStore.resetAllStores();
    abortNavigation();
    return navigateTo('/login');
  }

  return true;
});
