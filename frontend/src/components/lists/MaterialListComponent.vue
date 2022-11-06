<template>
  <cv-structured-list-data class="material-container">
    <div class="material">
      <VideoChat24 @click="openMaterial" v-if="this.materialProp.content_type === 'video'"
                   class="icon"/>
      <Document24 @click="openMaterial" v-else class="icon"/>
      <p @click="openMaterial" :class="(material.is_teacher_only) ? 'material-title' : ''">
        {{ material.name }}
      </p>
    </div>
    <div class="action-buttons" v-if="isEditing">
      <a v-if="!inAction"
         class="visibility-button icon"
         @click="changeMaterialVisibility">
        {{ this.material.is_teacher_only ? 'Материал для учителя' : 'Материал для студентов' }}
      </a>
      <TrashCan24 class="icon" @click="showConfirmModal"/>
    </div>
  </cv-structured-list-data>
</template>

<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import Document24 from '@carbon/icons-vue/es/document/24';
import VideoChat24 from '@carbon/icons-vue/es/video--chat/24';
import TrashCan24 from '@carbon/icons-vue/es/trash-can/24';
import router from '@/router';
import {Component, Prop, Vue} from 'vue-property-decorator';
import materialStore from '@/store/modules/material';

@Component({components: {Document24, VideoChat24, TrashCan24}})
export default class MaterialListComponent extends Vue {
  @Prop() materialProp!: MaterialModel;
  @Prop({required: false}) isEditing!: false | boolean;
  private materialStore = materialStore;
  inAction = false;

  openMaterial(): void {
    this.materialStore.setCurrentMaterial(this.material);
    router.push({name: 'MaterialView', params: {materialId: this.material.id.toString()}});
  }

  showConfirmModal() {
    this.$emit('show-confirm-modal', this.material);
  }

  async changeMaterialVisibility() {
    this.inAction = true;
    await this.materialStore.patchMaterialVisibility({
      is_teacher_only: !this.materialProp.is_teacher_only,
      id: this.materialProp.id
    });
    this.inAction = false;
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
  padding 0.5rem 0 0.5rem
  align-items center

.material
  display flex
  flex-direction row

.action-buttons
  display flex
  align-content center

.icon
  margin-right 0.5rem
  cursor pointer

.material-title
  font-style oblique
  text-decoration-line underline

p
  display inline-flex
  cursor pointer
</style>
