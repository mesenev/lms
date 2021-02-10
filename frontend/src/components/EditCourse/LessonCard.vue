<template>
  <div class="card">
    <div class="title">
      <h5>{{ lesson.name }}</h5>
      <cv-tag v-for="problem in getLessonProblems"
              :key="problem"
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
                 :is="getIcon"
                 @click="manipulation(lesson); changeIcon()">
      </component>
    </div>
  </div>
</template>

<script lang="ts">
import LessonModel from "@/models/LessonModel";
import router from '@/router';
import _ from 'lodash';
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({})
export default class LessonCard extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;
  @Prop({ required: true }) manipulation!: Function;
  @Prop({ required: true }) mainIcon!: object;
  @Prop({ required: false }) changeMainIcon!: object;
  @Prop({ required: false }) secondIcon!: object;

  currentIcon = 0;

  icons = [this.mainIcon, this.changeMainIcon || this.mainIcon];

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

  editLesson() {
    router.push({name: 'lesson-edit', params: {lessonId: this.lesson.id.toString()}});
  }
}
</script>

<style scoped lang="stylus">
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
