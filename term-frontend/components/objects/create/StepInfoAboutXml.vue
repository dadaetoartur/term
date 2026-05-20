<template>
  <div class="flex w-full gap-14 justify-between">
    <div class="flex w-full flex-col gap-3">
      <div class="flex w-full flex-col gap-3">
        <h3 class="text-md">
          Загрузить XML-файл с информацией об объекте
        </h3>
        <UInput
          class="w-full"
          type="file"
          @change="loadFile"
        />
      </div>
      <div
        v-if="xmlText.length > 0"
        class="flex w-full flex-col gap-3"
      >
        <h3 class="text-md">
          Предпросмотр загруженного файла
        </h3>
        <UTextarea
          v-model="xmlText"
          textarea-class="disabled:cursor-default"
          disabled
          :rows="25"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emits = defineEmits<{ loadXmlFile: [value: FormData] }>();

const xmlText = ref('');

async function loadFile(fileList: FileList) {
  xmlText.value = await fileList[0].text();

  const formData = new FormData();
  formData.append('file', fileList[0]);
  emits('loadXmlFile', formData);
}
</script>

<style scoped></style>
