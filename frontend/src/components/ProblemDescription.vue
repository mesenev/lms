<template>
  <div>
    <div v-if="!isNaN(problem.id)"
         id="problem-description-container"
         v-html="problem.description">
    </div>
    <cv-skeleton-text v-else/>
  </div>
</template>

<script lang="ts">
import ProblemModel from '@/models/ProblemModel';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class ProblemDescription extends Vue {
  @Prop({ required: true }) problem!: ProblemModel;
}
</script>

<style lang="stylus">
#problem-description-container
  padding 0.5rem
  h2, .timing, .submit
    display none

  table.sample
    border 1px

    *
      padding 5px

    td
      border 1px solid black

  button.copy_button
    display none
</style>

<style lang="stylus" scoped>

</style>
