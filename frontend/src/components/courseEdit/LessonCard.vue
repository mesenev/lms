<template>
  <div class="card">
    <div class="title">
      <h5>{{ lesson.name }}</h5>
      <cv-tag v-for="(problem, id) in getLessonProblems"
              :key="id"
              kind="red"
              :label="problem">
      </cv-tag>
    </div>
    <div class="icons">
      <component class="icon"
                 v-if="secondIcon"
                 :is="secondIcon"
                 @click="editLesson">
      </component>
      <component class="icon"
                 v-if="getIcon"
                 :is="getIcon"
                 @click="manipulation(lesson); changeIcon()">
      </component>
    </div>
  </div>
</template>

<script lang="ts">
import { Prop, Component, Vue } from 'vue-property-decorator';
import LessonModel from "@/models/LessonModel";
import router from '@/router';
import _ from 'lodash';

@Component({})
export default class CourseCalendarView extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;
  @Prop({ required: true }) manipulation!: Function;
  @Prop({ required: false }) icon!: object;
  @Prop({ required: false }) onClickIcon!: object;
  @Prop({ required: false }) secondIcon!: object;

  currentIcon = 0;

  icons = [this.icon, this.onClickIcon];

  get getIcon() {
    return this.icons[this.currentIcon];
  }

  changeIcon() {
    this.currentIcon = (this.currentIcon + 1) % this.icons.length;
  }

  get getLessonProblems() {
    const problems: string[] = [];
    for (const [key, value] of Object.entries(this.lesson)) {
      if (_.isArrayLike(value) && _.isEmpty(value)) {
        problems.push(`Empty ${key}`);
      }
    }
    return problems;
  }

  // TODO Correct push to LessonEditView
  editLesson() {
    router.push({ name: 'LessonEditView', params: { lessonId: this.lesson.id.toString() } });
  }
}
</script>

<style lang="stylus">
  .card
    padding 20px
    display flex
    flex-direction row
    justify-content space-between
    align-items center

  .title
    display flex
    flex-direction row
    align-items baseline
    h5
      margin-right: 5px

  .icon
    transition ease-in-out 0.1s
  .icon:active
    transform scale(0.9)
  .icon:nth-child(odd)
    margin: 0 10px
</style>
