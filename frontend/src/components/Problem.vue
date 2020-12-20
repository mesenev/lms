<template>
  <!--TODO: padding for status of lesson and fix the the router open the same problem -->
  <cv-accordion-item>
    <template slot="title">
      <div v-on:click="openProblem">{{problem.name}}</div>
      <div class="aw">
        <cv-tag v-if="problem.completed"
                label = "OK"
                kind="green">
        </cv-tag>
        <cv-tag v-if="!problem.completed"
                label = "Не выполненно"
                kind="red">
        </cv-tag>
      </div>
    </template>
    <template slot="content">
      <p>{{problem.description}}</p>
    </template>
  </cv-accordion-item>
</template>

<script>

import { Component, Vue, Prop } from 'vue-property-decorator';
import ProblemModel from '@/models/ProblemModel';
import router from '@/router';

@Component
export default class Problem extends Vue {
  @Prop() problemProp = ProblemModel;

  openProblem() {
    router.push({ name: 'ProblemView', params: { problemId: this.problem.id.toString() } });
  }

  get problem() {
    return this.problemProp;
  }
}
</script>
<!-- TODO: Prop -->
<style scoped lang="stylus">
.aw
  text-align right
</style>
