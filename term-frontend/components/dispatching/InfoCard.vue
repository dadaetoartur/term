<template>
  <UCard>
    <div class="flex gap-3">
      <UBadge
        class="h-14 w-14 flex justify-center"
        variant="outline"
      >
        <UIcon
          class="text-2xl"
          :name="icon"
        />
      </UBadge>
      <div class="flex flex-col ">
        <p class="text-base">
          {{ name }}
        </p>
        <p class="text-2xl font-bold">
          {{ value }}
        </p>
      </div>
    </div>
  </UCard>
</template>

<script setup lang="ts">
defineProps<{
  icon: string,
  name: string,
  value: string | number,
}>();
</script>

<style scoped></style>
