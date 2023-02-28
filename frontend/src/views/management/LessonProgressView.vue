<template>
  <div class="bx--grid">
    <div v-if="!loading">
      <div class="main-title">
        <h2>Успеваемость урока: {{ currentLesson.name }}</h2>
      </div>
      <div class="table-actions" v-if="progress.length">
        <cv-toggle v-model="dontSolved"
                   value="value">
          <template slot="text-left">Отображать только студентов без решений</template>
          <template slot="text-right">Отображать только студентов без решений</template>
        </cv-toggle>
        <div class="problem-type-dropdown">
          <cv-dropdown v-model="problemsType">
            <cv-dropdown-item value="CW" selected>Классная работа</cv-dropdown-item>
            <cv-dropdown-item value="HW">Домашняя работа</cv-dropdown-item>
            <cv-dropdown-item value="EW">Доп. задачи</cv-dropdown-item>
          </cv-dropdown>
        </div>
      </div>
      <div class="table-wrapper" v-if="progress.length">
        <cv-data-table @sort="Sort">
          <template slot="headings">
            <cv-data-table-heading class="fixed-col thead-element"
                                   v-for="(column, id) in columns" :key="id"
                                   :sortable="true">
              <h5 v-if="(column.id === 0)">Результаты</h5>
              <h5 v-else-if="(column.id === -2)">{{ column.name }}</h5>
              <div v-else @click="openSubmitOrProblem(column.id)">
                <cv-definition-tooltip :definition="definition(column.id)"
                                       :term="column.name"
                                       direction="bottom"/>
              </div>
            </cv-data-table-heading>
          </template>
          <template slot="data">
            <cv-data-table-row v-for="user in progress" :key="user.id">
              <cv-data-table-cell class="fixed-col">
                <router-link :to="{ name: 'profile-page', params: { userId: user.user } }"
                             class="course--title" tag="p">
                  <UserComponent :userId="user.user"/>
                </router-link>
              </cv-data-table-cell>
              <cv-data-table-cell v-for="problem in problems"
                                  :key="problem.id"
                                  class="mark tbody-element">
                <div
                  @click="openSubmitOrProblem(problem.id, user.solved[problem.type][problem.id][1])">
                  <submit-status v-if="userMarks(user,problem.type,problem.id)"
                                 :submit="create_submit(user.solved[problem.type][problem.id],problem.id,user.user)"/>
                </div>
              </cv-data-table-cell>
              <cv-data-table-cell>
                {{ average(user).toString() + '%' }}
              </cv-data-table-cell>
            </cv-data-table-row>
          </template>
          >
        </cv-data-table>
      </div>
      <empty-list-component v-else :text="emptyText" list-of="students"/>
    </div>
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
import submitStore from '@/store/modules/submit';
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Dictionary } from "vue-router/types/router";
import SubmitModel from "@/models/SubmitModel";
import EmptyListComponent from "@/components/EmptyListComponent.vue";

@Component({ components: { EmptyListComponent, SubmitStatus, UserComponent, UserAvatar20, } })
export default class LessonProgressView extends Vue {
  @Prop() lessonId!: number;

