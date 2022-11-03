<template>
  <div v-if="!isStaff">
    <cv-structured-list>
      <template slot="items">
        <cv-structured-list-item
          v-for="problem in taskList"
          :key="problem.id">
          <student-problem-list-item-component
            :problem="problem">
          </student-problem-list-item-component>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
  <div v-else>
    <confirm-modal
      :modal-trigger="modalTrigger"
      :approve-handler="deleteProblem"
      :text="approvedText"/>
    <cv-inline-notification
      v-if="showNotification"
      :sub-title="notificationText"
      kind="error"
      @close="() => showNotification=false"/>
    <cv-accordion
      v-for="problem in taskList"
      :key="problem.id"
      align="end">
      <staff-problem-list-item-component
        :is-editing="isEditing"
        :problem="problem"
        @show-confirm-modal="showConfirmModal($event)">
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
import {Component, Prop} from 'vue-property-decorator';
import CatsProblemModel from "@/models/CatsProblemModel";
import StudentProblemListItemComponent from "@/components/StudentProblemListItemComponent.vue";
import StaffProblemListItemComponent from "@/components/StaffProblemListItemComponent.vue";
import NotificationMixinComponent from '../common/NotificationMixinComponent.vue';
import api from "@/store/services/api";
import ConfirmModal from "@/components/ConfirmModal.vue";

@Component({
  components: {
    ProblemStats,
    SubmitStatus,
    Launch,
    StatsGraph,
    StudentProblemListItemComponent,
    StaffProblemListItemComponent,
    ConfirmModal
  }
})
export default class ProblemListComponent extends NotificationMixinComponent {
  @Prop({required: true}) taskList!: Array<ProblemModel | CatsProblemModel>;
  @Prop({required: false}) isEditing!: false | boolean;
  userStore = userStore;
  courseStore = courseStore;
  deletingProblemId: number | null = null;
  modalTrigger = false;
  approvedText = '';

  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }

  showConfirmModal(deletingProblem: ProblemModel) {
    this.deletingProblemId = deletingProblem.id;
    this.approvedText = `Удалить задачу: ${deletingProblem.name}`;
    this.modalTrigger = !this.modalTrigger;
  }

  async deleteProblem() {
    if (!this.deletingProblemId)
      throw Error;
    await api.delete(`/api/problem/${this.deletingProblemId}/`).then(() => {
      this.$emit('update-problem-delete', this.deletingProblemId);
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    })
  }
}
</script>
<style lang="stylus">
.problem-list-component--header
  display flex
  align-items center
  justify-content space-between

.icon-trash
  margin-right 1rem

.aw
  text-align right

.accordion /deep/ .bx--accordion__content
  padding-right 0
</style>
