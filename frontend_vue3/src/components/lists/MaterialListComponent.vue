<template>
  <cv-structured-list-data class="material-wrapper">
    <div class="material-click" @click="openHandler">
      <div class="material-container">
        <div class="material" :style="isUrl ? 'color: var(--cds-link-01);' : ''">
          <VideoChat24 v-if="isVideo" class="icon"/>
          <LicenseGlobal24 v-if="isUrl" class="icon"/>
          <Document24 v-if="isText" class="icon"/>
          <p>
            {{ material.name }}
          </p>
        </div>
        <div class="action-buttons">
          <component v-if="isStaff && showVisibility" :is="hiddenIcon" class="icon"/>
          <Checked16 v-if="isSelected" class="icon"/>
        </div>
      </div>
    </div>
  </cv-structured-list-data>
</template>

<script lang="ts" setup>
import Document24 from '@carbon/icons-vue/es/document/24';
import VideoChat24 from '@carbon/icons-vue/es/video--chat/24';
import TrashCan24 from '@carbon/icons-vue/es/trash-can/24';
import LicenseGlobal24 from '@carbon/icons-vue/es/license--global/24';
import Settings24 from '@carbon/icons-vue/es/settings/24';
import Checked16 from '@carbon/icons-vue/es/checkmark--filled/16';
import viewOff from '@carbon/icons-vue/es/view--off/24';
import view from '@carbon/icons-vue/es/view/24';
import type { PropType } from "vue";
import type { MaterialModel } from "@/models/MaterialModel";
import useMaterialStore from "@/stores/modules/material";
import { useRoute, useRouter } from "vue-router";
import { computed } from "vue";

const props = defineProps({
  materialProp: { type: Object as PropType<MaterialModel>, required: true },
  isStaff: { type: Boolean, required: false, default: false },
  isSelected: { type: Boolean, required: false, default: false },
  showVisibility: { type: Boolean, required: false, default: false }
})

const emits = defineEmits(['modal-hidden'])

const materialStore = useMaterialStore();

const router = useRouter();
const route = useRoute();

const isCurrentMaterialSelected = computed(() => {
  return route.params.hasOwnProperty('materialId') &&
      route.params['materialId'] === material.value.id.toString();
})

const isVideo = computed(() => {
  return material.value.content_type === 'video';
})

const isUrl = computed(() => {
  return material.value.content_type === 'url';
})

const isText = computed(() => {
  return material.value.content_type === 'text';
})

const hiddenIcon = computed(() => {
  return (material.value.is_teacher_only) ? viewOff : view;
})

const material = computed((): MaterialModel => {
  return props.materialProp;
})

async function openMaterial() {
  materialStore.setCurrentMaterial(material.value);
  await emits('modal-hidden');
  if (!isCurrentMaterialSelected.value)
    await router.push({
      name: 'MaterialView',
      params: { materialId: material.value.id.toString() }
    });
}

async function openHandler() {
  if (props.isStaff && !props.showVisibility) {
    await openMaterial();
  } else {
    openMaterialContent();
  }
}

function openMaterialContent() {
  if (material.value.content_type === 'url') {
    setContentUrl();
    addProtocolDomain();
    open(material.value.content);
  } else {
    openMaterial();
  }
}

function setContentUrl() {
  let contentUrl = material.value.content
  if (contentUrl.includes('href="')) {
    const subBegin = contentUrl.lastIndexOf('href="') + 6;
    const subEnd = contentUrl.indexOf('">');
    contentUrl = contentUrl.substring(subBegin, subEnd);
  }
  material.value.content = contentUrl;
}

function addProtocolDomain() {
  if (!material.value.content.includes('https://') && !material.value.content.includes('http://'))
    material.value.content = 'https://' + material.value.content;
}
</script>


<style scoped lang="stylus">
.material-container
  display flex
  justify-content space-between
  align-items center

.material-wrapper
  cursor pointer
  padding 0.5rem 0 0.5rem

.material-wrapper:hover
  background-color var(--cds-ui-02)

.material
  display flex
  flex-direction row

.action-buttons
  display flex
  align-content center

.icon
  margin-right 0.5rem
  margin-left 0.5rem
  cursor pointer

.material-title
  font-style oblique
  text-decoration-line underline
</style>
