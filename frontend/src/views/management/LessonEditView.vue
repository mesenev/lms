<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>{{ isNewLesson ? 'Создание урока' : 'Редактирование урока' }}</h1>
    </div>
    <div class="box--col-lg-8">
      <cv-text-input
        label="Название урока"
        v-model.trim="lessonEdit.name"
      />
      <cv-date-picker
        class="deadLine"
        kind="single"
        v-model="lessonEdit.deadline"
        date-label="Дедлайн"
      />
      <cv-search class="search" v-model="query"></cv-search>
      <cv-structured-list class="classwork">
        <template slot="headings">
          <cv-structured-list-heading>
            Классная работа
          </cv-structured-list-heading>
        </template>
        <template slot="items">
          <cv-structured-list-item class="work"
                  v-for="classwork in getClassworks"
                  :key="classwork.id">
            <div>
              <h4>{{ classwork.name }}</h4>
            </div>
          </cv-structured-list-item>
        </template>
      </cv-structured-list>
      <cv-structured-list class="homework">
        <template slot="headings">
          <cv-structured-list-heading>
            Домашняя работа
          </cv-structured-list-heading>
        </template>
        <template slot="items">
          <cv-structured-list-item class="work"
                  v-for="homework in getHomeworks"
                  :key="homework.id">
            <div>
              <h4>{{ homework.name }}</h4>
            </div>
          </cv-structured-list-item>
        </template>
      </cv-structured-list>
      <div class="lesson-buttons">
        <EditLessonModal
        :lesson="lessonEdit"
        class="edit--lesson-props"/>
        <EditLessonMaterialsModal
        :lesson="lessonEdit"
        class="edit--lesson-props"/>
      </div>
      <cv-button class="finishButton" :disabled="!isChanged">{{ isNewLesson ? 'Создать урок' : 'Изменить урок' }}</cv-button>

    </div>
  </div>
</template>

<script lang="ts" >
import { modBStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';
import LessonModel from "@/models/LessonModel";
import ProblemModel from "@/models/ProblemModel";
import searchByProblems from '@/common/searchByProblems'
import EditLessonModal from "@/components/LessonEdit/EditLessonModal.vue";
import EditLessonMaterialsModal from "@/components/LessonEdit/EditLessonMaterialsModal.vue";
@Component({
  components: {EditLessonMaterialsModal, EditLessonModal},
})
export default class CourseCalendarView extends Vue {
  @Prop() courseId!: number;
  store = modBStore;
  lesson: LessonModel = {
    id: NaN,
    name: '',
    classwork: this.store.getLesson.classwork,
    homework: this.store.getLesson.homework,
    materials: [],
    deadline: '',
    lessonContent: ''
  }
  lessonEdit: LessonModel = { ...this.lesson }
  query = '';
  search(problems: ProblemModel[]): ProblemModel[] {
    return searchByProblems(this.query, problems);
  }
  get getClassworks(): ProblemModel[] {
    return this.search(this.lessonEdit.classwork);
  }
  get getHomeworks(): ProblemModel[] {
    return this.search(this.lessonEdit.homework);
  }
  get isNewLesson(): boolean {
    return isNaN(this.lessonEdit.id);
  }
  get isChanged(): boolean {
    return !_.isEqual(this.lesson, this.lessonEdit);
  }
}
</script>

<style scoped lang="stylus">
.head-content
  margin: 50px
.bx--col
  margin: 2rem
.lesson-buttons
  display flex
  flex-direction row
.works-col
  margin-right 0
  margin-bottom 1rem
  margin-left 1rem
  margin-top 1rem
  display flex
.work div
  padding 1rem 1rem 0.5rem 1rem
.classwork, .homework
  margin: 20px 0
.deadLine
  padding-top 10px
.finishButton
  margin-top 25px
  display flex
  flex-direction row
  width 204px
  background-color var(--cds-interactive-01)
.search
  margin 10px 0
.addButton
  background-color var(--cds-interactive-02)
  margin-left 25px

//border black 1px solid
.main-content
  border 2px black solid;
  margin: 50px
.bx--text-input
  border: 2px solid #222;
  padding: 5
  display: block;
  width: 100%;
  height: 50px;
  background: #fff;
.change__btn
  margin-top: 10px
  background-color: var(--cds-ui-05)
  &:hover
    background-color: var(--cds-ui-04)
</style>
