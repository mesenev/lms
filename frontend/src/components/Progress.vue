<template>
  <div class="bx--grid">
    <!-- TODO ссылка на задачу -->
    <cv-data-table :columns="columns"
                   title="Успеваемость курса">
      <template slot="helper-text">
        <router-link :to="{ name: 'CourseView', params: { courseId: course.id } }"
                     tag="p" class="course--title">
          {{ course.name }}
        </router-link>
      </template>
      <template slot="data">
        <cv-data-table-row v-for="user in users" :key="user.id">
          <cv-data-table-cell>
            <!-- TODO ссылка на профиль -->
            {{ user.name }}
          </cv-data-table-cell>
          <cv-data-table-cell class="mark"
                              v-for="lessonId in user.courseLength"
                              :key="lessonId - 1">
            <!-- TODO цвет в зависимости от оценки по-человечески -->
            <cv-tag :label="`${user.marks[lessonId - 1]}`"
                    :kind="kind(user.id, lessonId - 1)">
            </cv-tag>
            <cv-checkbox :value="`${user.attendance[lessonId - 1]}`"
                         @click="changeAttendance(user.id, lessonId - 1)"
                         class="attendance">
            </cv-checkbox>
          </cv-data-table-cell>
          <cv-data-table-cell>
            {{ avarage(user.id) }}
          </cv-data-table-cell>
        </cv-data-table-row>
      </template>
    </cv-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { mainStore } from '@/store';

@Component
export default class Progress extends Vue {
  name!: 'Progress';

  store = mainStore;

  kind(userId: number, lessonId: number) {
    const colors = ['red', 'magenta', 'cyan', 'green'];
    const mark = this.store.getUsers[userId].marks[lessonId] - 2;
    return colors[mark % colors.length];
  }

  get users() {
    return this.store.getUsers;
  }

  get course() {
    return this.store.getCourse;
  }

  get columns() {
    return ['Ученики'].concat(this.store.getColumns).concat(['Рейтинг']);
  }

  changeAttendance(userId: number, lessonId: number) {
    this.$store.commit('changeAttendance', { userId, lessonId });
  }

  avarage(userId: number): number {
    const sum = (marks: number[]) => marks.reduce((total, value) => total + value);
    const { marks } = this.users[userId];
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
