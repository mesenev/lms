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
        <div v-html="markdownText"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import marked from 'marked';
import Material from '@/components/Material.vue';
import LessonModel from '@/models/LessonModel';
import { modBStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Material } })
export default class MaterialView extends Vue {
  private store = modBStore;
  @Prop() lessonId!: number;

  get lesson(): LessonModel {
    return this.store.getLesson;
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
.less {
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)
}

code {
  color: var(--color-b)
}
</style>
