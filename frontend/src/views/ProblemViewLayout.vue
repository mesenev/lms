<template>
  <transition mode="out-in" name="fade">
    <router-view v-if="problem"/>
    <div class="loading-out" v-else>
      <cv-loading />
    </div>
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
.loading-out
  display flex
  width 100%;
  height 100%;
  align-items center;
  justify-content center;

</style>
