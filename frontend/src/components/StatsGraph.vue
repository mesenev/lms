<template>
  <div>
    <cv-inline-loading v-if="loading" state="loading"></cv-inline-loading>
    <div v-else>
      <div class="stats-graph">
        <span class="stat" v-for="student in students"
              :key="student.id" :style="submitStatusStyle(student)"></span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import ProblemModel from '@/models/ProblemModel';
import { Component, Prop, Vue } from "vue-property-decorator";
import courseStore from '@/store/modules/course';
import userStore from '@/store/modules/user';
import submitStore from '@/store/modules/submit';
import SubmitModel from "@/models/SubmitModel";
import { Dictionary } from "vue-router/types/router";
import UserModel from "@/models/UserModel";

interface StatsGraphStyle {
  backgroundColor: string;
  width: string;
}

@Component({})
export default class StatsGraph extends Vue {
  @Prop({required: true}) problem!: ProblemModel;
  userStore = userStore;
  submitStore = submitStore;
  courseStore = courseStore;
  _submits: SubmitModel[] = [];
  usersWithSubmits: number[] = [];
  loading = true;

  wrongStyle: StatsGraphStyle = {
    backgroundColor: '#fc4848',
    width: `${1 / this.studentsCount * 100}%`,
  };
  successfulStyle: StatsGraphStyle = {
    backgroundColor: '#2ff306',
    width: `${1 / this.studentsCount * 100}%`,
  };
  testingStyle: StatsGraphStyle = {
    backgroundColor: '#fff300',
    width: `${1 / this.studentsCount * 100}%`,
  };
  withoutSolutionStyle: StatsGraphStyle = {
    backgroundColor: 'var(--cds-ui-01)',
    width: `${1 / this.studentsCount * 100}%`,
  };

  async created() {
    this._submits = await this.submitStore.fetchProblemStats(this.problem.id);
    this.usersWithSubmits = this.submits.map(x => x.student);
    this.loading = false;
  }

  get students(): Dictionary<UserModel> {
    return this.userStore.currentCourseStudents;
  }

  get studentsCount(): number {
    return Object.keys(this.students).length;
  }

  get submits(): SubmitModel[] {
    return this._submits.filter(x => this.students[x.student] !== undefined);
  }

  get noSubmitsUsers(): Array<UserModel> {
    return Object.keys(this.students)
      .filter(x => !(this.usersWithSubmits.includes(Number(x))))
      .map(x => this.students[x]);
  }

  isSuccessfulStatus(studentId: number) {
    return this.submits.filter(x => x.status === "OK" && x.student === studentId).length > 0;
  }

  isTestingStatus(studentId: number) {
    return this.submits.filter(
      x => (x.status === 'AW' || x.status === 'NP') && x.student === studentId
    ).length > 0;
  }

  submitStatusStyle(student: UserModel) {
    if (this.isWithoutSolution(student))
      return this.withoutSolutionStyle;
    else if (this.isSuccessfulStatus(student.id))
      return this.successfulStyle;
    else if (this.isTestingStatus(student.id))
      return this.testingStyle;
    return this.wrongStyle;
  }

  isWithoutSolution(student: UserModel) {
    return this.noSubmitsUsers.includes(student);
  }
}
</script>

<style lang="stylus" scoped>
.stats-graph
  margin-right 5px
  width 130px
  height 5px
  display flex
  background-color var(--cds-ui-01)

.stat
  border 0.3px solid var(--cds-ui-05)
</style>
