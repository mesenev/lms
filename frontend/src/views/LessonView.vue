<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
        <cv-tile kind="standard">
          <h1>{{ lesson.name }}</h1>
          <p>{{ lesson.deadline }}</p>
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
          <cv-accordion v-for="less in classwork" :key="less.id">
            <Problem :problem-prop='less'/>
          </cv-accordion>
        </div>
        <div class="homework">
          <h4>Домашнаяя работа</h4>
          <cv-accordion v-for="less in homework" :key="less.id">
            <Problem :problem-prop="less"/>
          </cv-accordion>
        </div>
      </div>
      <div class="add bx--col-lg-6">
        <h4>Материалы</h4>
        <cv-structured-list selectable>
          <template slot="items">
            <cv-structured-list-item v-for="material in materials" :key="material.id">
              <h5>{{material.name}}</h5>
              <span>{{material.text}}</span>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
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
import LessonContent from "@/models/LessonContent";

@Component({ components: { Problem } })
export default class HomeView extends Vue {
  private store = mainStore;

  get lesson(): LessonModel {
    return this.store.getLesson;
  }
  get materials(): Array<LessonContent> {
    console.log(this.lesson.materials);
    return this.lesson.materials;
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
  background-color var(--cds-ui-02)
</style>
