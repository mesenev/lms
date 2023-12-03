<template>
  <div>
    groups of {{ course.name }}
  </div>
</template>

<script setup lang="ts">
import { onMounted, type PropType, ref } from "vue";
import type { CourseModel } from "@/models/CourseModel";
import useCourseStore from "@/stores/modules/course";

const props = defineProps({
  courseId: {type: Number, required: true}
});

const courseStore = useCourseStore();

const course = ref<CourseModel>({ ...courseStore.newCourse });

onMounted(async () => {
  course.value = await courseStore.fetchCourseById(props.courseId);
})

</script>


<style scoped lang="stylus">

</style>