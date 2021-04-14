<template>
  <div>
    <h4 v-if="!isNaN(problem.id)"
        class="problem-description-container"
        v-html="problem.description">
    </h4>
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


.problem-description-container
  margin 0.5rem
  font-size 1.15rem

</style>

<style lang="stylus" scoped>

</style>
