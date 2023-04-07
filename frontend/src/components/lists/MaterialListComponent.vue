<template>
  <cv-structured-list-data class="material-wrapper">
    <div class="material-click" @click="openHandler">
      <div class="material-container">
        <div class="material">
          <VideoChat24 v-if="this.materialProp.content_type === 'video'"
                       class="icon"/>
          <Document24 v-else class="icon"/>
          <p :class="(material.is_teacher_only) ? 'material-title' : ''">
            {{ material.name }}
          </p>
        </div>
        <div class="action-buttons" v-if="isStaff">

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
import Settings24 from '@carbon/icons-vue/es/settings/24';
import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';
import materialStore from '@/store/modules/material';

@Component({ components: { Document24, VideoChat24, TrashCan24, Settings24 } })
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
      this.addProtocolDomain();
      open(this.material.content, '_blank');
    } else {
      this.openMaterial();
    }
  }

  addProtocolDomain() {
    if (!this.material.content.includes('https://'))
      this.material.content = 'https://' + this.material.content;
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
