<template>
  <component :is="Edit24" @click.stop.prevent="showModal"/>
  <cv-modal :visible="modalVisible" @modal-hidden="hideModal">
    <template v-slot:title>
      <p>Редактировать группу: {{ group.id }}</p>
    </template>
    <template v-slot:content>
      <confirm-modal :approve-handler="deleteGroup"
                     :text="approvedText"
                     :modal-trigger="confirmModalTrigger"/>
      <div class="group-edit">
        <cv-structured-list v-if="[...group.staff, ...group.students].length">
          <template v-slot:items>
            <cv-structured-list-item v-for="member in [...group.staff, ...group.students]" :key="member">
              <div class="group-member">
                <router-link :to="{ name: 'profile-page', params: { userId: member} }">
                  <user-component :user-id="member"/>
                </router-link>
                <component :is="TrashCan24" class="trash-icon"/>
              </div>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
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
          <generate-links :course-id="group.course_id"/>
          <add-teacher-modal :course-id="group.course_id"/>
        </div>
        <div class="delete-btn">
          <cv-button kind="danger" @click="showConfirmModal">
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
import type { UserModel } from "@/models/UserModel";
import type { GroupModel } from "@/models/GroupModel";
import GenerateLinks from "@/components/EditCourse/GenerateLinks.vue";
import AddTeacherModal from "@/components/EditCourse/AddTeacherModal.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import api from "@/stores/services/api";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";

const props = defineProps({
  group: { type: Object as PropType<GroupModel>, required: true },
})

const emits = defineEmits(['update-groups']);

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const approvedText = ref('');
const confirmModalTrigger = ref(false);


const modalVisible = ref(false);

function showModal() {
  modalVisible.value = true;
}

function hideModal() {
  modalVisible.value = false;
}

function showConfirmModal() {
  approvedText.value = `Удалить группу: ${props.group.id}`;
  confirmModalTrigger.value = !confirmModalTrigger.value;
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
/deep/ .bx--modal-content:focus
  outline none

/deep/ .bx--modal-content
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

.action-btns
  margin 1rem 3rem 0 0
  display flex
  justify-content space-between
  gap 3rem

.invite-links
  display flex
  gap 1rem

.empty-component
  text-align center
</style>