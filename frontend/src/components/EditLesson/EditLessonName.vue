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
import { Component, Prop, Vue } from 'vue-property-decorator';
import { mainStore } from '@/store';
import LessonModel from "@/models/LessonModel";
import _ from 'lodash';

@Component({})
export default class EditLessonName extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;

  store = mainStore;

  lessonTitle: string = this.lesson.name;

  get canChangeLessonName() {
    return this.lessonTitle && _.isEqual(this.lesson.name, this.lessonTitle);
  }

  changeLessonName() {
    this.store.changeLessonName(this.lessonTitle);
  }
}
</script>

<style lang="stylus">

</style>
