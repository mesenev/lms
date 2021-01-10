<template>
  <div class="bx--grid">
    <!-- TODO ссылка на задачу -->
    <cv-data-table title="Успеваемость курса">
      <template slot="helper-text">
        <router-link :to="{ name: 'CourseView', params: { courseId: course.id } }"
                     tag="p" class="course--title">
          {{ course.name }}
        </router-link>
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
            {{ user.name }}
          </cv-data-table-cell>
          <cv-data-table-cell class="mark"
                              v-for="lessonId in course.lessons.length"
                              :key="lessonId - 1">
            <!-- TODO цвет в зависимости от оценки по-человечески -->
            <cv-tag v-if="userMarks(user.id - 1, lessonId - 1)"
                    :label="`${userMarks(user.id - 1, lessonId - 1)}`"
                    :kind="kind(user, lessonId - 1)">
            </cv-tag>
            <cv-checkbox :value="`${userAttendance(user.id - 1, lessonId - 1)}`"
                         @change="changeAttendance(user.id - 1, lessonId - 1)"
                         class="attendance">
            </cv-checkbox>
          </cv-data-table-cell>
          <cv-data-table-cell>
            {{ average(user) }}
          </cv-data-table-cell>
        </cv-data-table-row>
      </template>
    </cv-data-table>
  </div>
</template>


<script lang="ts">
import CourseModel from '@/models/CourseModel';
import UserProgress from '@/models/UserProgress';
import { courseStore, userStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class CourseProgressView extends Vue {
  @Prop() courseId!: number;
  students!: Array<UserProgress>;
  userStore = userStore;
  courseStore = courseStore;
  course!: CourseModel;
  loading = true;

  async created() {
    this.students = await this.userStore.fetchStudentsProgressByCourseId(this.courseId);
    this.course = await this.courseStore.fetchCourseById(this.courseId);
    this.loading = false;
  }

  kind(user: UserProgress, lessonId: number) {
    const colors = ['red', 'magenta', 'cyan', 'green'];
    const mark = user.marks[lessonId] - 2;
    return colors[mark % colors.length];
  }

  get users() {
    return this.students;
  }


  get columns() {
    return ['Ученики'].concat(this.course.lessons.map((l) => l.name)).concat('Рейтинг');
  }

  userMarks(userId: number, lessonId: number) {
    // return this.users[userId].marks[lessonId];
    return [];
  }

  userAttendance(userId: number, lessonId: number) {
    // return this.users[userId].attendance[lessonId];
    return [];
  }

  changeAttendance(userId: number, lessonId: number) {
    //
  }

  average(user: UserProgress): number {
    const sum = (marks: number[]) => marks.reduce((total, value) => total + value);
    const { marks } = user;
    return sum(marks) / marks.length;
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
