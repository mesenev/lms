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
    <cv-inline-notification
      v-if="showNotification"
      @close="() => showNotification=false"
      kind="error"
      :sub-title="notificationText"/>
    <cv-accordion
      v-for="problem in taskList"
      :key="problem.id"
      align="end">
      <staff-problem-list-item-component
        @delete-problem-click="deleteProblem($event)"
        :is-editing="isEditing"
        :problem="problem">
      </staff-problem-list-item-component>
    </cv-accordion>
  </div>
</template>

<script lang="ts">
import ProblemStats from '@/components/ProblemStats.vue';
import StatsGraph from '@/components/StatsGraph.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import ProblemModel from '@/models/ProblemModel';
import Launch from '@carbon/icons-vue/es/launch/16';
import userStore from '@/store/modules/user';
import courseStore from '@/store/modules/course';
import { Component, Prop } from 'vue-property-decorator';
import CatsProblemModel from "@/models/CatsProblemModel";
import StudentProblemListItemComponent from "@/components/StudentProblemListItemComponent.vue";
import StaffProblemListItemComponent from "@/components/StaffProblemListItemComponent.vue";
import NotificationMixinComponent from '../common/NotificationMixinComponent.vue';
import api from "@/store/services/api";

@Component({ components: { ProblemStats, SubmitStatus, Launch, StatsGraph, StudentProblemListItemComponent, StaffProblemListItemComponent } })
export default class ProblemListComponent extends NotificationMixinComponent {
  @Prop({ required: true }) taskList!: Array<ProblemModel | CatsProblemModel>;
  @Prop({ required: false }) isEditing!: false | boolean;
  userStore = userStore;
  courseStore = courseStore;

  deleteProblem(problemId: number) {
    api.delete(`/api/problem/${problemId}/`).then(() => {
      this.$emit('update-problem-delete', problemId);
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    })
  }

  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }
}
</script>
<style scoped lang="stylus">
.problem-list-component--header
  display flex
  align-items center
  justify-content space-between

.icon-trash
  margin-right 2rem

.aw
  text-align right

.accordion /deep/ .bx--accordion__content
  padding-right 0
</style>
