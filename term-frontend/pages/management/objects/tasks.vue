<template>
  <main>
    <UDivider
      class="mb-4"
      label="Задачи сотрудников"
    />

    <TasksSummary />
    <TasksTable />
  </main>
</template>

<script lang="ts" setup>
import TasksSummary from '~/components/objects/tasks/TasksSummary.vue';
import TasksTable from '~/components/objects/tasks/TasksTable.vue';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});
</script>

<style lang="scss" scoped></style>
