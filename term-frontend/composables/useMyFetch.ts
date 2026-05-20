import type {
  NitroFetchRequest,
} from 'nitropack';

const useMyFetch = async<
  T = unknown, R extends NitroFetchRequest = NitroFetchRequest
>(
  url: Parameters<typeof $fetch<T, R>>[0],
  otherOptions: Partial<Parameters<typeof $fetch<T, R>>[1]> = {},
): Promise<T> => {
  const { API_URL } = useRuntimeConfig().public;

  return $fetch(
    url,
    {
      credentials: 'include',
      baseURL: API_URL,
      ...otherOptions,
    },
  );
};

export default useMyFetch;
