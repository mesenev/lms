<script lang="ts">
import CourseModel from '@/models/CourseModel';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class CourseListComponent extends Vue {
  @Prop() courseProp!: CourseModel;


  get course(): CourseModel {
    return this.courseProp;
  }

  get teacher(): string {
    if (!this.course.author)
      return '';
    if (this.course.author.middle_name)
      return `${this.course.author.first_name} `
        + `${this.course.author.middle_name} `
        + `${this.course.author.last_name}`;
    return `${this.course.author.first_name} ${this.course.author.last_name}`;
  }
}
</script>

<template>
  <cv-link
    :to="{ name: 'CourseView', params: { courseId: this.course.id.toString() } }"
    class="course">
    <div>
      <h5>{{ course.name }}</h5>
      <span>Преподаватель: </span> {{ teacher }}<br>
      <span>Следующий урок:</span> 24/1
    </div>
  </cv-link>
</template>

<style scoped lang="stylus">
.course
  text-decoration none
  color black
  width 100%

</style>
