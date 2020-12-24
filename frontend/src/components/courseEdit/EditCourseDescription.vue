<template>
  <div>
    <cv-text-input label="Описание курса" v-model.trim="courseDescription">
    </cv-text-input>
    <cv-button class="change__btn"
               :disabled="canChangeCourseDescription"
               @click="changeCourseDescription">
      Сменить описание
    </cv-button>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import CourseModel from '@/models/CourseModel';
import { mainStore } from '@/store';
import _ from 'lodash';

@Component({})
export default class EditCourseDescription extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  store = mainStore;

  courseDescription: string = this.course.description || '';

  get canChangeCourseDescription() {
    return _.isEqual(this.course.description || '', this.courseDescription);
  }

  changeCourseDescription() {
    this.store.changeCourseDescription(this.courseDescription);
  }
}
</script>

<style lang="stylus">

</style>
