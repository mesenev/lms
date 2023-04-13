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
        <div class="action-buttons" v-if="isStaff">
          <component :is="hiddenIcon" class="icon"/>
        </div>
      </div>
    </div>
  </cv-structured-list-data>
</template>

<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import Document24 from '@carbon/icons-vue/es/document/24';
import VideoChat24 from '@carbon/icons-vue/es/video--chat/24';
import TrashCan24 from '@carbon/icons-vue/es/trash-can/24';
import LicenseGlobal24 from '@carbon/icons-vue/es/license--global/24';
import Settings24 from '@carbon/icons-vue/es/settings/24';
import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';
import materialStore from '@/store/modules/material';
import viewOff from '@carbon/icons-vue/es/view--off/24';
import view from '@carbon/icons-vue/es/view/24';

@Component({ components: { Document24, VideoChat24, TrashCan24, Settings24, LicenseGlobal24 } })
export default class MaterialListComponent extends Vue {
  @Prop() materialProp!: MaterialModel;
  @Prop({ required: false, default: false }) isStaff!: boolean;
  private materialStore = materialStore;

  async openMaterial() {
    this.materialStore.setCurrentMaterial(this.material);
    await this.$emit('modal-hidden');
    await router.push({
      name: 'MaterialView',
      params: { materialId: this.material.id.toString() }
    });
  }

  async openHandler() {
    if (this.isStaff) {
      await this.openMaterial();
    } else {
      this.openMaterialContent();
    }
  }

  openMaterialContent() {
    if (this.material.content_type === 'url') {
      this.setContentUrl();
      this.addProtocolDomain();
      open(this.material.content);
    } else {
      this.openMaterial();
    }
  }

  setContentUrl() {
    let contentUrl = this.material.content
    if (contentUrl.includes('href="')) {
      const subBegin = contentUrl.lastIndexOf('href="') + 6;
      const subEnd = contentUrl.indexOf('">');
      contentUrl = contentUrl.substring(subBegin, subEnd);
    }
    this.material.content = contentUrl;
  }

  addProtocolDomain() {
    if (!this.material.content.includes('https://') && !this.material.content.includes('http://'))
      this.material.content = 'https://' + this.material.content;
  }

  get isVideo() {
    return this.material.content_type === 'video';
  }

  get isUrl() {
    return this.material.content_type === 'url';
  }

  get isText() {
    return this.material.content_type === 'text';
  }

  get hiddenIcon() {
    return (this.material.is_teacher_only) ? viewOff : view;
  }

  get material(): MaterialModel {
    return this.materialProp;
  }
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
