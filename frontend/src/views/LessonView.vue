<template>
  <div>
    <Problem v-for="p in problems" :key="p.id" :problemProp="p"/>
  </div>
</template>

<script lang="ts">
import Problem from '@/components/Problem.vue';
import CourseModel from '@/models/CourseModel';
import ProblemModel from '@/models/ProblemModel';
import { mainStore } from '@/store';
import { PropType } from 'vue';

export default {
  name: 'LessonView',
  components: { Problem },
  props: {
    todo: {
      type: Object as PropType<CourseModel>,
      required: true,
    },
  },
  methods: {},
  computed: {
    problems(): Array<ProblemModel> {
      return mainStore.getProblems;
    },
  },
};
</script>

<style scoped>

</style>
