<template>
  <router-link :to="{ name: 'ProblemView', params: { problemId: 1 }}">
    <span> {{ problem.name }}</span>
  </router-link>
</template>

<script>

import { Component, Vue, Prop } from 'vue-property-decorator';
import ProblemModel from '@/models/ProblemModel';

@Component
export default class Problem extends Vue {
  @Prop problemProp = ProblemModel;

  get problem() {
    return this.problemProp;
  }
}
</script>
// TO-DO Prop?
<style scoped lang="stylus">
</style>
