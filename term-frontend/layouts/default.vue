<template>
  <div class="flex flex-col justify-between min-h-screen">
    <Header />

    <UContainer>
      <slot />
    </UContainer>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '~/components/promo/Header.vue';
import Footer from '~/components/promo/Footer.vue';
</script>
