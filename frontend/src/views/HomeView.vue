<template>
  <div>
    <span>Home</span>
    <div>
      <router-link :to="{ name: 'CourseView', params: { courseId: 1 }}">Курс</router-link>
      <br>
      <router-link :to="{ name: 'LessonView', params: { lessonId: 1 }}">Урок</router-link>
      <br>
      <router-link :to="{ name: 'ProblemView', params: { problemId: 1 }}">Задача</router-link>
      <br>
    </div>
  </div>
</template>

<script lang="ts">

export default {
  name: 'HomeView',
  data() {
    return {};
  },
  methods: {},
  computed: {},
};
</script>

<style scoped>

</style>
