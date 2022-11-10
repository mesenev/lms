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
    <div class="bx--row lesson-content">
      <div :class="(isProblemsEmpty) ? 'empty-items bx--col-lg-6 bx--col-md-6'
      : 'items bx--col-lg-6 bx--col-md-6'">
        <div v-if="isProblemsEmpty">
          <empty-list-component list-of="problems" :text="emptyProblemsText"/>
        </div>
        <div v-else class="content-tasks-problems">
          <div v-if="classwork.length > 0" class="classwork">
            <h4 class="classwork-title">Классная работа</h4>
            <div v-if="!loading">
              <problem-list-component :task-list="classwork"></problem-list-component>
            </div>
            <div v-else>
              <cv-accordion-skeleton/>
            </div>
          </div>
          <div v-if="homework.length > 0" class="homework">
            <h4 class="homework-title">Домашняя работа</h4>
            <div v-if="!loading">
              <problem-list-component :task-list="homework"/>
            </div>
            <div v-else>
              <cv-accordion-skeleton/>
            </div>
          </div>
          <div v-if="extrawork.length > 0" class="extrawork">
            <h4 class="classwork-title">Дополнительные задания</h4>
            <div v-if="!loading">
              <problem-list-component :task-list="extrawork"/>
            </div>
            <div v-else>
              <cv-accordion-skeleton/>
            </div>
          </div>
        </div>
      </div>
      <div class="bx--col-lg-4 bx--col-md-4 content-info">
        <div v-if="isMaterialsEmpty">
          <empty-list-component :text="emptyMaterialsText" list-of="materials"/>
        </div>
        <h2 v-else class="content-info-title">Материалы</h2>
        <div class="content-info-materials" v-if="!loading">
          <cv-structured-list class="list">
            <template slot="items">
              <cv-structured-list-item
                v-for="material in studentMaterials"
                :key="material.id">
                <material-list-component :material-prop="material"/>
              </cv-structured-list-item>
            </template>
            <template slot="items" v-if="isStaff">
              <cv-structured-list-item
                v-for="material in teacherMaterials"
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
import EmptyListComponent from "@/components/EmptyListComponent.vue";

@Component({ components: { MaterialListComponent, ProblemListComponent, EmptyListComponent } })
export default class LessonView extends Vue {
  @Prop({ required: true }) lessonId!: number;
  lessonStore = lessonStore;
  problemStore = problemStore;
  userStore = userStore;
  materialStore = materialStore;
  loading = true;
  changingVisibility = false;
  emptyProblemsText = '';
  emptyMaterialsText = '';

  async created() {
    this.emptyProblemsText = 'В данный момент нет доступных задач.';
    this.emptyMaterialsText = 'Похоже, доступные материалы отсутствуют.';
    await this.problemStore.fetchProblemsByLessonId(this.lessonId);
    await this.materialStore.fetchMaterialsByLessonId(this.lessonId);
    this.loading = false;
  }

  get isProblemsEmpty() {
    if (this.problemStore.problemsByLesson[this.lessonId].length === 0) {
      return true;
    }
  }

  get isMaterialsEmpty() {
    if (!this.isStaff)
      return !this.studentMaterials.length;
    return !this.materialStore._materials[this.lessonId].length;
  }

  get isStaff(): boolean {
    return this.userStore.user.staff_for.includes(Number(this.lesson?.course));
  }

  get hiddenIcon() {
    return (this.lesson?.is_hidden) ? viewOff : view;
  }

  //TODO: move materials in separate component
  get studentMaterials(): Array<MaterialModel> {
    if (this.lesson)
      return this.materialStore._materials[this.lessonId].filter(el => !el.is_teacher_only)
        .sort((a, b) => a.id - b.id);
    return [];
  }

  get teacherMaterials(): Array<MaterialModel> {
    if (this.lesson)
      return this.materialStore._materials[this.lessonId].filter(el => el.is_teacher_only)
        .sort((a, b) => a.id - b.id);
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

.content-info-materials
  margin-bottom 1rem


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

.lesson-content
  margin-top 2rem

.empty-items
  background-color var(--cds-ui-background)
  padding-top 1rem
  margin-bottom 1rem
  margin-right 1rem
  padding-bottom 1rem

.items
  background-color: var(--cds-ui-02)
  padding-top 1rem
  padding-bottom 1rem
  margin-bottom 1rem
  margin-right 1rem
</style>
