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
        <cv-data-table-heading v-for="(column, id) in columns" :key="id" :sortable="sortable">
          <!-- Todo: переверстать по человечески -->
          <h5 v-if="(column.id === 0)">Результаты</h5>
          <h5 v-else-if="(column.id === -1)">Участник</h5>
          <cv-definition-tooltip v-else :definition="definition(column.id)" :term="column.name" />
        </cv-data-table-heading>
      </template>
      <template slot="data">
        <cv-data-table-row v-for="user in users" :key="user.id">
          <cv-data-table-cell>
            <!-- TODO ссылка на профиль -->
            <UserComponent :user="student(user.user)"/>
          </cv-data-table-cell>
          <cv-data-table-cell class="mark"
                              v-for="lessonId in les.problems"
                              :key="lessonId.id">
            <!-- TODO цвет в зависимости от оценки по-человечески -->
            <submit-status v-if="userMarks(user, lessonId.id)"
                          :submit="create_submit(lessonId.id,user.user,user.solved[lessonId.id])"/>
          </cv-data-table-cell>
          <cv-data-table-cell>
            {{ average(user) }}
          </cv-data-table-cell>
        </cv-data-table-row>
      </template>>
    </cv-data-table>
    <cv-data-table-skeleton v-else :columns="2" :rows="6"/>
  </div>
</template>


<script lang="ts">
import LessonModel from '@/models/LessonModel';
import UserProgress from '@/models/UserProgress';
import lessonStore from "@/store/modules/lesson";
import userStore from '@/store/modules/user';
import {Component, Prop, Vue} from 'vue-property-decorator';
import UserModel from "@/models/UserModel";
import {Dictionary} from "vue-router/types/router";
import UserComponent from "@/components/UserComponent.vue";
import SubmitModel from "@/models/SubmitModel";
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';

@Component({ components: {SubmitStatus, UserComponent, UserAvatar20} })
export default class LessonProgressView extends Vue {
  @Prop() lessonId!: number;

  students: Array<UserProgress> = [];
  users1: Dictionary<UserModel> = {};
  userStore = userStore;
  lessonStore = lessonStore;

  definition(a: number) {
    if (!this.loading && a!= -1 && a!= 0){
      const  pr = this.lesson.problems.filter((problem) => problem.id === a)
      a = pr[0].success_or_last_submits.filter(x => x.status === 'OK').length
    }
    return `Успешно решило ${a} из ${this.users.length} студентов`
  }
  create_submit(problemId: number, userid: number,status: string): SubmitModel{
    return { id:1, problem: problemId, student: userid, status: status};
  }
  begin = true;
  end = true;
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
    progress: [],
  };

  async created() {
    this.lesson = await this.lessonStore.fetchLessonById(this.lessonId);
    this.students = this.lesson.progress;
    this.users1 = await this.userStore.fetchStudentsByCourseId(this.lesson.course);
    this.loading = false;

  }

  student(id: number) {
    const a = this.users1[id];
    if (a){
      return a;
    }
  }

  get users() {
    if (this.dontSolved) {
      return this.students.filter(x => Object.keys(x.solved).length === 0)
    }
    return this.students;
  }

  get les() {
    return this.lesson;
  }

  get columns() {
    const a = this.les.problems.map(l => (
      {
        id: l.id,
        name: l.name
      }
    ))
    a.unshift({id:-1, name: "Ученики"})
    a.push({id:0, name: "Рейтинг"})
    return a

    //return [{'i': 'Ученики'}].concat('6',this.les.problems.map((l) => l.name).toLocaleString()).concat('Рейтинг');
  }

  userMarks(userId: UserProgress, lessonId: number) {
    return userId.solved[lessonId]
  }

  /*userAttendance(userId: number, lessonId: number) {
    // return this.users[userId].attendance[lessonId];
    return [];
  }

  changeAttendance(userId: number, lessonId: number) {
    //
  }*/

  average(user: UserProgress): string {
    //const sum = (marks: number[]) => marks.reduce((total, value) => total + value);
    //const { solved } = user;
    //return sum(solved) / solved.length;
    const a  = Object.fromEntries(Object.entries(user.solved).filter(([key, value]) => value === 'OK'))
    return  (Object.keys(a).length/this.les.problems.length)*100+"%";
  }

  Sort(sortBy: { index: string ; order: string}) {
    console.log(sortBy)
    if (sortBy.order == "ascending") {
          return this.students.sort((a, b) => {
      return Number(b.user) - Number(a.user);
    })
    }
    if(sortBy.order == "descending") {
          return this.students.sort((a, b) => {
      return Number(a.user) - Number(b.user);
    })
    }
    return this.students
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
