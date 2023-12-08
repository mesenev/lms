<template>
  <component :is="Edit24" @click.stop.prevent="showModal"/>
  <cv-modal :visible="modalVisible" @modal-hidden="hideModal">
    <template v-slot:title>
      <p>Редактировать группу</p>
    </template>
    <template v-slot:content>
      <div class="group-edit">
        <cv-structured-list>
          <template v-slot:items>
            <cv-structured-list-item v-for="member in groupMembers" :key="member.id">
              <div class="group-member">
                <router-link :to="{ name: 'profile-page', params: { userId: member.id} }">
                  <user-component :user-prop="member" :user-id="member.id"/>
                </router-link>
                <component :is="TrashCan24" class="trash-icon"/>
              </div>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
      <div class="action-btns">
        <div class="invite-links">
          <generate-links :course-id="courseId"/>
          <add-teacher-modal :course-id="courseId"/>
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

const props = defineProps({
  courseId: { type: Number, required: true },
  group: { type: Object as PropType<GroupModel>, required: false },
  groupMembers: { type: Object as PropType<Array<UserModel>>, required: false },
})

const modalVisible = ref(false);

function showModal() {
  modalVisible.value = true;
}

function hideModal() {
  modalVisible.value = false;
}

function showConfirmModal() {

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
</style>