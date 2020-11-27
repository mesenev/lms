<template>
  <router-link :to="{ name: 'ProblemView', params: { problemId: 1 }}">
    <span> {{ problem.name }}</span>
  </router-link>
</template>

<script lang="ts">
import ProblemModel from '@/models/ProblemModel';
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'Lesson',
  props: {
    problemProp: {
      required: true,
      type: Object as PropType<ProblemModel>, // TODO: investigate this Object as PropType<ololo>
    },
  },
  computed: {
    problem(): ProblemModel {
      return this.problemProp;
    },
  },

});
</script>

<style scoped lang="stylus">

</style>
