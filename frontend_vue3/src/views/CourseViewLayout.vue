<template>
  <transition mode="out-in" name="fade">
    <router-view/>
  </transition>
</template>

<script lang="ts" setup>
  import CourseModel from '@/models/CourseModel';
  import UserModel from '@/models/UserModel';
  import useCourseStore from "@/stores/modules/course";
  import useUserStore from "@/stores/modules/user";
  import { ref, onMounted } from 'vue'


  const props = defineProps(['courseId'])
  const userStore = useUserStore();
  const courseStore = useCourseStore();
  const course: CourseModel | null = ref(null)


  onMounted(async ()=> {
    courseStore.changeCurrentCourse(null);
    course.value = await courseStore.fetchCourseById(props.courseId);
    courseStore.changeCurrentCourse(course.value);
    if (!course.value.students.isEmpty()){
      const users = course.value.students.reduce(
      (previousValue: { [key: number]: UserModel }, currentValue) => {
        previousValue[currentValue.id] = currentValue;
        return previousValue;
      }, {});
      userStore.fetchStudentsMutation(users);
      return;
    }
    userStore.fetchStudentsMutation(null);
  })


</script>