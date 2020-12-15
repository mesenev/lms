<template>
  <div>
    <h1>Список уроков</h1>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import CourseModel from '@/models/CourseModel';

@Component
export default class CourseView extends Vue {
  @Prop() courseId!: number;

  @Prop() courseProp!: CourseModel;
}
</script>

<style scoped>
</style>
