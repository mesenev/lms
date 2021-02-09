<template>
  <div class="course" v-on:click="openLesson">
    <cv-structured-list-data class="title">
      <h5>{{ lesson.name }}</h5>
      <span>Количество задач: {{ lesson.problems.length }}</span>
      <span>Дедлайн: {{ lesson.deadline }}</span>
    </cv-structured-list-data>
    <!-- ToDo get statistic -->
  </div>
</template>

<script lang="ts">
import LessonModel from "@/models/LessonModel";
import userStore from '@/store/modules/user';
import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class LessonListComponent extends Vue {
  @Prop({ required: true }) lessonProp!: LessonModel;

  userStore = userStore;

  openLesson(): void {
    router.push({ name: 'LessonView', params: { lessonId: this.lesson.id.toString() } });
  }

  get lesson(): LessonModel {
    return this.lessonProp;
  }

  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }
}
</script>

<style scoped lang="stylus">
.course
  display flex
  flex-direction row
  justify-content space-between

.title
  display flex
  flex-direction column
</style>
