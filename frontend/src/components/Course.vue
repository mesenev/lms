<template>
  <div>
    <router-link :to="{ name: 'CourseView', params: { courseId: course.id }}">
      <div class="wrapper">
        <span>{{ course.name }}</span>
      </div>
    </router-link>
  </div>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import { PropType } from 'vue';

export default {
  name: 'Course',
  props: {
    course: {
      type: Object as PropType<CourseModel>,
      required: true,
    },
  },
})
</script>
