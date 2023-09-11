<template>
  <!-- > ToDo fix transition <-->
  <transition>
    <router-view v-if="lesson"/>
    <cv-loading v-else/>
  </transition>

</template>

<script lang="ts" setup>
import LessonModel from '@/models/LessonModel';
import useLessonStore from "@/stores/modules/lesson";
import { computed, onMounted, ref, Ref, reactive } from "vue";

const props = defineProps({ lessonId: {type: Number, required: true} })
const lesson: LessonModel | null = ref(null);
const lessonStore = useLessonStore();

lessonStore.changeCurrentLesson(null);
onMounted(async () =>{
  lesson.value =  await lessonStore.fetchLessonById(props.lessonId);
  lessonStore.changeCurrentLesson(lesson.value);
  await lessonStore.fetchLessonsByCourseId(lesson.value.course);
})
</script>
