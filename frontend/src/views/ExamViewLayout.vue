<template>
  <transition mode="out-in" name="fade">
    <router-view v-if="exam" :key="$route.params.examId"/>
    <div v-else class="loading-out">
      <cv-loading />
    </div>
  </transition>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import ExamModel from "@/models/ExamModel";
import examStore from '@/store/modules/exam';

@Component({components: {}})
export default class ExamViewLayout extends Vue {
  @Prop({required: true}) examId!: number;

  exam: ExamModel | null = null;
  examStore = examStore;

  async created() {
    this.examStore.changeCurrentExam(null);
    this.exam = await this.examStore.fetchExamById(this.examId);
    this.examStore.changeCurrentExam(this.exam);
    await this.examStore.fetchExamsByLessonId(this.exam.lesson);
  }
}
</script>

<style scoped>

</style>
