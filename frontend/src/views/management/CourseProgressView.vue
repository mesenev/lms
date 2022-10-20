<template>
  <div class="bx--grid">
    <cv-data-table v-if="!loading" title="Успеваемость курса">
      <template slot="helper-text">
        <router-link
          :to="{ name: 'CourseView', params: { courseId: course.id } }"
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
        <cv-data-table-row v-for="row in progress" :key="row.id">
          <cv-data-table-cell>
            <router-link
              :to="{ name: 'profile-page', params: { userId: users[row.user]} }"
              class="course--title" tag="p">
              <UserComponent :userProp="users[row.user]"/>
            </router-link>
          </cv-data-table-cell>
          <cv-data-table-cell v-for="les in lessons" :key="les.id">
            {{ sum(row.progress[les.id]) }}
            <div v-for="(value, name) in row.progress[les.id]" :key="value+name"
                 class="mark">
              <cv-tag :label="value.toString()" :kind="color(name)"/>
            </div>
            <cv-checkbox
              :checked="student_attendance[`${row.user}-${les.id}`].attendance"
              :value="`${row.user}-${les.id}`"
              class="mark"
              @change="attendanceChange(row.user, les.id)"/>
          </cv-data-table-cell>
          <cv-data-table-cell>
            {{ average(row.lessons) }}
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
import Attendance from "@/models/Attendance";
import UserProgress from '@/models/UserProgress';
import courseStore from '@/store/modules/course'
import problemStore from "@/store/modules/problem"
import progressStore from "@/store/modules/progress"
import userStore from '@/store/modules/user';
import lessonStore from '@/store/modules/lesson'
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Dictionary } from "vue-router/types/router";
import CourseModel from "@/models/CourseModel";
import LessonModel from "@/models/LessonModel";

@Component({ components: { SubmitStatus, UserComponent, UserAvatar20 } })
export default class CourseProgressView extends Vue {
  @Prop() courseId!: number;

  students_progress: Array<UserProgress> = [];
  s: Dictionary<Array<Attendance>> = {};
  users: Dictionary<UserModel> = {};
  student_attendance: Dictionary<Attendance> = {};
  student_attendance_copy: Dictionary<any> = {};
  lessons: Array<LessonModel> = [];
  course: CourseModel = { ...courseStore.newCourse };
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

  get attendance() {
    return this.student_attendance;
  }

  get progress() {
    // if (this.dontSolved) {
    //   return this.students_progress.filter(x => Object.keys(x.solved["HW"]).length === 0)
    // }
    return this.students_progress;
  }

  get change() {
    return _.isEqual(this.student_attendance, this.student_attendance_copy)
  }

  attendanceChange(userId: number, lessonId: number) {
    const key = `${userId}-${lessonId}`;
    this.student_attendance_copy[key].attendance = !this.student_attendance_copy[key].attendance;
  }

  async created() {
    this.course = await this.courseStore.fetchCourseById(this.courseId);
    this.students_progress = await this.progressStore.fetchCourseProgressById(this.courseId);
    this.users = await this.userStore.fetchStudentsByCourseId(this.courseId);
    this.lessons = await this.lessonStore.fetchLessonsByCourseId(this.courseId);
    this.s = await this.progressStore.fetchAttendance(this.courseId);

    for (const [key, val] of Object.entries(this.s))
      for (const at of val)
        this.student_attendance[`${key}-${at.lesson}`] = at;

    this.student_attendance_copy = _.cloneDeep(this.student_attendance);
    this.loading = false;
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

  sum(type: any) {
    return (type['CW'] + type['HW'] + type['EX'])
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

  //TODO: change it with classical link
  openSubmitOrProblem(problem: number, submit?: number) {
    if (submit)
      this.$router.push(`/course/${this.$route.params['courseId']}/lesson/${this.$route.params['lessonId']}/problem/${problem}/submit/${submit}`);
    else
      this.$router.push(`/course/${this.$route.params['courseId']}/lesson/${this.$route.params['lessonId']}/problem/${problem}`);
  }

  async mark(): Promise<void> {
    let success = true;
    //TODO: remove unchanged instances
    for (const val of Object.values(this.student_attendance_copy)) {
      debugger;
      const request = axios.patch(`/api/lessonprogress/${val.id}/`, val);
      request.then((response: any) => {
        //
      });
      request.catch((error: any) => {
        success = false;
      })
    }
    this.student_attendance = _.cloneDeep(this.student_attendance_copy);
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
