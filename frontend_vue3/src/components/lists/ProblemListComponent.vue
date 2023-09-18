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

<script lang="ts" setup>
import ProblemStats from '@/components/ProblemStats.vue';
import StatsGraph from '@/components/StatsGraph.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import type { ProblemModel } from '@/models/ProblemModel';
import Launch from '@carbon/icons-vue/es/launch/16';
import useUserStore from '@/stores/modules/user';
import useCourseStore from '@/stores/modules/course';
import type { CatsProblemModel } from "@/models/CatsProblemModel";
import StudentProblemListItemComponent from "@/components/StudentProblemListItemComponent.vue";
import StaffProblemListItemComponent from "@/components/StaffProblemListItemComponent.vue";
import useNotificationMixin from '../common/NotificationMixinComponent.vue';
import api from "@/stores/services/api";
import ConfirmModal from "@/components/ConfirmModal.vue";
import { type Ref, ref, computed, type PropType } from 'vue';
import { useRoute } from 'vue-router';


  const props = defineProps({
    taskList: {type :Object as PropType<Array<ProblemModel | CatsProblemModel>>, required: true},
    isEditing: { type: Boolean, required: false } 
  })
  const emit = defineEmits<{
    (e: 'update-problem-delete', problemId: number | null) : void
  }>()
  const userStore = useUserStore();
  const courseStore = useCourseStore();
  const route = useRoute();

  const deletingProblemId: Ref<number | null> = ref(null);
  const modalTrigger: Ref<boolean> = ref(false);
  const approvedText: Ref<string> = ref('');

  const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

  const isStaff =computed((): boolean => {
    const courseId = Number(route.params.courseId);
    return userStore.user.staff_for.includes(courseId);
  })

  function showConfirmModal(deletingProblem: ProblemModel) {
    deletingProblemId.value = deletingProblem.id;
    approvedText.value = `Удалить задачу: ${deletingProblem.name}`;
    modalTrigger.value = !modalTrigger.value;
  }

  async function deleteProblem() {
    if (!deletingProblemId.value)
      throw Error;
    await api.delete(`/api/problem/${deletingProblemId.value}/`).then(() => {
      emit('update-problem-delete', deletingProblemId.value);
    }).catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    })
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
