<template>
  <div>
    <router-link :to="target(exam)" class="list-element" v-for="exam in examsList" :key="exam.id">
      <div class="content-wrapper">
        <div class="title-wrapper">
          <h5 class="list-element--title"> {{ exam.name }} </h5>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script lang="ts">
import ExamModel from "@/models/ExamModel";
import { Component, Prop, Vue } from 'vue-property-decorator';
import solutionStore from '@/store/modules/solution';

@Component({ components: {} })
export default class ExamListComponent extends Vue {
  @Prop({ required: true }) examsList!: Array<ExamModel>;
  @Prop({ required: false }) isStaff!: boolean;
  solutionStore = solutionStore;

  target(exam: ExamModel) {
    if (this.isStaff && this.solutionStore.solutions)
      return {
        name: 'ExamViewWithSolution', params: {
          courseId: this.$route.params.courseId,
          lessonId: this.$route.params.lessonId,
          examId: exam.id.toString(),
          solutionId: this.solutionStore.solutions[this.solutionStore.solutions.length - 1].id.toString(),
        }
      }
    return { name: 'ExamView', params: { examId: exam.id.toString() } };
  }
}
</script>

<style scoped lang="stylus">
.list-element
  display flex
  flex-direction row
  justify-content space-between
  align-items center
  border-top 1px solid var(--cds-ui-03)
  border-bottom 1px solid var(--cds-ui-03)

.list-element:hover
  background-color var(--cds-ui-03)

.cv-tag
  display flex
  align-items stretch
  margin-right 1rem
</style>
