<template>
  <cv-structured-list-data class="material">
    <Catalog20 class="icon" />
    <p @click="openMaterial">{{ material.name }}</p>
  </cv-structured-list-data>
</template>

<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import Catalog20 from '@carbon/icons-vue/es/catalog/20';
import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Catalog20 } })
export default class MaterialListComponent extends Vue {
  @Prop() materialProp!: MaterialModel;

  openMaterial(): void {
    router.push({ name: 'MaterialView', params: { materialId: this.material.id.toString() } });
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
  .icon
    margin-right 0.5rem
  p
    display inline-flex
    cursor pointer
</style>
