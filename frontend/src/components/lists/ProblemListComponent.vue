<template xmlns:cv-tag="http://www.w3.org/1999/html">
  <!--TODO: padding for status of lesson and fix the the router open the same problem -->
  <cv-accordion-item class="accordion">
    <template slot="title">
      <div v-on:click="openProblem" class="title">
        {{ problem.name }}
        <div class="tags" v-if="!isStaff">
          <submit-status v-if="!!lastSubmit" :submit="lastSubmit" />
          <cv-tag v-else label="Не сдано" kind="red" ></cv-tag>
        </div>
      </div>
    </template>
    <template slot="content">
      <problem-stats v-if="isStaff" :problem="problemProp"/>
      <p v-else>{{ problem.description }}</p>
    </template>
  </cv-accordion-item>
</template>

<script lang="ts">
import ProblemStats from '@/components/ProblemStats.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import ProblemModel from '@/models/ProblemModel';
import userStore from '@/store/modules/user'

import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';
import SubmitModel from "@/models/SubmitModel";

@Component({ components: { ProblemStats, SubmitStatus } })
export default class ProblemListComponent extends Vue {
  @Prop() problemProp!: ProblemModel;

  userStore = userStore

  openProblem() {
    router.push({ name: 'ProblemView', params: { problemId: this.problem.id.toString() } });
  }

  get lastSubmit(): SubmitModel {
    return this.problemProp.success_or_last_submits
      .find((submit: SubmitModel) => submit.student === userStore.user.id)
  }

  get problem() {
    return this.problemProp;
  }

  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }
}
</script>
<!-- TODO: Prop -->
<style scoped lang="stylus">
.aw
  text-align right

.accordion /deep/ .bx--accordion__content
  padding-right 0

.title
  display flex
  align-items center
  justify-content space-between

</style>
