<template>
  <div class="stats-graph">
    <span :style="wrongStyle"></span>
    <span :style="testingStyle"></span>
    <span :style="successfulStyle"></span>
    <span :style="withoutSolutionStyle"></span>
  </div>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import { ProblemStatsModel } from '@/models/ProblemModel';
import { Component, Prop, Vue } from "vue-property-decorator";
import { graphColor } from "@/common/colors";
import courseStore from '@/store/modules/course';

interface StatsGraphStyle {
  backgroundColor: string;
  width: string;
}

@Component
export default class StatsGraph extends Vue {
  @Prop() stats!: ProblemStatsModel;

  courseStore = courseStore;
  size = this.successful + this.testing + this.wrong + this.withoutSolution;
  wrongStyle: StatsGraphStyle = {
    backgroundColor: '#fc4848',
    width: `${this.wrong / this.size * 100}%`,
  };
  successfulStyle: StatsGraphStyle = {
    backgroundColor: '#2ff306',
    width: `${this.successful / this.size * 100}%`,
  };
  testingStyle: StatsGraphStyle = {
    backgroundColor: '#ddf902',
    width: `${this.testing / this.size * 100}%`,
  };
  withoutSolutionStyle: StatsGraphStyle = {
    backgroundColor: '#fcfbfb',
    width: `${this.testing / this.size * 100}%`,
  };

  get successful() {
    return this.stats.green;
  }

  get testing() {
    return this.stats.yellow;
  }

  get wrong() {
    return this.stats.red;
  }

  get withoutSolution() {
    return (this.courseStore.currentCourse as CourseModel).students.length
      - (this.successful + this.testing + this.wrong);
  }
}
</script>

<style lang="stylus" scoped>
.stats-graph
  margin-right 5px
  width 110px
  height: 6px
  display flex
  background-color var(--cds-ui-01);
  border: 1px solid #e8e8e8;
</style>
