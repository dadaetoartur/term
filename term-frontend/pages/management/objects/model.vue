<template>
  <main>
    <UDivider
      class="mb-4"
      label="BIM-модель объекта"
    />

    <ClientOnly>
      <Viewer />
    </ClientOnly>
  </main>
</template>

<script lang="ts" setup>
import Viewer from '~/components/objects/model/Viewer.vue';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});
</script>
