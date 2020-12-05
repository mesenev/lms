<template>
  <div>
    <h1>Список уроков</h1>
  </div>
</template>

<script>

export default {
  name: 'CourseView',
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
