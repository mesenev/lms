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
        <div class="groups-wrapper" id="groups-wrapper">
          <cv-accordion>
            <cv-accordion-item v-for="group in groups" :key="group.id">
              <template v-slot:title>
                <div class="group-header">
                  <p>{{ group }}</p>
                  <group-modal :course-id="courseId" :group-members="groupMembers" :group-id="1"/>
                </div>
              </template>
              <template v-slot:content>
                <cv-structured-list>
                  <template v-slot:headings>
                    <cv-structured-list-heading>
                      Тип проверки: Автоматический
                    </cv-structured-list-heading>
                  </template>
                  <template v-slot:items>
                    <cv-structured-list-item v-for="member in groupMembers" :key="member.id">
                      <router-link :to="{ name: 'profile-page', params: { userId: member.id} }">
                        <user-component class="group-member" :user-prop="member" :user-id="member.id"/>
                      </router-link>
                    </cv-structured-list-item>
                  </template>
                </cv-structured-list>
              </template>
            </cv-accordion-item>
          </cv-accordion>
          <cv-button class="create-group-btn" @click="createGroup">
            Создать группу
          </cv-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, type PropType, ref } from "vue";
import type { CourseModel } from "@/models/CourseModel";
import useCourseStore from "@/stores/modules/course";
import useUserStore from "@/stores/modules/user";
import type { UserModel } from "@/models/UserModel";
import UserComponent from "@/components/UserComponent.vue";
import GroupModal from "@/components/GroupModal.vue";

const props = defineProps({
  courseId: { type: Number, required: true }
});

const courseStore = useCourseStore();
const userStore = useUserStore();

const groupMembers = ref<Array<UserModel>>([]);
const groups = ['Группа 1', 'Группа 2', 'Группа 3'];

const course = ref<CourseModel>({ ...courseStore.newCourse });

const loading = ref(true);

onMounted(async () => {
  course.value = await courseStore.fetchCourseById(props.courseId);
  groupMembers.value = [userStore.user, userStore.user, userStore.user];
  loading.value = false;
})

function createGroup() {

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
  align-self end

/deep/ .bx--accordion__content
  padding-right 3rem

/deep/ .bx--structured-list
  margin-bottom 0

</style>