<template>
  <div>
    <cv-text-input label="Название урока" v-model.trim="lessonTitle">
    </cv-text-input>
    <cv-button class="change-btn"
               :disabled="canChangeLessonName"
               @click="changeLessonName">
      Сменить название
    </cv-button>
  </div>
</template>

<script lang="ts">
import LessonModel from "@/models/LessonModel";
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component({})
export default class EditLessonName extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;

  lessonTitle: string = this.lesson.name;

  get canChangeLessonName() {
    return this.lessonTitle && _.isEqual(this.lesson.name, this.lessonTitle);
  }

  changeLessonName() {
 //
  }
}
</script>

<style lang="stylus">

</style>
