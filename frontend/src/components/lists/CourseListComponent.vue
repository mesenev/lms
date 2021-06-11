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
  <router-link
    :to="{ name: 'CourseView', params: { courseId: this.course.id.toString() } }"
    class="list-element">
    <h5 class="list-element--title">{{ course.name }}</h5>
    <span class="list-element--info">Преподаватель: {{ teacher }}</span>
    <span class="list-element--info">Следующий урок: {{ "24/1" }}</span>
  </router-link>
</template>

<style scoped lang="stylus">

</style>
