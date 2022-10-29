<template>
  <div v-if="!isStaff">
    <cv-structured-list>
      <template slot="items">
        <cv-structured-list-item
          v-for="problem in taskList"
          :key="problem.id">
          <student-problem-list-item-component
            :problem="problem"></student-problem-list-item-component>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
  <div v-else>
    <cv-accordion
      v-for="problem in taskList"
      :key="problem.id"
      align="end">
      <staff-problem-list-item-component :problem="problem"></staff-problem-list-item-component>
    </cv-accordion>
  </div>
</template>

<script lang="ts">
import ProblemStats from '@/components/ProblemStats.vue';
import StatsGraph from '@/components/StatsGraph.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import ProblemModel from '@/models/ProblemModel';

import userStore from '@/store/modules/user';
import courseStore from '@/store/modules/course';
import {Component, Prop, Vue} from 'vue-property-decorator';
import CatsProblemModel from "@/models/CatsProblemModel";
import StudentProblemListItemComponent from "@/components/StudentProblemListItemComponent.vue";
import StaffProblemListItemComponent from "@/components/StaffProblemListItemComponent.vue";

@Component({
  components: {
    StaffProblemListItemComponent,
    StudentProblemListItemComponent, ProblemStats, SubmitStatus, StatsGraph
  }
})
export default class ProblemListComponent extends Vue {
  @Prop({required: true}) taskList!: Array<ProblemModel | CatsProblemModel>;
  userStore = userStore;
  courseStore = courseStore;


  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }
}

</script>
<style scoped lang="stylus">
.aw
  text-align right

.accordion /deep/ .bx--accordion__content
  padding-right 0
</style>
