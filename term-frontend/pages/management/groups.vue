<template>
  <main>
    <UDivider
      class="mb-4"
      label="Группы сотрудников"
    />

    <GroupsTable
      :groups="allGroups"
      :loading="loading"
    />
  </main>
</template>

<script lang="ts" setup>
import GroupsTable from '~/components/groups/GroupsTable.vue';
import useGroupStore from '~/store/group';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});

const groupStore = useGroupStore();
const loading = ref(true);
const allGroups = computed(() => groupStore.getAllGroups);

onMounted(async () => {
  if (Object.keys(allGroups.value).length === 0) {
    await groupStore.fetchAllGroups();
  }
  loading.value = false;
});
</script>

<style lang="scss" scoped></style>
