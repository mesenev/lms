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
            {{ avarage(user) }}
          </cv-data-table-cell>
        </cv-data-table-row>
      </template>
    </cv-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { mainStore } from '@/store';
import UserProgress from '@/models/UserProgress';

@Component
export default class Progress extends Vue {
  name!: 'Progress';

  store = mainStore;

  kind(user: UserProgress, lessonId: number) {
    const colors = ['red', 'magenta', 'cyan', 'green'];
    const mark = user.marks[lessonId] - 2;
    return colors[mark % colors.length];
  }

  get users() {
    return this.store.getUsers;
  }

  get course() {
    return this.store.getCourse;
  }

  get columns() {
    return ['Ученики'].concat(this.course.lessons.map((l) => l.name)).concat('Рейтинг');
  }

  userMarks(userId: number, lessonId: number) {
    return this.users[userId].marks[lessonId];
  }

  userAttendance(userId: number, lessonId: number) {
    return this.users[userId].attendance[lessonId];
  }

  changeAttendance(userId: number, lessonId: number) {
    this.$store.commit('changeAttendance', { userId, lessonId });
  }

  avarage(user: UserProgress): number {
    const sum = (marks: number[]) => marks.reduce((total, value) => total + value);
    const { marks } = user;
    return sum(marks) / marks.length;
  }
}
</script>

<style lang="stylus">
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
</style>
