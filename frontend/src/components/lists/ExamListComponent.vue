<template>
  <div>
    <confirm-modal
      :modal-trigger="modalTrigger"
      :approve-handler="deleteExam"
      :text="approvedText"/>
    <cv-inline-notification
      v-if="showNotification"
      :sub-title="notificationText"
      kind="error"
      @close="() => showNotification=false"/>
    <router-link :to="target(exam)" class="list-element" v-for="exam in examsList" :key="exam.id">
      <div class="title-wrapper">
        <h5 class="list-element--title"> {{ exam.name }} </h5>
      </div>
      <div class="icons" v-if="isStaff && isEditing">
        <component :is="settings" @click.stop.prevent="redirectToEdit(exam)"/>
        <component :is="trashCan" @click.stop.prevent="showConfirmModal(exam)"/>
      </div>
    </router-link>
  </div>
</template>

<script lang="ts">
import ExamModel from "@/models/ExamModel";
import { Component, Prop } from 'vue-property-decorator';
import trashCan from '@carbon/icons-vue/lib/trash-can/16';
import settings from '@carbon/icons-vue/lib/settings/16';
import ConfirmModal from "@/components/ConfirmModal.vue";
import api from "@/store/services/api";
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import router from "@/router";

@Component({ components: { ConfirmModal } })
export default class ExamListComponent extends NotificationMixinComponent {
  @Prop({ required: true }) examsList!: Array<ExamModel>;
  @Prop({ required: false, default: false }) isStaff!: boolean;
  @Prop({ required: false, default: false }) isEditing!: boolean;

  trashCan = trashCan;
  settings = settings;

  deletingExamId: number | null = null;
  modalTrigger = false;
  approvedText = '';

  target(exam: ExamModel) {
    return { name: 'ExamView', params: { examId: exam.id.toString() } };
  }

  redirectToEdit(exam: ExamModel) {
    router.push({name: 'exam-edit', params: {examId: exam.id.toString()}})
  }

  showConfirmModal(deletingExam: ExamModel) {
    this.deletingExamId = deletingExam.id;
    this.approvedText = `Удалить тест: ${deletingExam.name}`;
    this.modalTrigger = !this.modalTrigger;
  }

  async deleteExam() {
    if (!this.deletingExamId)
      throw Error;
    await api.delete(`/api/exam/${this.deletingExamId}/`).then(() => {
      this.$emit('update-exam-delete', this.deletingExamId);
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    })
  }
}
</script>

<style scoped lang="stylus">
.list-element
  display flex
  flex-direction row
  justify-content space-between
  align-items center
  border-top 1px solid var(--cds-ui-03)
  border-bottom 1px solid var(--cds-ui-03)

.list-element:hover
  background-color var(--cds-ui-03)

.icons
  display flex
  margin-right 1rem
  gap 1rem
</style>
