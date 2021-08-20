<template>
  <transition mode="out-in" name="fade">
    <router-view v-if="problem"/>
    <cv-loading v-else/>
  </transition>
</template>

<script lang="ts">
import ProblemDescription from "@/components/ProblemDescription.vue";
import SubmitComponent from '@/components/SubmitComponent.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import ProblemModel from '@/models/ProblemModel';
import problemStore from '@/store/modules/problem';
import submitStore from '@/store/modules/submit';
import { Component, Prop, Vue } from 'vue-property-decorator';
import SubmitModel from "@/models/SubmitModel";

@Component({ components: { SubmitComponent, ProblemDescription, SubmitStatus } })
export default class ProblemViewLayout extends Vue {
  @Prop({ required: true }) problemId!: number;
  problem: ProblemModel | null = null;
  private problemStore = problemStore;
  private submitStore = submitStore;

  async created() {
    this.problemStore.changeCurrentProblem(null);
    this.problem = await this.problemStore.fetchProblemById(this.problemId);
    this.problemStore.changeCurrentProblem(this.problem);
    this.submitStore.setSubmits(this.problemStore.currentProblem?.submits as SubmitModel[]);
  }
}
</script>

<style lang="stylus" scoped>
.item
  background-color var(--cds-ui-background)
  padding 1rem

.bx--row
  margin-bottom 1rem

.solution-container
  display flex

  &--submit-component
    flex 69%

  &--submit-list
    flex 30%

.name
  display flex
  flex-direction row
  justify-content space-between
  align-items center

.submit-list, .student-list
  margin 0
  padding 0

.student-list
  margin-left 1rem

.submit-btn, .handlers button
  margin-top 1rem


.submit
  display flex
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.problem-solution
  height 100%

.no-submits
  width 100%
  padding 0
  margin 0
  background-color inherit

.accepted, .rejected
  transition ease-in-out 0.25s

.accepted
  background-color var(--cds-inverse-support-02)

  &:hover
    background-color: var(--cds-support-02)

.rejected
  background-color var(--cds-inverse-support-01)

  &:hover
    background-color: var(--cds-support-01)

.text-area-student
.text-area-teacher
  border 1px solid black

.text-area-teacher textarea:disabled
  cursor pointer
  color #000

.problem-view
  margin-top: 2rem

.handlers
  button:nth-child(2n)
    margin-left 5px

.code
  .bx--text-area
    height 30em

  //width 45rem

  .bx--label,
  .bx--label--disabled
    display none

</style>
