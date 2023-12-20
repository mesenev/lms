<template>
  <component :is="Edit24" @click.stop.prevent="showModal"/>
  <cv-modal :visible="modalVisible" @modal-hidden="hideModal">
    <template v-slot:title>
      <p>Редактировать группу: {{ group.id }}</p>
    </template>
    <template v-slot:content>
      <confirm-modal :approve-handler="deleteFunction"
                     :text="approvedText"
                     :modal-trigger="confirmModalTrigger"/>
      <div class="group-edit">
        <div v-if="[...group.staff, ...group.students].length">
          <cv-structured-list v-if="group.staff.length">
            <template v-slot:headings>
              <cv-structured-list-heading>
                <span>Преподаватели</span>
              </cv-structured-list-heading>
            </template>
            <template v-slot:items>
              <cv-structured-list-item v-for="member in group.staff" :key="member">
                <div class="group-member">
                  <router-link :to="{ name: 'profile-page', params: { userId: member} }">
                    <user-component :user-id="member"/>
                  </router-link>
                  <component :is="TrashCan24" class="trash-icon"
                             @click="showConfirmModal('Удалить учителя из группы', deleteTeacherFromGroup, member)"/>
                </div>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
          <cv-structured-list v-if="group.students.length">
            <template v-slot:headings>
              <cv-structured-list-heading>
                <span>Студенты</span>
              </cv-structured-list-heading>
            </template>
            <template v-slot:items>
              <cv-structured-list-item v-for="member in group.students" :key="member">
                <div class="group-member">
                  <router-link :to="{ name: 'profile-page', params: { userId: member} }">
                    <user-component :user-id="member"/>
                  </router-link>
                  <component :is="TrashCan24" class="trash-icon"
                             @click="showConfirmModal('Удалить студента из группы', deleteStudentFromGroup, member)"/>
                </div>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
        </div>
        <empty-list-component v-else class="empty-component"
                              list-of="groupMembers"
                              text="Добавьте участников в группу"/>
        <cv-inline-notification v-if="showNotification"
                                :kind="notificationKind"
                                :sub-title="notificationText"
                                @close="hideNotification"/>
      </div>
      <div class="action-btns">
        <div class="invite-links">
          <generate-links :group-id="group.id"/>
          <add-teacher-modal :group-id="group.id"/>
        </div>
        <div class="delete-btn">
          <cv-button kind="danger" @click="showConfirmModal('Удалить группу', deleteGroup)">
            Удалить группу
          </cv-button>
        </div>
      </div>
    </template>
  </cv-modal>
</template>

<script setup lang="ts">
import Edit24 from "@carbon/icons-vue/es/edit/24"
import TrashCan24 from "@carbon/icons-vue/es/trash-can/24";
import { type PropType, ref } from "vue";
import UserComponent from "@/components/UserComponent.vue";
import type { GroupModel } from "@/models/GroupModel";
import GenerateLinks from "@/components/EditCourse/GenerateLinks.vue";
import AddTeacherModal from "@/components/EditCourse/AddTeacherModal.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import api from "@/stores/services/api";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";
import useUserStore from "@/stores/modules/user";

const props = defineProps({
  group: { type: Object as PropType<GroupModel>, required: true },
})

const emits = defineEmits(['update-groups']);

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const approvedText = ref('');
const confirmModalTrigger = ref(false);
const modalVisible = ref(false);

const userStore = useUserStore();

const deleteFunction = ref<Function>(() => {});
const memberIdToDelete = ref<number | null>(null);

function showModal() {
  modalVisible.value = true;
}

function hideModal() {
  modalVisible.value = false;
}

function showConfirmModal(deletion_text: string, delFunction: Function, member_id: number | null = null) {
  memberIdToDelete.value = member_id;
  approvedText.value = member_id ? deletion_text : `${deletion_text}: ${props.group.id}`;
  deleteFunction.value = delFunction;
  confirmModalTrigger.value = !confirmModalTrigger.value;
}

async function deleteStudentFromGroup() {
  if (!memberIdToDelete.value)
    throw Error('member to delete is not selected');
  await api.delete(`/api/group/${props.group.id}/delete-student/${memberIdToDelete.value}/`)
    .then(() => {
      let updatedGroup = {
        ...props.group,
        students: [...props.group.students].filter(studentId => studentId !== memberIdToDelete.value)
      };
      emits('update-groups', updatedGroup);
    }).catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    })
}

async function deleteTeacherFromGroup() {
  if (!memberIdToDelete.value)
    throw Error('member to delete is not selected');
  await api.delete(`/api/group/${props.group.id}/delete-teacher/${memberIdToDelete.value}/`)
    .then(() => {
      let updatedGroup = {
        ...props.group,
        staff: [...props.group.staff].filter(teacherId => teacherId !== memberIdToDelete.value)
      };
      emits('update-groups', updatedGroup);
    }).catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    })
}

async function deleteGroup() {
  await api.delete(`/api/group/${props.group.id}/`)
    .then(async () => {
      emits('update-groups', props.group.id);
      hideModal();
    })
    .catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    })
}
</script>


<style scoped lang="stylus">
:deep() .bx--modal-content:focus
  outline none

:deep() .bx--modal-content, :deep() .bx--structured-list
  margin-bottom 1rem

.group-create-btn
  align-self end
  margin-top 1rem

.group-member
  margin 0.5rem
  display flex
  justify-content space-between
  align-items center

.group-edit
  margin-right 3rem
  max-height 25rem
  overflow auto

.action-btns
  margin 1rem 3rem 0 0
  display flex
  justify-content space-between
  gap 3rem

.invite-links
  display flex
  gap 1rem

.trash-icon
  cursor pointer

.empty-component
  text-align center
</style>