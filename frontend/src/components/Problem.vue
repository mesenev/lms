<template xmlns:cv-tag="http://www.w3.org/1999/html">
  <!--TODO: padding for status of lesson and fix the the router open the same problem -->
  <cv-accordion-item>
    <template slot="title">
      <div v-on:click="openProblem">{{problem.name}}
        <cv-tag :label = problemStatus[0]
                :kind = problemStatus[1]>
        </cv-tag>
        <cv-tag :label = problemStatus[2]
                kind="gray">
        </cv-tag>
      </div>
    </template>
    <template slot="content">
      <p>{{problem.description}}</p>
    </template>
  </cv-accordion-item>
</template>

<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import ProblemModel from '@/models/ProblemModel';
import router from '@/router';

@Component
export default class Problem extends Vue {
  @Prop() problemProp!: ProblemModel;

  openProblem() {
    router.push({ name: 'ProblemView', params: { problemId: this.problem.id.toString() } });
  }

  get problem() {
    return this.problemProp;
  }
  get problemStatus() {
    const status = [];
    (this.problem.completed) ? status.push("OK","green"): status.push("Не выполнено","red");
    (this.problem.manual) ? status.push("РУЧН"): status.push("АВТ");
    return status;
  }

}
</script>
<!-- TODO: Prop -->
<style scoped lang="stylus">
.aw
  text-align right
</style>
