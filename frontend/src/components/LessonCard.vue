<template>
  <div class="lesson bx--grid">
    <h5>{{ lesson.name }}</h5>
    <TrashCan32 @click="deleteLesson(lesson)" />
  </div>
</template>

<script lang="ts">
import {Prop, Component, Vue} from 'vue-property-decorator';
import LessonModel from "@/models/LessonModel";

@Component({})
export default class CourseCalendarView extends Vue {
  @Prop() lesson!: LessonModel;
  @Prop() deleteLesson!: Function;
}
</script>

<style lang="stylus">
  #titleCourse
    padding 10px 0

  .lesson
    padding 20px
    display flex
    flex-direction row
    justify-content space-between
    align-items baseline
</style>
