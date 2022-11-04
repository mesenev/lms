<template>
  <cv-structured-list-data class="material-container">
    <div class="material">
      <VideoChat24 @click="openMaterial" v-if="this.materialProp.content_type === 'video'"
                   class="icon"/>
      <Document24 @click="openMaterial" v-else class="icon"/>
      <p @click="openMaterial">{{ material.name }}</p>
    </div>
    <TrashCan24 class="icon" @click="showConfirmModal"/>
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
  private materialStore = materialStore;

  openMaterial(): void {
    router.push({name: 'MaterialView', params: {materialId: this.material.id.toString()}});
  }

  showConfirmModal() {
    this.$emit('show-confirm-modal', this.material);
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

.icon
  margin-right 0.5rem
  cursor pointer

p
  display inline-flex
  cursor pointer
</style>
