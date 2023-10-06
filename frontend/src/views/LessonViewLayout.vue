<template>
  <router-view v-slot="{Component}">
    <transition  mode="out-in" name="fade">
      <component :is="Component"/>
    </transition>
  </router-view>
</template>

<script lang="ts" setup>
import type { LessonModel } from '@/models/LessonModel';
import useLessonStore from "@/stores/modules/lesson";
import { onMounted, ref } from "vue";

const props = defineProps({ lessonId: {type: String, required: true} })
const lesson = ref<LessonModel | null>(null);
const lessonStore = useLessonStore();


onMounted(async () =>{
  lessonStore.changeCurrentLesson(null);
  lesson.value =  await lessonStore.fetchLessonById(parseInt(props.lessonId));
  lessonStore.changeCurrentLesson(lesson.value);
  await lessonStore.fetchLessonsByCourseId(lesson.value.course);
})
</script>
