<template>
  <router-view v-slot="{Component}">
    <transition mode="out-in" name="fade">
      <component :is="Component"/>
    </transition>
  </router-view>
</template>

<script lang="ts" setup>
import type { CourseModel } from '@/models/CourseModel';
import type { UserModel } from '@/models/UserModel';
import useCourseStore from "@/stores/modules/course";
import useUserStore from "@/stores/modules/user";
import { ref, onMounted } from 'vue'

import useGroupStore from "@/stores/modules/group";
import type { GroupModel } from "@/models/GroupModel";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";


const props = defineProps({
  courseId: { type: Number, required: true }
});

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();


const courseStore = useCourseStore();
const groupStore = useGroupStore();

const groups = ref<Array<GroupModel>>([]);

const course = ref<CourseModel>({ ...courseStore.newCourse });


onMounted(async () => {
  courseStore.changeCurrentCourse(null);
  course.value = await courseStore.fetchCourseById(props.courseId);
  courseStore.changeCurrentCourse(course.value);
  groups.value = await groupStore.fetchGroupsByCourseId(props.courseId);
  //
  // if (groups.value.length !== 0) {
  //   const users = groups.value.students.reduce(
  //       (previousValue: { [key: number]: UserModel }, currentValue) => {
  //         previousValue[currentValue.id] = currentValue;
  //         return previousValue;
  //       }, {});
  //   userStore.fetchStudentsMutation(users);
  // }
})


</script>