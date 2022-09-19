<template>
  <transition mode="out-in" name="fade">
    <router-view v-if="lesson"/>
    <cv-loading v-else/>
  </transition>
</template>

<script lang="ts">
import LessonModel from '@/models/LessonModel';
import lessonStore from "@/store/modules/lesson";
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class LessonViewLayout extends Vue {
  @Prop({ required: true }) lessonId!: number;

  lesson: LessonModel | null = null;
  lessonStore = lessonStore;

  async created() {
    this.lessonStore.changeCurrentLesson(null);
    this.lesson = await this.lessonStore.fetchLessonById(this.lessonId);
    this.lessonStore.changeCurrentLesson(this.lesson);
    await this.lessonStore.fetchLessonsByCourseId(this.lesson.course);
  }

}

</script>
