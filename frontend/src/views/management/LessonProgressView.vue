<template>
  <div class="bx--grid">
    <cv-data-table v-if="!loading" title="Успеваемость урока" @sort="Sort">
      <template slot="helper-text">
        <router-link :to="{ name: 'LessonView', params: { lessonId: lesson.id } }"
                     class="course--title" tag="p">
          {{ les.name }}
        </router-link>
      </template>
      <template slot="actions">
        <cv-checkbox
            v-model="dontSolved"
            label="Не решали"
            value="value"/>
      </template>
      <template slot="headings">
        <cv-data-table-heading v-for="(column, id) in columns" :key="id" :sortable=isSortable(column.id)>
          <h5 v-if="(column.id === 0)">Результаты</h5>
          <h5 v-else-if="(column.id === -2)">{{ column.name }}</h5>
          <div v-else @click="openSubmitOrProblem(column.id)">
            <cv-definition-tooltip :definition="definition(column.id)" :term="column.name"/>
          </div>
        </cv-data-table-heading>
      </template>
      <template slot="data">
        <cv-data-table-row v-for="user in progress" :key="user.id">
          <cv-data-table-cell>
            <router-link :to="{ name: 'profile-page', params: { userId: user.user.id } }"
                         class="course--title" tag="p">
              <UserComponent :userProp="user.user"/>
            </router-link>
          </cv-data-table-cell>
          <cv-data-table-cell v-for="problem in problems"
                              :key="problem.id"
                              class="mark">
            <div @click="openSubmitOrProblem(problem.id, user.solved[problem.type][problem.id][1])">
              <submit-status v-if="userMarks(user,problem.type,problem.id)"
                             :submit="create_submit(user.solved[problem.type][problem.id],problem.id,user.user)"/>
            </div>
          </cv-data-table-cell>
          <cv-data-table-cell>
            {{ average(user) }}
          </cv-data-table-cell>
        </cv-data-table-row>
      </template>
      >
    </cv-data-table>
    <cv-data-table-skeleton v-else :columns="2" :rows="6"/>
  </div>
</template>


<script lang="ts">
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from "@/components/UserComponent.vue";
import LessonModel from '@/models/LessonModel';
import ProblemModel from "@/models/ProblemModel";
import UserModel from "@/models/UserModel";
import UserProgress from '@/models/UserProgress';
import lessonStore from "@/store/modules/lesson";
import problemStore from "@/store/modules/problem"
import progressStore from "@/store/modules/progress"
import userStore from '@/store/modules/user';
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Dictionary } from "vue-router/types/router";

@Component({ components: { SubmitStatus, UserComponent, UserAvatar20 } })
export default class LessonProgressView extends Vue {
  @Prop() lessonId!: number;

  students: Array<UserProgress> = [];
  users: Dictionary<UserModel> = {};
  problems: Array<ProblemModel> = [];
  lesson: LessonModel = {
    id: NaN,
    course: NaN,
    description: '',
    name: '',
    problems: [],
    materials: [],
    deadline: '',
    lessonContent: '',
    is_hidden: true,
    progress: [],
    scores: {},
  };
  userStore = userStore;
  lessonStore = lessonStore;
  progressStore = progressStore;
  problemStore = problemStore;
  loading = true;
  sortable = true;
  dontSolved = false;

  get columns() {
    const a = this.problems.map(l => (
        {
          id: l.id,
          name: l.name,
        }
    ))
    a.unshift({ id: - 2, name: "Ученики" })
    a.push({ id: 0, name: "Рейтинг" })
    return a
  }

  get progress() {
    if (this.dontSolved) {
      return this.students.filter(x => Object.keys(x.solved["HW"]).length === 0)
    }
    return this.students;
  }

  get les() {
    return this.lesson;
  }

  async created() {
    this.lesson = await this.lessonStore.fetchLessonById(this.lessonId);
    this.students = await this.progressStore.fetchLessonProgressByLessonId(this.lessonId);
    this.users = await this.userStore.fetchStudentsByCourseId(this.lesson.course);
    this.problems = await this.problemStore.fetchProblemsByLessonId(this.lessonId);
    this.students = this.students.map(
        obj => Object.assign({}, obj, { user: this.users[obj.user.toLocaleString()] }));
    this.loading = false;
  }

