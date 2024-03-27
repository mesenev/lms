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

<script lang="ts" setup>
import trashCan from '@carbon/icons-vue/lib/trash-can/16';
import settings from '@carbon/icons-vue/lib/settings/16';
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import type { ExamModel } from "@/models/ExamModel";
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/stores/services/api";
import ConfirmModal from "@/components/ConfirmModal.vue";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  examsList: { type: Array<ExamModel>, required: true },
  isStaff: { type: Boolean, required: false },
  isEditing: { type: Boolean, required: false }
})

const emits = defineEmits(['update-exam-delete'])

const router = useRouter();

const deletingExamId = ref<number | null>(null);
const modalTrigger = ref(false);
const approvedText = ref('');

function target(exam: ExamModel) {
  return { name: 'ExamView', params: { examId: exam.id.toString() } };
}

function redirectToEdit(exam: ExamModel) {
  router.push({ name: 'exam-edit', params: { examId: exam.id.toString() } })
}

function showConfirmModal(deletingExam: ExamModel) {
  deletingExamId.value = deletingExam.id;
  approvedText.value = `Удалить тест: ${deletingExam.name}`;
  modalTrigger.value = !modalTrigger.value;
}

async function deleteExam() {
  if (!deletingExamId.value)
    throw Error;
  await api.delete(`/api/exam/${deletingExamId.value}/`).then(() => {
    emits('update-exam-delete', deletingExamId.value);
  }).catch(error => {
    notificationKind.value = 'error';
    notificationText.value = `Что-то пошло не так: ${error.message}`;
    showNotification.value = true;
  })
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
