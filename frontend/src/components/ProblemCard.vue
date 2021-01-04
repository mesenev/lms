<template>
  <div class="problem bx--grid">
    <h6 class="text">{{ problem.name }}</h6>
    <TrashCan20 class="deleteButton" @click="deleteProblem(problem)" />
  </div>
</template>

<script lang="ts">
import {Prop, Component, Vue} from 'vue-property-decorator';
import ProblemModel from '@/models/ProblemModel';
import TrashCan20 from '@carbon/icons-vue/es/trash-can/20'

@Component({components: {
  TrashCan20,
}})
export default class CourseCalendarView extends Vue {
  @Prop() problem!: ProblemModel;
  @Prop() deleteProblem!: Function;
  //TrashCan20 = TrashCan20;
}
</script>

<style lang="stylus">
  .problem
    padding 20px
    display flex
    flex-direction row
    justify-content space-between
    align-items baseline
    margin-left: 0;
  .text
    border 1px solid black
    padding 10px
  .deleteButton
    width: 1rem;
    height: 1rem;
    margin-left: 10px;
</style>
