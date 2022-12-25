<template>
  <div class="bx--grid">
    <div v-if="!loading">
      <div class="main-header">
        <div class="main-title">
          <h2>Успеваемость курса: {{ course.name }}</h2>
        </div>
        <cv-button :disabled="change" v-on:click="mark" v-if="progress.length">
          Отметить посещаемость
        </cv-button>
      </div>
      <div class="table-wrapper" v-if="progress.length">
        <cv-data-table @sort="Sort">
          <template slot="headings">
            <cv-data-table-heading class="fixed-col thead-element"
                                   v-for="(column, id) in columns" :key="id"
                                   :sortable=true>
              <h5 v-if="(column.id === 0)">Результаты</h5>
              <h5 v-else-if="(column.id === -2)">{{ column.name }}</h5>
              <div v-else @click="openSubmitOrProblem(column.id)">
                <h5>{{ column.name }}</h5>
              </div>
            </cv-data-table-heading>
          </template>
          <template slot="data">
            <cv-data-table-row v-for="row in progress" :key="row.user">
              <cv-data-table-cell class="fixed-col">
                <router-link
                  :to="{ name: 'profile-page', params: { userId: row.user} }"
                  class="course--title" tag="p">
                  <UserComponent :userProp="users[row.user]"/>
                </router-link>
              </cv-data-table-cell>
              <cv-data-table-cell v-for="les in lessons"
                                  :key="les.id"
                                  class="tbody-element">
                <div class="tbody-data">
                  <div class="marks">
                    <cv-tag class="result-mark" :label="sum(row.progress[les.id])"/>
                    <div v-for="(value, name) in row.progress[les.id]" :key="value+name"
                         class="mark">
                      <cv-tag :label="Math.trunc(value).toString()" :kind="color(name)"/>
                    </div>
                  </div>
                  <div class="mark-checkbox">
                    <cv-checkbox
                      :checked="student_attendance[`${row.user}-${les.id}`].attendance"
                      :value="`${row.user}-${les.id}`"
                      @change="attendanceChange(row.user, les.id)"/>
                  </div>
                </div>
              </cv-data-table-cell>
              <cv-data-table-cell>
                {{ average(row.progress) }}
              </cv-data-table-cell>
            </cv-data-table-row>
          </template>
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
import api from "@/store/services/api";
import EmptyListComponent from "@/components/EmptyListComponent.vue";

@Component({ components: { EmptyListComponent, SubmitStatus, UserComponent, UserAvatar20 } })
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
  emptyText = '';

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
    this.emptyText = 'Ни один студент не записан на данный курс'

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
    return Math.trunc(type['CW'] + type['HW'] + type['EX']).toString();
  }

  average(progress: Dictionary<string>) {
    let sum = 0 as any;
    for (const submits of Object.values(progress)) {
      sum += submits['CW' as any];
      sum += submits['HW' as any];
      sum += submits['EX' as any];
    }
    return Math.trunc(sum).toString();
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
      const request = api.patch(`/api/lessonprogress/${val.id}/`, val);
      request.then((response) => {
        //
      });
      request.catch((error) => {
        success = false;
      })
    }
    this.student_attendance = _.cloneDeep(this.student_attendance_copy);
  }

  Sort(sortBy: { index: string; order: string }) {
    let order = -1;
    console.log(this.progress);
    if (sortBy.order == "none") {
      return this.students_progress.sort((a, b) => {
        return a.user - b.user
      })
    }
    if (sortBy.order == "ascending") {
      order *= -1;
    }
    if (sortBy.index == "0") {
      return this.students_progress.sort((a, b) => {
        return (this.users[a.user].last_name > this.users[b.user].last_name) ? order : -1 * order;
      })
    } else if (sortBy.index == (this.columns.length - 1).toString()) {
      return this.students_progress.sort((a, b) => {
        const A = a.progress ? this.average(a.progress) : 0;
        const B = b.progress ? this.average(b.progress) : 0;
        return A > B ? order : -1 * order;
      })
    } else {
      return this.students_progress.sort((a, b) => {
        const A = a.progress ? this.sum(a.progress[sortBy.index]) : 0;
        const B = b.progress ? this.sum(b.progress[sortBy.index]) : 0;
        return A > B ? order : -1 * order;
      })
    }
  }
}
</script>

<style scoped lang="stylus">
.main-header
  display flex
  flex-direction row
  justify-content space-between
  margin-bottom 1rem

.main-title
  margin-left 0
  margin-bottom 0

.table-wrapper
  margin-top 1rem
  border 0.5px solid var(--cds-ui-05)
  border-collapse separate
  overflow-x auto
  width 100%

.tbody-element, .fixed-col
  min-width 16rem
  border-right 0.5px solid var(--cds-ui-05)
  z-index 0

.tbody-data
  display flex
  flex-direction row
  justify-content space-around

.fixed-col:first-child
  text-align-last left
  z-index 2
  position sticky
  left 0

.fixed-col:last-child
  border-right none

/deep/ table
  text-align-last center
  border-collapse separate

/deep/ th
  padding-top 0.5rem
  padding-bottom 0.5rem

/deep/ .bx--data-table-container
  padding-top 0

.marks
  min-width 180px

.result-mark
  color var(--cds-ui-05)
  background-color var(--cds-ui-background)
  border var(--cds-ui-05) 0.5px solid

.mark
  display: inline-flex

.mark-checkbox
  display flex
  align-items center

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

.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.item
  min-height 85px
</style>
