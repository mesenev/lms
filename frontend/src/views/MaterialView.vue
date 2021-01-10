<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
        <cv-tile>
          <h1>{{ materials.name }}</h1>
          <p>Материалы к уроку {{ lesson.name }}</p>
        </cv-tile>
      </div>
      <div class="bx--col-lg-10">
      </div>
      <div class="less bx--col-lg-10">
<!--        TODO: check that it's safe. (probably it's not and it should not be that way -->
        <div v-html="markdownText"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Material from '@/components/Material.vue';
import LessonModel from '@/models/LessonModel';
import { lessonStore } from '@/store';
import marked from 'marked';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Material } })
export default class MaterialView extends Vue {
  @Prop() lessonId!: number;
  store = lessonStore;
  lesson!: LessonModel;

  async created() {
    this.lesson = await this.store.fetchLessonById(this.lessonId);
  }

  get materials() {
    return this.lesson.materials[0];
  }

  get markdownText() {
    return marked(this.materials.text, { sanitize: true })
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
