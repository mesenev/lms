<template>
  <div class="bx--grid">
    <div class="bx--row title">
      <h1 v-if="!loading">{{ lesson.name }}</h1>
      <cv-skeleton-text v-else :heading="true" width="'50%'"/>
      <p v-if="!loading">Дедлайн {{ lesson.deadline }}</p>
      <cv-skeleton-text v-else width="'35%'"/>
    </div>
    <div class="bx--row content">
      <div class="bx--col-lg-9 content-tasks">
        <h2 class="content-tasks-title">Задачи урока</h2>
        <div class="content-tasks-problems">
          <div class="classwork">
            <h4 class="classwork-title">Классная работа</h4>
            <div v-if="!loading">
              <cv-accordion align="end"
                            v-for="problem in classwork"
                            :key="problem.id"
              >
                <problem-list-component :problem-prop="problem"/>
              </cv-accordion>
            </div>
            <div v-else>
              <cv-accordion-skeleton/>
            </div>
          </div>
          <div class="homework">
            <h4 class="homework-title">Домашняя работа</h4>
            <div v-if="!loading">
              <cv-accordion
                align="end"
                v-for="problem in homework"
                :key="problem.id"
              >
                <problem-list-component :problem-prop="problem"/>
              </cv-accordion>
            </div>
            <div v-else>
              <cv-accordion-skeleton/>
            </div>
          </div>
        </div>
      </div>
      <div class="bx--col-lg-6 content-info">
        <h2 class="content-info-title">Материалы</h2>
        <div class="content-info-materials" v-if="!loading">
          <cv-structured-list class="list">
            <template slot="items">
              <cv-structured-list-item
                v-for="material in materials"
                :key="material.id"
              >
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
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import lessonStore from '@/store/modules/lesson';
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({components: {MaterialListComponent, ProblemListComponent}})
export default class LessonView extends Vue {
  @Prop() lessonId!: number;
  store = lessonStore;
  userStore = userStore;
  lesson!: LessonModel;
  loading = true;

  async created() {
    this.lesson = await this.store.fetchLessonById(this.lessonId);
    const stds = await this.userStore.fetchStudentsByCourseId(this.lesson.course);
    this.loading = false;
  }

  get materials(): Array<MaterialModel> {
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

.title
  margin-top 1rem
  display flex
  flex-direction column
  align-items flex-start

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
  .classwork, .homework
    margin-bottom 1rem
    &-title
      padding-left 1rem
      margin 1rem 0

</style>
