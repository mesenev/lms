<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1 v-if="!loading && lesson" class=""> Урок: {{ lesson.name }} </h1>
        <cv-skeleton-text v-else :heading="true" class="main-title" width="'35%'"/>
        <div v-if="!loading && lesson" class="lesson-info">
          <span>
            Дедлайн: {{ lesson.deadline }}
          </span>
        </div>
        <cv-skeleton-text v-else width="'35%'"/>
        <div class="description-container">
          <span v-if="!loading && lesson" class="lesson-description">
             {{ lesson.description }}
          </span>
          <cv-skeleton-text v-else width="'35%'"/>
        </div>
      </div>
    </div>
    <div class="bx--row lesson-content">
      <div :class="(isProblemsEmpty) ? 'empty-items bx--col-lg-6 bx--col-md-6'
      : 'items bx--col-lg-6 bx--col-md-6'">
        <div v-if="!loading">
          <div v-if="isProblemsEmpty">
            <empty-list-component list-of="problems" :text="emptyProblemsText"/>
          </div>
          <div v-else class="content-tasks-problems">
            <div v-if="classwork.length > 0" class="classwork">
              <h4 class="classwork-title title">Классная работа</h4>
              <problem-list-component :task-list="classwork"></problem-list-component>
            </div>
            <div v-if="homework.length > 0" class="homework">
              <h4 class="homework-title title">Домашняя работа</h4>
              <problem-list-component :task-list="homework"/>
            </div>
            <div v-if="extrawork.length > 0" class="extrawork">
              <h4 class="classwork-title title">Дополнительные задания</h4>
              <problem-list-component :task-list="extrawork"/>
            </div>
            <div v-if="exams.length > 0" class="tests">
              <h4 class="classwork-title title">Тесты</h4>
              <exam-list-component :exams-list="exams"/>
            </div>
          </div>
        </div>
        <cv-skeleton-text :paragraph="true" :line-count="5" v-else/>
      </div>
      <div
        :class="(!loading && isMaterialsEmpty) ? ('bx--col-lg-4 bx--col-md-4 content-info-empty')
         : ('bx--col-lg-4 bx--col-md-4 content-info')">
        <div v-if="!loading">
          <div v-if="isMaterialsEmpty" class="content-info-empty">
            <empty-list-component :text="emptyMaterialsText" list-of="materials"/>
          </div>
          <div v-else>
            <h2 class="content-info-title">Материалы</h2>
            <div class="content-info-materials" v-if="!loading">
              <cv-structured-list class="list">
                <template slot="items">
                  <cv-structured-list-item
                    v-for="material in studentMaterials"
                    :key="material.id">
                    <material-list-component :material-prop="material"
                                             :show-visibility="true"
                                             :is-staff="isStaff"/>
                  </cv-structured-list-item>
                </template>
                <template slot="items" v-if="isStaff">
                  <cv-structured-list-item
                    v-for="material in teacherMaterials"
                    :key="material.id">
                    <material-list-component :material-prop="material"
                                             :show-visibility="true"
                                             :is-staff="isStaff"/>
                  </cv-structured-list-item>
                </template>
              </cv-structured-list>
            </div>
          </div>
        </div>
        <cv-skeleton-text :paragraph="true" :line-count="5" v-else/>
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
import examStore from '@/store/modules/exam';
import { Component, Prop, Vue } from 'vue-property-decorator';
import EmptyListComponent from "@/components/EmptyListComponent.vue";
import ExamModel from "@/models/ExamModel";
import ExamListComponent from "@/components/lists/ExamListComponent.vue";

@Component({
  components: {
    ExamListComponent,
    MaterialListComponent,
    ProblemListComponent,
    EmptyListComponent
  }
})
export default class LessonView extends Vue {
  @Prop({ required: true }) lessonId!: number;
  lessonStore = lessonStore;
  problemStore = problemStore;
  userStore = userStore;
  materialStore = materialStore;
  examStore = examStore;
  loading = true;
  emptyProblemsText = '';
  emptyMaterialsText = '';

  async created() {
    this.emptyProblemsText = 'В данный момент нет доступных задач.';
    this.emptyMaterialsText = 'Похоже, доступные материалы отсутствуют.';
    await this.problemStore.fetchProblemsByLessonId(this.lessonId);
    await this.materialStore.fetchMaterialsByLessonId(this.lessonId);
    await this.examStore.fetchExamsByLessonId(this.lessonId);
    this.loading = false;
  }

  get isProblemsEmpty() {
    if ((this.problems ?? []).length === 0 && (this.exams ?? []).length === 0) {
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

  get problems() {
    return this.problemStore.problemsByLesson[this.lessonId];
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

  get exams(): Array<ExamModel> {
    return this.examStore.examsByLesson[this.lessonId];
  }

}
</script>

<style scoped lang="stylus">
.lesson-info
  display flex
  flex-direction row
  align-items center
  padding-left 1rem
  font-weight var(--cds-display-02-font-weight)
  margin-top 1rem
  color var(--cds-text-02)
  gap 2rem

.description-container
  max-width 70%
  word-break break-word
  color var(--cds-text-02)
  font-weight var(--cds-display-02-font-weight)
  margin-top var(--cds-spacing-03)
  padding-left 1rem

.lesson-hide-button
  margin-left -1rem

.accordion
  height 100%

.no-problems
  margin 1rem

.content-info-materials
  max-height 300px
  min-height 300px
  overflow auto
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
    margin-bottom 1rem

    &-empty
      margin-bottom 1rem
      height 400px
      display flex
      align-items center

    &-title
      color var(--cds-text-01)

    .list
      margin 1rem 0

  &-tasks, &-info
    background-color var(--cds-ui-01)
    padding 1rem

  /deep/ .bx--accordion__heading
    align-items center


.classwork, .homework, .extrawork
  margin-bottom 1rem

  &-title
    font-weight bold
    color var(--cds-text-01)
    padding-left 1rem
    margin 1rem 0

.empty-items
  background-color var(--cds-ui-01)
  display flex
  align-items center
  padding-top 1rem
  margin-bottom 1rem
  margin-right 1rem
  padding-bottom 1rem

.items
  background-color: var(--cds-ui-01)
  padding-top 1rem
  padding-bottom 1rem
  margin-bottom 1rem
  margin-right 1rem
</style>
