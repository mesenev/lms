<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <h1 v-if="!loading && lesson" class="main-title">
        {{ lesson.name }}
      </h1>
      <cv-skeleton-text
        v-else :heading="true" class="main-title" width="'35%'"/>
      <div class="description-container">
        <span v-if="!loading && lesson">
          Дедлайн {{ lesson.deadline }}
        </span>
        <cv-skeleton-text v-else width="'35%'"/>
        <div v-if="isStaff">
          <cv-button-skeleton v-if="changingVisibility || !this.lesson" kind="ghost"/>
          <cv-button v-else
                     class="lesson-hide-button"
                     :icon="hiddenIcon"
                     kind="ghost"
                     v-on:click="changeLessonVisibility">
            {{ (lesson.is_hidden) ? "Открыть урок" : "Скрыть урок" }}
          </cv-button>
        </div>
      </div>
    </div>
    <div class="bx--row">
      <div class="items bx--col-lg-6">
        <div v-if="isProblemsEmpty">
          <h4 class="no-problems">В уроке пока нет задач</h4>
        </div>
        <div class="content-tasks-problems">
          <div v-if="classwork.length > 0" class="classwork">
            <h4 class="classwork-title">Классная работа</h4>
            <div v-if="!loading">
              <cv-accordion
                v-for="problem in classwork"
                :key="problem.id"
                align="end">
                <problem-list-component :problem-prop="problem"/>
              </cv-accordion>
            </div>
            <div v-else>
              <cv-accordion-skeleton/>
            </div>
          </div>
          <div v-if="homework.length > 0" class="homework">
            <h4 class="homework-title">Домашняя работа</h4>
            <div v-if="!loading">
              <cv-accordion
                align="end"
                v-for="problem in homework"
                :key="problem.id"
                class="accordion">
                <problem-list-component :problem-prop="problem"/>
              </cv-accordion>
            </div>
            <div v-else>
              <cv-accordion-skeleton/>
            </div>
          </div>
          <div v-if="extrawork.length > 0" class="extrawork">
            <h4 class="classwork-title">Дополнительные задания</h4>
            <div v-if="!loading">
              <cv-accordion v-for="problem in extrawork"
                            :key="problem.id"
                            align="end">
                <problem-list-component :problem-prop="problem"/>
              </cv-accordion>
            </div>
            <div v-else>
              <cv-accordion-skeleton/>
            </div>
          </div>
        </div>
      </div>
      <div class="bx--col-lg-4 content-info">
        <h2 class="content-info-title">Материалы</h2>
        <div v-if="isMaterialsEmpty">
          <h4 class="no-problems">В уроке пока нет материалов</h4>
        </div>
        <div class="content-info-materials" v-if="!loading">
          <cv-structured-list class="list">
            <template slot="items">
              <cv-structured-list-item
                v-for="material in materials"
                :key="material.id">
                <material-list-component :material-prop="material"/>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import MaterialListComponent from '@/components/lists/MaterialListComponent.vue';
import ProblemListComponent from '@/components/lists/ProblemListComponent.vue';
import MaterialModel from '@/models/MaterialModel';
import ProblemModel from '@/models/ProblemModel';
import lessonStore from '@/store/modules/lesson';
import materialStore from '@/store/modules/material';
import problemStore from '@/store/modules/problem';
import userStore from '@/store/modules/user';
import viewOff from '@carbon/icons-vue/es/view--off/32';
import view from '@carbon/icons-vue/es/view/32';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { MaterialListComponent, ProblemListComponent } })
export default class LessonView extends Vue {
  @Prop({ required: true }) lessonId!: number;
  lessonStore = lessonStore;
  problemStore = problemStore;
  userStore = userStore;
  materialStore = materialStore;
  loading = true;
  changingVisibility = false;

  get isProblemsEmpty() {
    if (this.problemStore.problemsByLesson[this.lessonId].length === 0) {
      return true;
    }
  }

  get isMaterialsEmpty() {
    return !this.materialStore._materials[this.lessonId].length;
  }

  get isStaff(): boolean {
    return this.userStore.user.staff_for.includes(Number(this.lesson?.course));
  }

  get hiddenIcon() {
    return (this.lesson?.is_hidden) ? viewOff : view;
  }

  //TODO: move materials in separate component
  get materials(): Array<MaterialModel> {
    if (this.lesson)
      return this.materialStore._materials[this.lessonId];
    return [];
  }

  get lesson() {
    return this.lessonStore.currentLesson;
  }

  get classwork(): Array<ProblemModel> {
    return this.problemStore.problemsByLesson[this.lessonId].filter(x => x.type === 'CW');
  }

  get homework(): Array<ProblemModel> {
    return this.problemStore.problemsByLesson[this.lessonId].filter(x => x.type === 'HW');
  }

  get extrawork(): Array<ProblemModel> {
    return this.problemStore.problemsByLesson[this.lessonId].filter(x => x.type === 'EX');
  }

  async created() {
    await this.problemStore.fetchProblemsByLessonId(this.lessonId);
    await this.materialStore.fetchMaterialsByLessonId(this.lessonId);
    this.loading = false;
  }

  async changeLessonVisibility() {
    this.changingVisibility = true;
    await this.lessonStore.patchLesson(
      { id: this.lessonId, is_hidden: !this.lesson?.is_hidden },
    );
    this.changingVisibility = false;
  }

}
</script>

<style scoped lang="stylus">

.description-container
  margin-left var(--cds-spacing-05)
  padding-left var(--cds-spacing-05)

.lesson-hide-button
  margin-left -1rem

.accordion
  height 100%

.no-problems
  margin 1rem

.content-info-title
  margin 1rem

.content-tasks-title
  margin 1rem

.less
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.add
  background-color var(--cds-ui-02)

.back-to-lesson
  background-color transparent
  border 1px solid var(--cds-text-01)
  cursor pointer
  user-select none

.content
  margin-top 1rem

  &-info
    margin-left 1rem
    height 100%

    .list
      margin 1rem 0

  &-tasks, &-info
    background-color var(--cds-ui-02)
    padding 1rem

  /deep/ .bx--accordion__heading
    align-items center


  .classwork, .homework, extrawork
    margin-bottom 1rem

    &-title
      padding-left 1rem
      margin 1rem 0

</style>
