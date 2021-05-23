<template>
  <cv-structured-list-data class="material">
    <VideoChat24 v-if="this.materialProp.content_type === 'video'" class="icon_video"/>
    <Document24 v-else class="icon_text"/>
    <p @click="openMaterial">{{ material.name }}</p>
  </cv-structured-list-data>
</template>

<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import Document24 from '@carbon/icons-vue/es/document/24';
import VideoChat24 from '@carbon/icons-vue/es/video--chat/24';
import router from '@/router';
import {Component, Prop, Vue} from 'vue-property-decorator';
import materialStore from '@/store/modules/material';

@Component({components: {Document24, VideoChat24}})
export default class MaterialListComponent extends Vue {
  @Prop() materialProp!: MaterialModel;
  private materialStore = materialStore;

  openMaterial(): void {
    router.push({name: 'MaterialView', params: {materialId: this.material.id.toString()}});
  }

  get material(): MaterialModel {
    return this.materialProp;
  }
}
</script>


<style scoped lang="stylus">
.material
  display flex
  flex-direction row
  align-items center
  padding 0.5rem 0 0.5rem 1rem

  .icon_video
    margin-right 0.5rem

  .icon_text
    margin-right 0.5rem
    size 1rem

  p
    display inline-flex
    cursor pointer
</style>
