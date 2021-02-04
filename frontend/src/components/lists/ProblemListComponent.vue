<template xmlns:cv-tag="http://www.w3.org/1999/html">
  <!--TODO: padding for status of lesson and fix the the router open the same problem -->
  <cv-accordion-item class="accordion">
    <template slot="title">
      <div v-on:click="openProblem">{{ problem.name }}
        <cv-tag :kind=problemStatus[1]
                :label=problemStatus[0]>
        </cv-tag>
        <cv-tag :label=problemStatus[2]
                kind="gray">
        </cv-tag>
      </div>
    </template>
    <template slot="content">
      <problem-stats :problem="problemProp"/>
    </template>
  </cv-accordion-item>
</template>

<script lang="ts">
import ProblemStats from '@/components/ProblemStats.vue';
import ProblemModel from '@/models/ProblemModel';
import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { ProblemStats } })
export default class ProblemListComponent extends Vue {
  @Prop() problemProp!: ProblemModel;

  openProblem() {
    router.push({ name: 'ProblemView', params: { problemId: this.problem.id.toString() } });
  }

  get problem() {
    return this.problemProp;
  }

  get problemStatus() {
    const status = [];
    (this.problem.completed) ? status.push("OK", "green") : status.push("Не выполнено", "red");
    (this.problem.manual) ? status.push("РУЧН") : status.push("АВТ");
    return status;
  }

}
</script>
<!-- TODO: Prop -->
<style scoped lang="stylus">
.aw
  text-align right

.accordion /deep/ .bx--accordion__content
  padding-right 0
</style>
