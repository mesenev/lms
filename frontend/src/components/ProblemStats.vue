<template>
  <div>
    <cv-structured-list class="sent">
      <template slot="headings">
        <cv-structured-list-heading class="headings">
          <span>
            Решений: {{ successful.concat(testing).concat(wrong).length }}
          </span>
          <div
            class="stats"
          >
            <stats-graph :size="usersWithSubmits.size"
                         :wrong="wrong.length"
                         :successful="successful.length"
                         :testing="testing.length"
            />
            <span>Зачтено: {{ successful.length }}</span>
            <span>Ждут проверки: {{ testing.length }}</span>
            <span>Неправильно: {{ wrong.length }}</span>
          </div>
        </cv-structured-list-heading>
      </template>
      <template slot="items">
        <cv-structured-list-item
          v-for="submit in successful.concat(testing).concat(wrong)"
          :key="submit.id">
          <div class="list-results-container">
            <cv-structured-list-data class="student">
              <UserComponent :user="students[submit.student.toString()]"/>
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
         class="unsent-users"
       >
         <cv-structured-list-data>
           <UserComponent class="user" :user="user"/>
         </cv-structured-list-data>
       </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script lang="ts">
import UserComponent from '@/components/UserComponent.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import StatsGraph from '@/components/StatsGraph.vue';
import ProblemModel from '@/models/ProblemModel';
import SubmitModel from '@/models/SubmitModel';
import UserModel from '@/models/UserModel';
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Dictionary } from 'vue-router/types/router';

@Component({ components: { UserComponent, SubmitStatus, StatsGraph } })
export default class ProblemStats extends Vue {
  @Prop({ required: true }) problem!: ProblemModel;
  userStore = userStore;

  usersWithSubmits: Set<string> = new Set(
    this.problem.success_or_last_submits
      .reduce<Array<string>>((previousValue: Array<string>, currentValue: SubmitModel) => {
        previousValue.push(currentValue.student.toString())
        return previousValue;
      }, []),
  )

  get students(): Dictionary<UserModel> {
    if (!(this.$route.params.courseId in this.userStore.fetchedStudents))
      return {};
    return this.userStore.fetchedStudents[this.$route.params.courseId];
  }

  get successful() {
    return this.problem.success_or_last_submits.filter(x => x.status === 'OK');
  }

  get testing() {
    return this.problem.success_or_last_submits.filter(x => {
      return x.status === 'AW' || x.status === 'NP';
    });
  }

  get wrong() {
    return this.problem.success_or_last_submits.filter(x => x.status === 'WA');
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
