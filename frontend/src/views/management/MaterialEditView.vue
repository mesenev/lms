<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
        <label>
          <input :class="`bx--text-input`" type="text" v-model="materialTittle">
        </label>
        <cv-button
          class="change__btn"
          :disabled="canChangeMaterialName"
          @click="ChangeMaterialName">
          Сменить название
        </cv-button>
      </div>
      <div class="bx--col-lg-10"></div>
      <div class="less bx--col-lg-8">
        <cv-text-area style="height: auto;" v-model="materialText"></cv-text-area>
      </div>
      <div class="less bx--col-lg-8">
        <div v-html="getMarkdownText"></div>
      </div>
      <cv-button class="change__btn" :disabled="canChangeMaterial" @click="ChangeMaterial">
        Изменить
      </cv-button>
    </div>
  </div>
</template>


<script lang="ts">
import Material from '@/components/Material.vue';
import LessonModel from '@/models/LessonModel';
import { lessonStore } from '@/store';
import _ from 'lodash';
import marked from 'marked';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Material } })
export default class MaterialEditView extends Vue {
  private store = lessonStore;
  @Prop() lessonId!: number;
  lesson!: LessonModel;
  materialTittle: string = this.materials.name;
  materialText: string = this.materials.content;

  async created() {
    this.lesson = await this.store.fetchLessonById(this.lessonId);
  }

  get materials() {
    return this.lesson.materials[0];
  }

  get getMarkdownText() {
    return marked(this.materialText);
  }

  get canChangeMaterialName() {
    return this.materials.name === this.materialTittle;
  }

  get canChangeMaterial() {
    return _.isEqual(this.materials.content, this.materialText)
  }

  ChangeMaterialName() {
    //
  }

  ChangeMaterial() {
    //
  }

}
</script>

<style scoped lang="stylus">
.less {
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)
  height auto
}

textarea,
#editor div {
  display: inline-block;
  width: 600px;
  height: 500px;
  vertical-align: top;
  box-sizing: border-box;
  padding: 0 20px;
}

textarea {
  background-color: #f6f6f6;
  font-size: 14px;
  font-family: "Monaco", courier, monospace;
  padding: 20px;
}

code {
  color: #f66;
}

</style>
