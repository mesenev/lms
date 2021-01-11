<template>
  <div class="bx--grid">
  </div>
</template>

<script lang="ts">
import Material from '@/components/Material.vue';
import { materialStore } from '@/store';
import marked from 'marked';
import { Component, Prop, Vue } from 'vue-property-decorator';
import LessonContent from "@/models/LessonContent";

@Component({ components: { Material } })
export default class MaterialView extends Vue {
  @Prop() materialId!: number;
  private materialStore = materialStore;
  material!: LessonContent;

  async created() {
    this.material = await this.materialStore.fetchMaterialById(this.materialId);
  }

  get materials(): LessonContent {
    return this.material;
  }

  get markdownText() {
    return marked(this.material.content, { sanitize: true })
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
