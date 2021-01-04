<template>
  <div>
    <cv-text-input label="Описание курса" v-model.trim="courseDescription">
    </cv-text-input>
    <cv-button class="change-btn"
               :disabled="canChangeCourseDescription"
               @click="changeCourseDescription">
      Сменить описание
    </cv-button>
  </div>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import { modBStore } from '@/store';
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({})
export default class EditCourseDescription extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  store = modBStore;

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
