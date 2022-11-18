<template>
  <div>
    <cv-inline-loading v-if="loading" state="loading"></cv-inline-loading>
    <div v-else-if="problems.length">
      <span>Решено задач: {{ solvedProblems }} из {{ problems.length }}</span>
      <div class="stats-graph">
        <span class="stat" v-for="problem in problems"
              :key="problem.id" :style="problemStatStyle(problem.id)"></span>
      </div>
    </div>
    <span v-else>Задачи отсутствуют</span>
  </div>
</template>

<script lang="ts">
import ProblemModel from "@/models/ProblemModel";
import { Component, Prop, Vue } from "vue-property-decorator";
import UserModel from "@/models/UserModel";
import SubmitModel from "@/models/SubmitModel";
import submitStore from "@/store/modules/submit";
import problemStore from "@/store/modules/problem";
import { Dictionary } from "vue-router/types/router";
import LessonModel from "@/models/LessonModel";

interface StatsGraphStyle {
  backgroundColor: string;
  width: string;
}

@Component({})
export default class LessonStatsGraph extends Vue{
  @Prop({required: true}) lesson!: LessonModel;
  @Prop({required: true}) user!: UserModel;
  submitStore = submitStore;
  problemStore = problemStore;
  problemsSubmits: Dictionary<SubmitModel[]> = {};
  _problems: ProblemModel[] = [];
  loading = true;

  wrongStyle: StatsGraphStyle = {
    backgroundColor: '#fc4848',
    width: `${1 / this.problemsCount * 100}%`,
  };
  successfulStyle: StatsGraphStyle = {
    backgroundColor: '#2ff306',
    width: `${1 / this.problemsCount * 100}%`,
  };
  testingStyle: StatsGraphStyle = {
    backgroundColor: '#fff300',
    width: `${1 / this.problemsCount * 100}%`,
  };
  withoutSolutionStyle: StatsGraphStyle = {
    backgroundColor: '#fcfbfb',
    width: `${1 / this.problemsCount * 100}%`,
  };

  async created() {
    this._problems = await this.problemStore.fetchProblemsByLessonId(this.lesson.id);
    for (const problem of this.problems) {
      this.problemsSubmits[problem.id] = await this.submitStore.fetchProblemStats(problem.id);
    }
    this.loading = false;
  }

  get problems() {
    return this._problems;
  }

  get problemsCount(): number {
    return this.lesson.problems.length;
  }

  get lessonStats(): Dictionary<string> {
    const stats: Dictionary<string> = {};
    for (const problem of this.problems) {
      if (this.problemsSubmits[problem.id].filter(x => x.status === 'OK' && x.student === this.user.id).length)
        stats[problem.id] = 'OK';
      else if (this.problemsSubmits[problem.id].filter(x => (x.status === 'AW' || x.status === 'NP') && x.student === this.user.id).length)
        stats[problem.id] = 'NP';
      else if (this.problemsSubmits[problem.id].filter(x => x.status === 'WA' && x.student === this.user.id).length)
        stats[problem.id] = 'WA'
      else
        stats[problem.id] = '';
    }
    return stats;
  }

  get solvedProblems() {
    return Object.values(this.lessonStats).filter(x => x === 'OK').length;
  }

  problemStatStyle(problemId: number) {
    if(this.lessonStats[problemId.toString()] === '')
      return this.withoutSolutionStyle;
    else if (this.lessonStats[problemId.toString()] === 'OK')
      return this.successfulStyle;
    else if (this.lessonStats[problemId.toString()] === 'NP')
      return this.testingStyle;
    else
      return this.wrongStyle;
  }

}
</script>

<style scoped lang="stylus">
.stats-graph
  margin-right 5px
  width 130px
  height 5px
  display flex
  background-color var(--cds-ui-01)

.stat
  border 0.3px solid var(--cds-ui-05)
</style>
