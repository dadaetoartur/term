<template>
  <div class="pt-2 ml-52">
    <NavBar />

    <UContainer class="mb-2">
      <TopMenu />

      <slot />
    </UContainer>
  </div>
</template>

<script setup lang="ts">
import NavBar from '~/components/management/NavBar.vue';
import TopMenu from '~/components/management/TopMenu.vue';
import useBuildingStore from '~/store/building';
import useUserStore from '~/store/user';

const userStore = useUserStore();
const buildingStore = useBuildingStore();

onMounted(async () => {
  await userStore.fetchCurrentUserInfo();
  await buildingStore.fetchAllBuildingInfo();
});
</script>
