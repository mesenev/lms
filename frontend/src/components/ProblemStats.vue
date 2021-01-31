<template>
  <div>
    <cv-structured-list>
      <template slot="headings"></template>
      <template slot="items">
        <cv-structured-list-item v-for="submit in (successful + testing + wrong)" :key="submit.id">
          <div class="list-results-container">
            <UserComponent :user="submit.student"/>
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

@Component({
  components: { UserComponent },
})
export default class ProblemStats extends Vue {
  @Prop({ required: true }) problem!: ProblemModel;
  userStore = userStore;

  usersWithSubmits: Set<UserModel> = new Set(
    this.problem.success_or_last_submits.reduce<Array<UserModel>>(
      (previousValue: Array<UserModel>, currentValue: SubmitModel) => {
        previousValue.push(currentValue.student)
        return previousValue;
      }, []),
  )

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
    return this.userStore.fetchedStudents[this.$route.params.courseId].filter(
      x => !this.usersWithSubmits.has(x),
    );
  }

}
</script>

<style lang="stylus" scoped>

</style>
