<template>
  <router-link :to="{ name: 'LessonView', params: { lessonId: lesson.id }}">
    <span> {{ lesson.name }}</span>
  </router-link>
</template>

<script lang="ts">
import LessonModel from '@/models/LessonModel';
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'Lesson',
  props: {
    lesson: {
      required: true,
      type: Object as PropType<LessonModel>,
    },
  },
});
</script>

<style scoped lang="stylus">

</style>