  openSubmitOrProblem(problem: number, submit?: number) {
    if (submit)
      this.$router.push(`/course/${this.$route.params['courseId']}/lesson/${this.$route.params['lessonId']}/problem/${problem}/submit/${submit}`);
    else
      this.$router.push(`/course/${this.$route.params['courseId']}/lesson/${this.$route.params['lessonId']}/problem/${problem}`);
  }

  definition(column: number) {
    if (!this.loading && column != - 1 && column != 0) {
      const columnProblem = this.problems.filter((problem) => problem.id === column)[0].submits
      column = (columnProblem) ? columnProblem.filter(x => x.status === 'OK').length:0;
    }
    return `Успешно решило ${column} из ${this.progress.length} студентов`
  }

  create_submit(status_id: never, problemId: number, userid: number) {
    return {
      id: Object.values(status_id)[1],
      problem: problemId,
      student: Number(userid),
      status: Object.values(status_id)[0]
    }
  };

  userMarks(userId: UserProgress, problemType: string, problemId: number) {
    return userId.solved[problemType][problemId];
  }

  average(user: UserProgress): string {
    const c = this.problems.filter(x => x.type === "CW").map(function (num) {
      return num.id.toString();
    })
    const h = this.problems.filter(x => x.type === "HW").map(function (num) {
      return num.id.toString();
    })
    const e = this.problems.filter(x => x.type === "EX").map(function (num) {
      return num.id.toString();
    })
    let coefCW = this.lesson.scores['CW'];
    let coefHW = this.lesson.scores['HW'];
    if (c.length === 0) {
      coefHW = 100;
    }
    if (h.length === 0) {
      coefCW = 100;
    }

    let CWSolved = Object.keys(user.solved['CW']).filter(x => c.includes(x) && user.solved['CW'][x][0] === 'OK').length;
    let HWSolved = Object.keys(user.solved['HW']).filter(x => h.includes(x) && user.solved['HW'][x][0] === 'OK').length;
    let EXSolved = Object.keys(user.solved['EX']).filter(x => h.includes(x) && user.solved['EX'][x][0] === 'OK').length;
    CWSolved = (coefCW / c.length) * CWSolved;
    HWSolved = (coefHW / h.length) * HWSolved;
    EXSolved = (this.lesson.scores['EX'] / e.length) * EXSolved;
    let solvedCount = 0;
    solvedCount += (CWSolved != CWSolved) ? 0:CWSolved;
    solvedCount += (HWSolved != HWSolved) ? 0:HWSolved;
    solvedCount += (EXSolved != EXSolved) ? 0:EXSolved;
    return solvedCount + '%';
  }

  isSortable(column: number): boolean {
    return (!(column != 0 && column != - 1));
  }

  Sort(sortBy: { index: string; order: string }) {
    let order = - 1;
    if (sortBy.order == "none") {
      return this.students.sort((a, b) => {
        return a.id - b.id
      })
    }
    if (sortBy.order == "ascending") {
      order *= - 1;
    }
    if (sortBy.index == "0") {
      return this.students.sort((a, b) => {
        return (this.users[a.user].last_name > this.users[b.user].last_name) ? order:- 1 * order;
      })
    } else {
      return this.students.sort((a, b) => {
        const A = Object.values(a.solved['CW'] && a.solved['HW'] && a.solved['EX']).filter(a => a == 'OK')
        const B = Object.values(b.solved['CW'] && b.solved['HW'] && b.solved['EX']).filter(b => b == 'OK')
        return (Object.keys(A).length > Object.keys(B).length) ? order:- 1 * order
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.course--title
  color inherit
  cursor pointer
  display inline

.mark
  user-select none

.attendance
  display inline

  label
    display inline

.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

  .bx--structured-list-thead
    display none

.item
  min-height 85px
</style>
