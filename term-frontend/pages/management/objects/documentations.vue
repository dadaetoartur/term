<template>
  <main>
    <UDivider
      class="mb-4"
      label="Документация"
    />

    <DocsTable />
  </main>
</template>

<script lang="ts" setup>
import DocsTable from '~/components/objects/documentations/DocsTable.vue';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});
</script>

<style lang="scss" scoped></style>
