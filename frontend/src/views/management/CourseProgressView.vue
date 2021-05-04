<template>
  <div class="bx--grid">
    <cv-data-table title="Успеваемость курса" v-if="!loading" @sort="Sort">
      <template slot="helper-text">
        <router-link :to="{ name: 'CourseView', params: { courseId: course.id } }"
                     tag="p" class="course--title">
          {{ course.name }}
        </router-link>
      </template>
      <template slot="actions">
        <cv-button :disabled="change" v-on:click="mark">
          Отметить посещаемость
        </cv-button>
      </template>
      <template slot="headings">
        <cv-data-table-heading v-for="(column, id) in columns" :key="id" :sortable=true>
          <h5 v-if="(column.id === 0)">Результаты</h5>
          <h5 v-else-if="(column.id === -2)">{{ column.name }}</h5>
          <div v-else @click="openSubmitOrProblem(column.id)">
            <h5>{{ column.name }}</h5>
          </div>
        </cv-data-table-heading>
      </template>
      <template slot="data">
        <cv-data-table-row v-for="user in progress" :key="user.id">
          <cv-data-table-cell>
            <router-link :to="{ name: 'profile-page', params: { userId: user.user.id } }"
                         class="course--title" tag="p">
              <UserComponent :user="user.user"/>
            </router-link>
          </cv-data-table-cell>
          <cv-data-table-cell
                v-for="les in lessons"
                              :key="les.id">
            {{sum(user.lessons[les.id])}}
              <div class="mark" v-for="(value, name) in user.lessons[les.id]" :key="value">
                <cv-tag :label="value.toString()"
                :kind="color(name)"/>
              </div>
            <cv-checkbox v-model="user.attendance[les.id]" class="mark">3</cv-checkbox>
          </cv-data-table-cell>
          <cv-data-table-cell>
            {{ average(user.lessons)}}
          </cv-data-table-cell>
        </cv-data-table-row>
      </template>
    </cv-data-table>
    <cv-data-table-skeleton v-else :columns="2" :rows="6"/>
  </div>
</template>


<script lang="ts">
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from "@/components/UserComponent.vue";
import _ from 'lodash';
import UserModel from "@/models/UserModel";
import UserProgress from '@/models/UserProgress';
import courseStore from '@/store/modules/course'
import problemStore from "@/store/modules/problem"
import progressStore from "@/store/modules/progress"
import userStore from '@/store/modules/user';
import lessonStore from '@/store/modules/lesson'
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import {Component, Prop, Vue} from 'vue-property-decorator';
import {Dictionary} from "vue-router/types/router";
import CourseModel from "@/models/CourseModel";
import LessonModel from "@/models/LessonModel";
import axios from "axios";

@Component({components: {SubmitStatus, UserComponent, UserAvatar20}})
export default class CourseProgressView extends Vue {
  @Prop() courseId!: number;

  students: Array<UserProgress> = [];
  students1: Array<UserProgress> = [...this.students];
  users: Dictionary<UserModel> = {};
  lessons: Array<LessonModel> = [];
  course: CourseModel = {
    id: NaN,
    name: '',
    author: {...userStore.user},
    lessons: [],
    completed: false,
    description: '',
    students: [],
  };
  userStore = userStore;
  courseStore = courseStore;
  progressStore = progressStore;
  problemStore = problemStore;
  lessonStore = lessonStore;

  loading = true;
  sortable = true;
  dontSolved = false;

  get columns() {
    const a = this.lessons.map(l => (
      {
        id: l.id,
        name: l.name,
      }
    ))
    a.unshift({ id: -2, name: "Ученики" })
    a.push({ id: 0, name: "Рейтинг" })
    return a
  }

  get progress() {
    if (this.dontSolved) {
      return this.students.filter(x => Object.keys(x.solved["HW"]).length === 0)
    }
    return this.students;
  }

  get cours() {
    return this.course;
  }

  async created() {
    this.course = await this.courseStore.fetchCourseById(this.courseId);
    this.students = await this.progressStore.fetchCourseProgressById(this.courseId);
    this.users = await this.userStore.fetchStudentsByCourseId(this.courseId);
    this.lessons = await this.lessonStore.fetchLessonsByCourseId(this.courseId);
    this.students = this.students.map(
      obj => Object.assign({}, obj, { user: this.users[obj.user.toLocaleString()]}));
    this.students1 = JSON.parse(JSON.stringify(this.students))
    this.loading = false;
  }

  openSubmitOrProblem(problem: number, submit?: number) {
    if (submit)
      this.$router.push(`/course/${this.$route.params['courseId']}/lesson/${this.$route.params['lessonId']}/problem/${problem}/submit/${submit}`);
    else
      this.$router.push(`/course/${this.$route.params['courseId']}/lesson/${this.$route.params['lessonId']}/problem/${problem}`);
  }

  color(type: string) {
    if (type === 'CW') {
      return 'blue'
    }
    if (type === 'HW') {
      return 'green'
    }
    if (type === 'EX') {
      return 'purple'
    }
  }

  sum(type: Dictionary<number>) {
    let s = 0;
    s += type['CW'] + type['HW'] + type['EX'];
    return s
  }

  average(progress: Dictionary<Dictionary<number>>) {
    let sum = 0;
    for (const i in progress) {
      sum += progress[i]['CW'];
      sum += progress[i]['HW'];
      sum += progress[i]['EX'];
    }
    return sum;
  }

  get change() {
    return _.isEqual(this.students, this.students1);
  }

  mark(): void {
    let progress: UserProgress = {
      id: NaN,
      user: NaN,
      solved: {},
    }
    let request: any;
    for (const i in this.students) {
      progress = JSON.parse(JSON.stringify(this.students[i]));
      progress.user = progress.user.id;
      request = axios.patch(`/api/courseprogress/${this.students[i].id}/`, progress);
    }
    request.then((response: any) => {
      console.log("Успех")
    });
    request.catch((error: any) => {
      console.log("Не успех")
    })
    request.finally(() => this.students1 = this.students);

  }
}
</script>

<style scoped lang="stylus">
.course--title
  color inherit
  cursor pointer
  display inline

.mark
  display: inline-block;

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
