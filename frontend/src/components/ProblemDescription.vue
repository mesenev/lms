<template>
  <div>
    <div v-if="!isNaN(problem.id)"
         id="problem-description-container"
         class="problem-description"
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

<style lang="stylus" scoped>
.problem-description
  h2
    display none
</style>
