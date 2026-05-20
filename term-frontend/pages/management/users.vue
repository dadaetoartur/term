<template>
  <main>
    <UDivider
      class="mb-4"
      label="Сотрудники"
    />

    <UsersTable
      :users="allUsers"
      :loading="loading"
    />
  </main>
</template>

<script lang="ts" setup>
import UsersTable from '~/components/users/UsersTable.vue';
import useUserStore from '~/store/user';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});

const userStore = useUserStore();
const loading = ref(true);
const allUsers = computed(() => userStore.getAllUsers);

onMounted(async () => {
  if (Object.keys(allUsers.value).length === 0) {
    await userStore.fetchAllUsers();
  }
  loading.value = false;
});

</script>

<style lang="scss" scoped></style>
