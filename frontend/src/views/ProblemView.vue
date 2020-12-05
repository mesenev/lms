<template>
  <div>
    <h1>
      {{ problem.name }}
      <span v-if="problem.completed">done!</span>
      <span v-else>not done yet!</span>
    </h1>
    <p> {{ problem.description }}</p>
  </div>
</template>

<script lang="ts">

import ProblemModel from '@/models/ProblemModel';

export default {
  name: 'ProblemView',
  props: {},
  data() {
    return {
      problem: {
        id: 7,
        name: 'Чё тебе надо у меня дома, мент',
        description: 'К джентельмену вломились силовые структуры.'
          + ' Помогите ему выяснить причину их появления и, по возможности,'
          + ' получить компенсацию за поломанное имущество.',
        completed: false,
      } as ProblemModel,
    };
  },
  methods: {},
  computed: {},
};
</script>

<style scoped>

</style>
