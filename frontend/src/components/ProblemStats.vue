<template>
  <div>
    <cv-structured-list>
      <template slot="headings"></template>
      <template slot="items">
        <cv-structured-list-item
          v-for="submit in successful.concat(testing).concat(wrong)"
          :key="submit.id">
          <div class="list-results-container">
            <UserComponent :user="students[submit.student.toString()]"/>
            <span>{{ submit.status }}</span>
          </div>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
    <div class="no-submits-users-container">
      <UserComponent v-for="user in noSubmitsUsers" :key="user.id" :user="user"/>
    </div>
  </div>
</template>

<script lang="ts">
import UserComponent from '@/components/UserComponent.vue';
import ProblemModel from '@/models/ProblemModel';
import SubmitModel from '@/models/SubmitModel';
import UserModel from '@/models/UserModel';
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Dictionary } from 'vue-router/types/router';

@Component({ components: { UserComponent } })
export default class ProblemStats extends Vue {
  @Prop({ required: true }) problem!: ProblemModel;
  userStore = userStore;

  usersWithSubmits: Set<string> = new Set(
    this.problem.success_or_last_submits.reduce<Array<string>>(
      (previousValue: Array<string>, currentValue: SubmitModel) => {
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
    return this.problem.success_or_last_submits.filter(x => x.status === 'AW');
  }

  get wrong() {
    return this.problem.success_or_last_submits.filter(x => x.status === 'WA');
  }

  get noSubmitsUsers(): Array<UserModel> {
    return Object.keys(this.students).filter(x => !this.usersWithSubmits.has(x)).map(x => {
      return this.students[x];
    });
  }

}
</script>

<style lang="stylus" scoped>

</style>