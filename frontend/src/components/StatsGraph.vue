<template>
  <div class="stats-graph">
    <span :style="successfulStyle">
    </span>
    <span :style="testingStyle">
    </span>
    <span :style="wrongStyle">
    </span>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { graphColor } from "@/common/colors";

interface StatsGraphStyle {
  backgroundColor: string;
  width: string;
}

@Component
export default class ProblemStats extends Vue {
  @Prop({}) successful!: number;
  @Prop({}) testing!: number;
  @Prop({}) wrong!: number;
  @Prop({}) size!: number;

  wrongStyle: StatsGraphStyle = {
    backgroundColor: graphColor['wrong'],
    width: `${this.wrong / this.size * 100}%`
  };

  successfulStyle: StatsGraphStyle = {
    backgroundColor: graphColor['successful'],
    width: `${this.successful / this.size * 100}%`
  };

  testingStyle: StatsGraphStyle = {
    backgroundColor: graphColor['testing'],
    width: `${this.testing / this.size * 100}%`
  };
}
</script>

<style lang="stylus" scoped>
  .stats-graph
    margin-right 5px
    width 100px
    display flex
    background-color var(--cds-ui-01)
</style>
