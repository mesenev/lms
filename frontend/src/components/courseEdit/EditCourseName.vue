<template>
  <div>
    <cv-text-input label="Название курса" v-model.trim="courseTitle">
    </cv-text-input>
    <cv-button class="change__btn"
               :disabled="canChangeCourseName"
               @click="changeCourseName">
      Сменить название
    </cv-button>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { mainStore } from '@/store';
import CourseModel from '@/models/CourseModel';
import _ from 'lodash';

@Component({})
export default class EditCourseName extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  store = mainStore;

  courseTitle: string = this.course.name;

  get canChangeCourseName() {
    return this.courseTitle && _.isEqual(this.course.name, this.courseTitle);
  }

  changeCourseName() {
    this.store.changeCourseName(this.courseTitle);
  }
}
</script>

<style lang="stylus">

</style>
