<template>
  <div class="bx--grid">
    <!-- TODO ссылка на задачу -->
    <cv-data-table title="Успеваемость курса" v-if="!loading">
      <template slot="helper-text">
        <router-link :to="{ name: 'LessonView', params: { lessonId: lesson.id } }"
                     tag="p" class="course--title">
          {{ les.name }}
        </router-link>
      </template>
      <template slot="actions">
        <cv-button @click="actionNew">Показать лентяев</cv-button>
      </template>
      <template slot="headings">
        <cv-data-table-heading v-for="(column, id) in columns" :key="id">
          {{ column }}
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
            <cv-tag v-if="userMarks(user, lessonId.id )"
                    :label="`${userMarks(user, lessonId.id)}`"
                    :kind="kind(user, lessonId.id )">
            </cv-tag>
          </cv-data-table-cell>
          <cv-data-table-cell>
            {{ average(user) }}
          </cv-data-table-cell>
        </cv-data-table-row>
      </template>
    </cv-data-table>
    <cv-data-table-skeleton v-else :columns="2" :rows="6"/>
  </div>
</template>


<script lang="ts">
import LessonModel from '@/models/LessonModel';
import UserProgress from '@/models/UserProgress';
import lessonStore from "@/store/modules/lesson";
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';
import UserModel from "@/models/UserModel";
import {Dictionary} from "vue-router/types/router";
import UserComponent from "@/components/UserComponent.vue";
import User from "@/store/modules/user";

@Component({ components: {User, UserComponent} })
export default class LessonProgressView extends Vue {
  @Prop() lessonId!: number;

  students: Array<UserProgress> | null = [];
  users1: Dictionary<UserModel> = {};
  userStore = userStore;
  lessonStore = lessonStore;

  sortable = true;

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
  loading = true;

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
  kind(user: UserProgress, lessonId: number) {
    enum colors {
      O = 'grey',
      OK = 'green',
      WA = 'red',
      TL = 'magenta',
      ML = 'cyan'
    }
    const mark = user.solved[lessonId];
    return colors[mark];
    //return colors[mark % colors.length];
  }

  get users() {
    console.log(this.students)
    return this.students;
  }

  get les() {
    return this.lesson;
  }

  get columns() {
    //return
    return ['Ученики'].concat(this.les.problems.map((l) => l.name)).concat('Рейтинг');
  }

  actionNew() {
    console.log(Object.keys(this.students[2].solved).length)
    this.students = this.students.filter(x => Object.keys(x.solved).length === 0)
    console.log(this.students)
  }
  userMarks(userId: UserProgress, lessonId: number) {
    return userId.solved[lessonId]
    //return [];
  }

  userAttendance(userId: number, lessonId: number) {
    // return this.users[userId].attendance[lessonId];
    return [];
  }

  changeAttendance(userId: number, lessonId: number) {
    //
  }

  average(user: UserProgress): string {
    //const sum = (marks: number[]) => marks.reduce((total, value) => total + value);
    //const { solved } = user;
    //return sum(solved) / solved.length;
    return  (Object.keys(user.solved).length/this.les.problems.length)*100+"%";
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
