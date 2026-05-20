<template>
  <main>
    <UDivider
      class="mb-4"
      label="Профиль"
    />

    <UCard>
      <UserEditForm />
    </UCard>
  </main>
</template>

<script lang="ts" setup>
import UserEditForm from '~/components/profile/UserEditForm.vue';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});
</script>

<style lang="scss" scoped></style>
