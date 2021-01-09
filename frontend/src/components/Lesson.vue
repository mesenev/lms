<script lang="ts">
import LessonModel from "@/models/LessonModel";
import ProblemModel from "@/models/ProblemModel";
import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Course extends Vue {
  @Prop({required: true}) lessonProp!: LessonModel;

  openLesson(): void {
    router.push({ name: 'LessonView', params: { lessonId: this.lesson.id.toString() } });
  }

  get lesson(): LessonModel {
    return this.lessonProp;
  }

  completed(learning: Array<ProblemModel>) {
    const completed = learning.filter((l) => l.completed).length;
    const all = learning.length;
    return (100 * (completed / all)).toFixed(0).toString().concat('%');
  }

  count(lesson: LessonModel) {
    const c = lesson.problems.concat(lesson.problems).length;
    const check = (c: number) => !(c % 2);
    return check(c) ? c + " задач" : c + " задачи";
  }
}
</script>

<template>
  <div class="course" v-on:click="openLesson">
    <cv-structured-list-data>
      <h5>{{ lesson.name }}</h5>
      <span> {{ count(lesson) }}<br></span>
      <span> Дедлайн: </span> {{ lesson.deadline }}
    </cv-structured-list-data>
    <cv-structured-list-data>
    </cv-structured-list-data>
    <cv-structured-list-data class="progress">
      <span>Прогресс:{{ completed(lesson.problems.concat(lesson.problems)) }}</span>
    </cv-structured-list-data>

  </div>
</template>

<style scoped lang="stylus">
</style>
