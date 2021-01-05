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
import { Component, Prop, Vue } from 'vue-property-decorator';
import { mainStore } from '@/store';
import LessonModel from "@/models/LessonModel";
import _ from 'lodash';
import { modBStore } from '@/store';
@Component({})
export default class EditLessonDeadline extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;

  store = modBStore;

  lessonDeadline: string = this.lesson.deadline;

  get canChangeLessonDeadline() {
      return this.lessonDeadline && _.isEqual(this.lesson.deadline, this.lessonDeadline);
  }

  changeLessonDeadline() {
    this.store.changeLessonDeadline(this.lessonDeadline);

  }
}
</script>

<style lang="stylus">

</style>
