<template>
  <div v-if="loading" class="loading-container">
    <cv-loading/>
  </div>
  <div v-else class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1>Группы курса: {{ course.name }}</h1>
      </div>
    </div>
    <div class="bx-row">
      <div class="bx--col-lg-6 bx--col-md-6">
        <cv-inline-notification v-if="showNotification"
                                :kind="notificationKind"
                                :sub-title="notificationText"
                                @close="hideNotification"/>
        <div class="groups-wrapper">
          <cv-accordion v-if="groups.length">
            <cv-accordion-item v-for="group in groups" :key="group.id">
              <template v-slot:title>
                <div class="group-header">
                  <p>Группа {{ group.id }}</p>
                  <group-modal @update-groups="updateGroups" :group="group"/>
                </div>
              </template>
              <template v-slot:content>
                <div v-if="[...group.staff, ...group.students].length">
                  <cv-structured-list v-if="group.staff.length">
                    <template v-slot:headings>
                      <cv-structured-list-heading>
                        <span>Преподаватели</span>
                      </cv-structured-list-heading>
                    </template>
                    <template v-slot:items>
                      <cv-structured-list-item v-for="member in group.staff" :key="member">
                        <router-link :to="{ name: 'profile-page', params: { userId: member} }">
                          <user-component class="group-member" :user-id="member"/>
                        </router-link>
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
                        <router-link :to="{ name: 'profile-page', params: { userId: member} }">
                          <user-component class="group-member" :user-id="member"/>
                        </router-link>
                      </cv-structured-list-item>
                    </template>
                  </cv-structured-list>
                </div>
                <empty-list-component v-else list-of="groupMembers" text="Добавьте участников в группу"/>
              </template>
            </cv-accordion-item>
          </cv-accordion>
          <empty-list-component v-else class="empty-component" list-of="groups" text="Создайте группу"/>
          <cv-button class="create-group-btn" @click="createGroup">
            Создать группу
          </cv-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import type { CourseModel } from "@/models/CourseModel";
import useCourseStore from "@/stores/modules/course";
import UserComponent from "@/components/UserComponent.vue";
import GroupModal from "@/components/GroupModal.vue";
import useGroupStore from "@/stores/modules/group";
import type { GroupModel } from "@/models/GroupModel";
import api from "@/stores/services/api";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";

const props = defineProps({
  courseId: { type: Number, required: true }
});

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();


const courseStore = useCourseStore();
const groupStore = useGroupStore();

const groups = ref<Array<GroupModel>>([]);

const course = ref<CourseModel>({ ...courseStore.newCourse });

const loading = ref(true);

onMounted(async () => {
  course.value = await courseStore.fetchCourseById(props.courseId);
  groups.value = await groupStore.fetchGroupsByCourseId(props.courseId);
  loading.value = false;
})

function updateGroups(payload: Array<GroupModel> | number): void {
  if (typeof payload !== 'number') {
    groupStore.setGroups({ [props.courseId]: payload });
    return;
  }
  groups.value = groups.value.filter(el => el.id !== payload);
  groupStore.setGroups({ [props.courseId]: groups.value });
}

function createGroup() {
  api.post('/api/group/', { ...groupStore.newGroup, course: props.courseId })
    .then(response => {
      groups.value.push(response.data);
      updateGroups(groups.value);
    })
    .catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    })
}

</script>

<style scoped lang="stylus">
.groups-wrapper
  display flex
  flex-direction column
  justify-content space-between
  padding 1rem
  background-color var(--cds-ui-01)
  min-height 400px

.group-header
  display flex
  flex-direction row
  justify-content space-between
  margin-right 1rem

.group-member
  margin 0.5rem

.create-group-btn
  margin-top 1rem
  align-self end

.empty-component
  text-align center

:deep() .bx--accordion__content
  padding-right 3rem

:deep() .bx--structured-list
  margin-bottom 0

</style>