<template>
  <div class="bx--grid">
    <!-- TODO ссылка на задачу -->
    <cv-data-table title="Успеваемость урока" v-if="!loading" @sort="Sort">
      <template slot="helper-text">
        <router-link :to="{ name: 'LessonView', params: { lessonId: lesson.id } }"
                     tag="p" class="course--title">
          {{ les.name }}
        </router-link>
      </template>
      <template slot="actions">
        <cv-checkbox
          label="Не решали"
          value="value"
          v-model="dontSolved"/>
      </template>
      <template slot="headings">
        <cv-data-table-heading v-for="(column, id) in columns" :key="id" :sortable=isSortable(column.id)>
          <h5 v-if="(column.id === 0)">Результаты</h5>
          <h5 v-else-if="(column.id === -1)">Участник</h5>
          <cv-definition-tooltip v-else :definition="definition(column.id)" :term="column.name"/>
        </cv-data-table-heading>
      </template>
      <template slot="data">
        <cv-data-table-row v-for="user in progress" :key="user.id">
          <cv-data-table-cell>
            <router-link :to="{ name: 'profile-page', params: { userId: user.user} }"
                         class="course--title" tag="p">
              <UserComponent :user="user.user"/>
            </router-link>
          </cv-data-table-cell>
          <cv-data-table-cell class="mark"
                              v-for="lessonId in problems"
                              :key="lessonId.id">
            <submit-status v-if="userMarks(user, lessonId.id)"
                           :submit="create_submit(user.solved[lessonId.id][1],lessonId.id,user.user,user.solved[lessonId.id][0])"/>
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
import SubmitModel from "@/models/SubmitModel";
import UserModel from "@/models/UserModel";
import UserProgress from '@/models/UserProgress';
import lessonStore from "@/store/modules/lesson";
import problemStore from "@/store/modules/problem"
import progressStore from "@/store/modules/progress"
import userStore from '@/store/modules/user';
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import {Component, Prop, Vue} from 'vue-property-decorator';
import {Dictionary} from "vue-router/types/router";
import ProblemModel from "@/models/ProblemModel";

@Component({components: {SubmitStatus, UserComponent, UserAvatar20}})
export default class LessonProgressView extends Vue {
  @Prop() lessonId!: number;

  students: Array<UserProgress> = [];
  users: Dictionary<UserModel> = {};
  problems: Array<ProblemModel> = [];
  userStore = userStore;
  lessonStore = lessonStore;
  progressStore = progressStore;
  problemStore = problemStore;

  get columns() {
    const a = this.problems.map(l => (
      {
        id: l.id,
        name: l.name,
      }
    ))
    a.unshift({id: -1, name: "Ученики"})
    a.push({id: 0, name: "Рейтинг"})
    return a
  }

  get progress() {
    if (this.dontSolved) {
      return this.students.filter(x => Object.keys(x.solved).length === 0)
    }
    return this.students;
  }

  loading = true;
  sortable = true;
  dontSolved = false;

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
  };

  definition(column: number) {
    if (!this.loading && column != -1 && column != 0) {
      const pr = this.problems.filter((problem) => problem.id === column)
      column = pr[0].submits.filter(x => x.status === 'OK').length
    }
    return `Успешно решило ${column} из ${this.users.length} студентов`
  }

  create_submit(id: number, problemId: number, userid: number, status: string): SubmitModel {
    return {id: 1, problem: problemId, student: userid, status: status};
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
      obj => Object.assign({}, obj,
        {user: this.users[obj.user.toLocaleString()]}));
    this.loading = false;
  }

  userMarks(userId: UserProgress, lessonId: number) {
    return userId.solved[lessonId]
  }

  average(user: UserProgress): string {
    const solvedCount = Object.values(user.solved).filter(x => x == 'OK').length
    return Number(solvedCount / this.problems.length) * 100 + "%";
  }

  isSortable(column: number): boolean {
    return (!(column != 0 && column != -1));
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
        return (a.user.last_name > b.user.last_name) ? order : -1 * order;
      })
    } else {
      return this.students.sort((a, b) => {
        const A = Object.values(a.solved).filter(a => a == 'OK')
        const B = Object.values(b.solved).filter(b => b == 'OK')
        return (Object.keys(A).length > Object.keys(B).length) ? order : -1 * order
      })
    }
  }
}
</script>

<style scoped lang="stylus">
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
