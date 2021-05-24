<template>
  <div v-if="loading">
    <cv-loading/>
  </div>
  <div v-else>
    <cv-structured-list class="sent">
      <template slot="headings">
        <cv-structured-list-heading class="headings">
          <div class="stats">
            <span>Зачтено: {{ successful.length }}</span>
            <span>Ждут проверки: {{ testing.length }}</span>
            <span>Неправильно: {{ wrong.length }}</span>
          </div>
        </cv-structured-list-heading>
      </template>
      <template slot="items">
        <cv-structured-list-item
          v-for="submit in successful.concat(testing).concat(wrong)" :key="submit.id">
          <div class="list-results-container">
            <cv-structured-list-data class="student">
              <UserComponent :user="students[submit.student]"/>
            </cv-structured-list-data>
            <cv-structured-list-data class="submit">
              <submit-status :submit="submit"></submit-status>
            </cv-structured-list-data>
          </div>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
    <cv-structured-list class="unsent">
      <template slot="headings">
        <cv-structured-list-heading>
          Не сдали: {{ noSubmitsUsers.length }}
        </cv-structured-list-heading>
      </template>
      <template slot="items">
        <cv-structured-list-item
          v-for="user in noSubmitsUsers"
          :key="user.id"
          class="unsent-users">
          <cv-structured-list-data>
            <user-component :user="user" class="user"/>
          </cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script lang="ts">
import StatsGraph from '@/components/StatsGraph.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from '@/components/UserComponent.vue';
import ProblemModel from '@/models/ProblemModel';
import SubmitModel from '@/models/SubmitModel';
import UserModel from '@/models/UserModel';
import courseStore from '@/store/modules/course';
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Dictionary } from 'vue-router/types/router';

@Component({ components: { UserComponent, SubmitStatus, StatsGraph } })
export default class ProblemStats extends Vue {
  @Prop({ required: true }) problem!: ProblemModel;
  userStore = userStore;
  courseStore = courseStore;
  loading = true;

  usersWithSubmits: Set<string> = new Set(Object.keys(this.problem.students || ''));
  success_or_last_submits: Array<SubmitModel> = Object.values(this.problem.students || '');

  get students(): Dictionary<UserModel> {
    if (!(this.$route.params.courseId in this.userStore.currentCourseStudents))
      return {};
    return this.userStore.currentCourseStudents;
  }

  get successful() {
    return this.success_or_last_submits.filter(x => x.status === 'OK');
  }

  get testing() {
    return this.success_or_last_submits.filter(x => {
      return x.status === 'AW' || x.status === 'NP';
    });
  }

  get wrong() {
    return this.success_or_last_submits.filter(x => x.status === 'WA');
  }

  get noSubmitsUsers(): Array<UserModel> {
    return Object.keys(this.students)
      .filter(x => !this.usersWithSubmits.has(x))
      .map(x => this.students[x]);
  }
}
</script>

<style lang="stylus" scoped>
.list-results-container
  display flex
  flex-direction row
  justify-content space-between
  align-items center

.submit span:first-child
  margin-right 5px

.sent, .unsent
  margin-bottom 1rem
  padding-left 1rem

  /deep/ .bx--structured-list-tbody
    padding 0 1rem

  .headings
    display flex
    flex-direction row
    justify-content space-between

  .stats
    display flex
    flex-direction row

    > span:not(:last-child)
      margin-right 5px

.sent
  /deep/ .bx--structured-list-tbody
    display flex
    flex-direction column


.unsent
  /deep/ .bx--structured-list-tbody
    display flex
    flex-direction row
    flex-wrap wrap

  .cv-structured-list-item
    border 0
    flex 0 0 25%

  .user
    border 0
</style>
