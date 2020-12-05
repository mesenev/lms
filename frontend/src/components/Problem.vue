<template>
  <router-link :to="{ name: 'ProblemView', params: { problemId: 1 }}">
    <span> {{ problem.name }}</span>
  </router-link>
</template>

<script>

export default {
  name: 'Problem',
  props: {
    problemProp: {
      required: true,
    },
  },
  computed: {
    problem() {
      return this.problemProp;
    },
  },

};
</script>

<style scoped lang="stylus">
</style>
