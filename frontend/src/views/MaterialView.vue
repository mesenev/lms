<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
        <cv-tile>
          <h1 class="material-title">{{ materials.name}}</h1>
        </cv-tile>
      </div>
      <div class="bx--col-lg-10">

      </div>
      <div class="less bx--col-lg-10">
        <MarkdownItVue class="md-body" :content="materials.content"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import materialStore from '@/store/modules/material';
import MarkdownItVue from 'markdown-it-vue'
import 'markdown-it-vue/dist/markdown-it-vue.css'
import { Component, Prop } from 'vue-property-decorator';
import Vue, { VueConstructor } from 'vue';


@Component({ components: { MarkdownItVue: MarkdownItVue as VueConstructor<Vue>  } })
export default class MaterialView extends Vue {
  @Prop() materialId!: number;
  private materialStore = materialStore;
  material!: MaterialModel;

  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    if (material) {
      this.materialStore.setCurrentMaterial(material);
    }
  }

  get materials(): MaterialModel {
    return this.materialStore.currentMaterial;
  }

}
</script>

<style scoped lang="stylus">

.material-title
  margin-top 2rem

.less
  border 1px solid rgba(0,0,0,.3)
  margin-left 2rem
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)
  min-height 10rem

code
  color: var(--color-b)
</style>
