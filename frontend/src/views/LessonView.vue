<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
        <cv-tile kind="standard">
          <h1 v-if="!loading">{{ lesson.name }}</h1>
          <cv-skeleton-text v-else :heading="true" width="'50%'"/>
          <p v-if="!loading">{{ lesson.deadline }}</p>
          <cv-skeleton-text v-else width="'35%'"/>
        </cv-tile>
        <h4> Задачи урока: </h4>
      </div>
      <div class="bx--col-lg-9">
      </div>
      <div class="bx--col-lg-1">
      </div>
      <div class="less bx--col-lg-9">
        <div class="classwork">
          <h4>Классная работа</h4>
          <div v-if="!loading">
            <cv-accordion v-for="less in classwork" :key="less.id">
              <Problem :problem-prop='less'/>
            </cv-accordion>
          </div>
          <div v-else>
            <cv-accordion-skeleton/>
          </div>
        </div>
        <br>
        <br>
        <div class="homework">

          <h4>Домашнаяя работа</h4>
          <div v-if="!loading">
            <cv-accordion v-for="less in homework" :key="less.id">
              <Problem :problem-prop='less'/>
            </cv-accordion>
          </div>
          <div v-else>
            <cv-accordion-skeleton/>
          </div>
        </div>
      </div>
      <div class="bx--col-lg-1">
      </div>
      <div class="bx--col-lg-6">
        <div class="less bx--row-lg-6">
          <h4>Материалы</h4>
          <cv-structured-list v-if="!loading" selectable>
            <template slot="items">
              <cv-structured-list-item v-for="material in materials" :key="material.id">
                <Material :material-prop='material'/>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
          <cv-data-table-skeleton v-else :columns="1"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Material from "@/components/Material.vue";
import Problem from '@/components/Problem.vue';
import LessonContent from "@/models/LessonContent";
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import { lessonStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {Material, Problem } })
export default class LessonView extends Vue {
  @Prop() lessonId!: number;
  store = lessonStore;
  lesson!: LessonModel;
  loading = true;

  async created() {
    this.lesson = await this.store.fetchLessonById(this.lessonId);
    this.loading = false;
  }

  get materials(): Array<LessonContent> {
    return this.lesson.materials;
  }

  get classwork(): Array<ProblemModel> {
    return this.lesson.problems.filter(x => x.type === 'CW');
  }

  get homework(): Array<ProblemModel> {
    return this.lesson.problems.filter(x => x.type === 'HW');
  }
}
</script>

<style scoped lang="stylus">
.less
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.add
  background-color var(--cds-ui-02)
</style>
