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
import api from "@/stores/services/api";


const props = defineProps(['courseId'])
const userStore = useUserStore();
const courseStore = useCourseStore();
const groupStore = useGroupStore();
const course = ref<CourseModel | null>(null)


onMounted(async () => {
  courseStore.changeCurrentCourse(null);
  course.value = await courseStore.fetchCourseById(props.courseId);
  courseStore.changeCurrentCourse(course.value);
  await groupStore.fetchGroupsByCourseId(props.courseId);
  if (course.value.students.length !== 0) {
    const users = course.value.students.reduce(
        (previousValue: { [key: number]: UserModel }, currentValue) => {
          previousValue[currentValue.id] = currentValue;
          return previousValue;
        }, {});
    userStore.fetchStudentsMutation(users);
  }
})


</script>