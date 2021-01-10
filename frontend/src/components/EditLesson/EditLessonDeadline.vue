<template>
  <div>
    <cv-date-picker kind="single"
                    date-label="Срок выполнения"
                    :cal-options="calOptions"
                    @change="changeLessonDeadline"
                    v-model="lessonDeadline">
    </cv-date-picker>
    <cv-button class="change-btn"
               :disabled="canChangeLessonDeadline"
               @click="changeLessonDeadline">
      Изменить срок
    </cv-button>
  </div>
</template>

<script lang="ts">
import LessonModel from "@/models/LessonModel";
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({})
export default class EditLessonDeadline extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;


  lessonDeadline: string = this.lesson.deadline;

  get canChangeLessonDeadline() {
    return this.lessonDeadline && _.isEqual(this.lesson.deadline, this.lessonDeadline);
  }

  changeLessonDeadline() {
    //
  }
}
</script>

<style lang="stylus">

</style>
