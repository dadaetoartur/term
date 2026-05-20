<template>
  <main>
    <UDivider
      class="mb-4"
      label="Управление ОКС и объектами"
    />

    <UCard>
      <template #header>
        <div class="flex justify-between gap-3 ">
          <GroupObjectsSwitcher
            :title="currentBuilding.id ? currentBuilding.name : 'Нет данных'"
            :management-btn="false"
          />

          <ClientOnly>
            <div class="flex gap-3">
              <UButton
                :disabled="!currentBuilding.id"
                color="black"
                @click="editBuilding"
              >
                Изменить ОКС
              </UButton>

              <UButton
                :disabled="!currentBuilding.id"
                color="red"
                @click="removeBuilding"
              >
                Удалить ОКС
              </UButton>
            </div>
          </ClientOnly>
        </div>
      </template>

      <ObjectsTable :loading="tableLoading" />
    </UCard>
  </main>
</template>

<script lang="ts" setup>
import useBuildingStore from '~/store/building';
import ObjectsTable from '~/components/objects/manage/ObjectsTable.vue';
import RemoveBuilding from '~/components/objects/manage/modals/RemoveBuilding.vue';
import EditBuilding from '~/components/objects/manage/modals/EditBuilding.vue';
import GroupObjectsSwitcher from '~/components/management/GroupObjectsSwitcher.vue';

definePageMeta({
  layout: 'management',
  middleware: 'auth',
});

const modal = useModal();
const buildingStore = useBuildingStore();
const currentBuilding = computed(() => buildingStore.currentBuilding);

const tableLoading = ref(true);

const removeBuilding = () => modal.open(RemoveBuilding, {
  building: currentBuilding.value,
  onSuccess() {
    modal.close();
  },
});

const editBuilding = () => modal.open(EditBuilding, {
  building: currentBuilding.value,
  onSuccess() {
    modal.close();
  },
});

onMounted(async () => {
  await buildingStore.fetchAllBuildingInfo();
  tableLoading.value = false;
});
</script>

<style lang="scss" scoped></style>
