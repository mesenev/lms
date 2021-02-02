<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
        <cv-tile>
          <h1>{{ materials.name}}</h1>
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
import Material from '@/components/lists/MaterialListComponent.vue';
import LessonContent from "@/models/LessonContent";
import materialStore from '@/store/modules/material';
import MarkdownItVue from 'markdown-it-vue'
import 'markdown-it-vue/dist/markdown-it-vue.css'
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Material, MarkdownItVue } })
export default class MaterialView extends Vue {
  @Prop() materialId!: number;
  private materialStore = materialStore;
  material!: LessonContent;
  md = require('markdown-it');
  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    if (material) {
      this.materialStore.setCurrentMaterial(material);
    }
  }

  get materials(): LessonContent {
    return this.materialStore.currentMaterial;
  }

}
</script>

<style scoped lang="stylus">
.less
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

code
  color: var(--color-b)
</style>
