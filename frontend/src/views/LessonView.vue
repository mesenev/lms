<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
          <cv-tile kind="standard">
          <h1>{{lesson.name}}</h1>
          <p>{{lesson.deadline}}</p>
        </cv-tile>
          <h4> Задачи урока: </h4>
        </div>
      <div class="bx--col-lg-10">
          </div>
      <div class="add bx--col-lg-6">
        <p>Пользователи</p>
      </div>
      <div class="less bx--col-lg-10">
        <div class="classwork">
          <h4>Классная работа</h4>
            <cv-accordion align="align" v-for="less in classwork" :key="less.id">
              <Problem :problem-prop='less'/>
            </cv-accordion>
          </div>
        <div class="homework">
          <h4>Домашнаяя работа</h4>
            <cv-accordion align="align" v-for="less in homework" :key="less.id">
              <Problem :problem-prop="less"/>
            </cv-accordion>
          </div>
      </div>
      <div class="add bx--col-lg-6">
        <p>{{lesson.lessoncontent}}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Problem from '@/components/Problem.vue';
import ProblemModel from '@/models/ProblemModel';
import { mainStore } from '@/store';
import Vue from 'vue';
import Component from 'vue-class-component';
import LessonModel from '@/models/LessonModel';

@Component({ components: { Problem } })
export default class HomeView extends Vue {
  private store = mainStore;

  get lesson(): LessonModel {
    return this.store.getLesson;
  }

  get classwork(): Array<ProblemModel> {
    return this.store.getLesson.classwork;
  }

  get homework(): Array<ProblemModel> {
    return this.store.getLesson.homework;
  }
}
</script>

<style lang="stylus">
.less
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)
.add
  background-color ghostwhite
</style>
