<template>
  <div>
    <span>Список курсов</span>

    <ul>
      <li v-for="el in course.activeLessons" :key="el.id">
        <Lesson :lesson="el"/>
      </li>
    </ul>
  </div>
</template>

<script>
import Lesson from '@/components/Lesson.vue';

export default {
  name: 'CourseView',
  components: { Lesson },
  props: {
    courseId: {
      type: Number,
      required: true,
    },
    courseProp: {
      required: false,
    },
  },

};
</script>

<style scoped>
</style>
