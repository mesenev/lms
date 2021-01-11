<script lang="ts">
import CourseModel from '@/models/CourseModel';
import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Course extends Vue {
  @Prop() courseProp!: CourseModel;

  openCourse(): void {
    router.push({ name: 'CourseView', params: { courseId: this.course.id.toString() } });
  }

  get course(): CourseModel {
    return this.courseProp;
  }
}
</script>

<template>
  <div class="course" v-on:click="openCourse">
    <h5>{{ course.name }}</h5>
    <span>Преподаватель: </span> Сущенко Андрей Андреевич <br>
    <span>Следующий урок:</span> 24/1
  </div>
</template>

<style scoped lang="stylus">
.course
  padding 20px
</style>