  students: Array<UserProgress> = [];
  users: Dictionary<UserModel> = {};
  _problems: Array<ProblemModel> = [];
  submits: Dictionary<SubmitModel[]> = {};
  lesson: LessonModel = {
    id: NaN,
    course: NaN,
    description: '',
    name: '',
    problems: [],
    exams: [],
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
  submitStore = submitStore;
  loading = true;
  dontSolved = false;
  problemsType = '';
  emptyText = '';

  get columns() {
    const a = this.problems.map(l => (
      {
        id: l.id,
        name: l.name,
      }
    ))
    a.unshift({ id: -2, name: "Ученики" })
    a.push({ id: 0, name: "Рейтинг" })
    return a
  }

  get problems() {
    return this._problems.filter(x => x.type === this.problemsType);
  }

  get progress() {
    if (this.dontSolved) {
      return this.students.filter(x => Object.keys(x.solved[this.problemsType]).length === 0)
    }
    return this.students;
  }

  get currentLesson() {
    return this.lesson;
  }

  async created() {
    this.lesson = await this.lessonStore.fetchLessonById(this.lessonId);
    this.users = await this.userStore.fetchStudentsByCourseId(this.lesson.course);
    this._problems = await this.problemStore.fetchProblemsByLessonId(this.lessonId);
    for (const problem of this._problems) {
      this.submits[problem.id] = await this.submitStore.fetchProblemStats(problem.id);
    }
    this.students = (await this.progressStore.fetchLessonProgressByLessonId(this.lessonId));
    this.emptyText = 'Ни один студент не записан на курс';
    this.loading = false;
  }

  openSubmitOrProblem(problem: number, submit?: number) {
    if (submit)
      this.$router.push(`/course/${this.$route.params['courseId']}/lesson/${this.$route.params['lessonId']}/problem/${problem}/submit/${submit}`);
    else
      this.$router.push(`/course/${this.$route.params['courseId']}/lesson/${this.$route.params['lessonId']}/problem/${problem}`);
  }

  definition(column: number) {
    if (!this.loading && column != -2 && column != 0) {
      const columnProblem = this.problems.filter((problem) => problem.id === column)[0]
      column = (columnProblem) ? (columnProblem.stats ? columnProblem.stats.green : 0) : 0;
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

  average(user: UserProgress): number {
    const problemIds = this.problems.filter(x => x.type === this.problemsType).map(x => x.id);
    let solvedCount = 0;

    for (const submits of Object.values(this.submits)) {
      solvedCount += submits.filter(
        x => x.student === user.user && x.status === 'OK' && problemIds.includes(x.problem.id)
      ).length ? 1 : 0;
    }
    const averageResult = (solvedCount / problemIds.length) * 100;

    return problemIds.length ? Math.trunc(averageResult) : 0;
  }

  Sort(sortBy: { index: string; order: string }) {
    let order = -1;
    if (sortBy.order == "none") {
      return this.students.sort((a, b) => {
        return a.id - b.id
      })
    }
    if (sortBy.order == "ascending") {
      order *= -1;
    }
    if (sortBy.index == "0") {
      return this.students.sort((a, b) => {
        return (this.users[a.user].last_name > this.users[b.user].last_name) ? order : -1 * order;
      })
    } else if (sortBy.index == (this.columns.length - 1).toString()) {
      return this.students.sort((a, b) => {
        return (this.average(a) > this.average(b) ? order : -1 * order);
      })
    } else {
      const solved = this.students.filter(x => x.solved[this.problemsType][sortBy.index]).sort((a, b) => {
        const aSolutions = a.solved[this.problemsType][sortBy.index];
        const bSolutions = b.solved[this.problemsType][sortBy.index];
        const A = aSolutions[0] === 'OK' ? 1 : (aSolutions[0] === 'NP' ? 0 : -1);
        const B = bSolutions[0] === 'OK' ? 1 : (bSolutions[0] === 'NP' ? 0 : -1);
        return (A > B) ? order : -1 * order;
      })
      return this.students = solved.concat(this.students.filter(x => !x.solved[this.problemsType][sortBy.index]));
    }
  }
}
</script>

<style lang="stylus" scoped>
.main-title
  margin-left 0
  margin-bottom 0

.table-actions
  display flex
  flex-direction row

.problem-type-dropdown
  width fit-content

/deep/ .bx--list-box__field
  display flex

.table-wrapper
  margin-top 1rem
  border 0.5px solid var(--cds-ui-05)
  border-collapse separate
  overflow-x auto
  width 100%

/deep/ table
  text-align-last center
  border-collapse separate

/deep/ th
  padding-top 0.5rem
  padding-bottom 0.5rem

.tbody-element, .fixed-col
  border-right 0.5px solid var(--cds-ui-05)
  z-index 0

.fixed-col:first-child
  text-align-last left
  z-index 2
  position sticky
  left 0

.fixed-col:last-child
  border-right none

/deep/ .bx--data-table-container
  padding-top 0

.mark
  user-select none

/deep/ .tag
  cursor pointer

.user-component
  cursor pointer

/deep/ .empty-list-wrapper
  margin-top 5rem
  text-align center

  h4
    font-size var(--cds-productive-heading-04-font-size)

  p
    font-size var(--cds-productive-heading-03-font-size)

.attendance
  display inline

  label
    display inline

</style>
