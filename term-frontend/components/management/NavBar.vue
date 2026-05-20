<template>
  <UCard class="fixed top-2 bottom-2 left-2 w-52">
    <NuxtLink
      class="flex justify-center mb-4"
      to="/management"
    >
      <h1 class="m-0 title">
        TERM
      </h1>
    </NuxtLink>

    <UBadge class="flex text-center justify-center p-3 gap-1 mb-2">
      <UTooltip
        :popper="{ offsetDistance: 16, placement: 'bottom' }"
        :ui="{ base: 'whitespace-normal overflow-visible h-full text-clip', width: 'max-w-min' }"
        :text="currentBuilding.name.length > 0 ? currentBuilding.name : 'Нет данных'"
      >
        <p class="overflow-ellipsis overflow-hidden line-clamp-2 w-full cursor-default">
          {{ currentBuilding.name.length > 0 ? currentBuilding.name : 'Нет данных' }}
        </p>
      </UTooltip>
    </UBadge>

    <UBadge
      variant="outline"
      class="flex text-center justify-center p-3 gap-1 mb-2"
    >
      <UTooltip
        :popper="{ offsetDistance: 16, placement: 'bottom' }"
        :ui="{ base: 'whitespace-normal overflow-visible h-full text-clip', width: 'max-w-min' }"
        :text="currentConstructionPart.name.length > 0 ? currentConstructionPart.name : 'Нет данных'"
      >
        <p class="overflow-ellipsis overflow-hidden line-clamp-2 w-full cursor-default">
          {{ currentConstructionPart.name.length > 0 ? currentConstructionPart.name : 'Нет данных' }}
        </p>
      </UTooltip>
    </UBadge>

    <UDivider class="mb-3" />

    <div class="flex flex-col gap-3 mb-3">
      <UVerticalNavigation :links="links" />
    </div>

    <div class="absolute bottom-3 left-0 right-0 flex flex-col items-center">
      <NuxtLink
        class="flex flex-col items-center gap-2 mb-4"
        to="/management/profile"
      >
        <UAvatar
          :alt="`${user.first_name} ${user.last_name}`"
          size="2xl"
        />
        <p>{{ `${user.first_name} ${user.last_name}` }}</p>
      </NuxtLink>

      <div class="flex items-center gap-3">
        <NuxtLink to="/management/profile">
          <UTooltip text="Настройки профиля">
            <UButton
              icon="i-heroicons-cog-6-tooth"
              color="gray"
            />
          </UTooltip>
        </NuxtLink>

        <UTooltip text="Выход">
          <UButton
            :loading="loadLogout"
            icon="i-heroicons-arrow-left-start-on-rectangle"
            color="gray"
            @click="logout"
          />
        </UTooltip>
      </div>
    </div>
  </UCard>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth';
import useBuildingStore from '~/store/building';
import useConstructionPartStore from '~/store/building/constructionPart';
import useUserStore from '~/store/user';

const toast = useToast();
const router = useRouter();
const authStore = useAuthStore();
const buildingStore = useBuildingStore();
const constructionPartStore = useConstructionPartStore();
const user = computed(() => useUserStore().getCurrentUser);
const currentBuilding = computed(() => buildingStore.getCurrentBuilding);
const currentConstructionPart = computed(() => constructionPartStore.getCurrentConstructionPart);
const loadLogout = ref(false);

const links = [[{
  label: 'Диспетчеризация',
  icon: 'i-heroicons-squares-plus',
  to: '/management',
}], [{
  label: 'BIM-модель',
  icon: 'i-heroicons-cube',
  to: '/management/objects/model',
}, {
  label: 'Задачи',
  icon: 'i-heroicons-calendar-days',
  to: '/management/objects/tasks',
}], [{
  label: 'Общие сведения',
  icon: 'i-heroicons-magnifying-glass',
  to: '/management/objects/info',
}, {
  label: 'Документация',
  icon: 'i-heroicons-folder',
  to: '/management/objects/documentations',
}]];

async function logout() {
  try {
    loadLogout.value = true;
    await authStore.logout();

    router.push('/login');
  } catch (error) {
    toast.add({
      title: 'Ошибка',
      description: 'Сервис не отвечает, попробуйте позже',
      icon: 'i-heroicons-exclamation-triangle',
      color: 'red',
    });
  } finally {
    loadLogout.value = false;
  }
}
</script>

<style lang="scss">
.title {
  font-size: 2.5rem;
  font-weight: bold;
  letter-spacing: 2px;

  &::first-letter {
    color: rgb(var(--color-primary-500));
  }
}
</style>
