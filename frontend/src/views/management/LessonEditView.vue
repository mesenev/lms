<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>{{ isNewLesson ? 'Создание урока' : 'Редактирование урока' }}</h1>
    </div>
    <cv-loading v-if="fetchingLesson"/>
    <div v-else class="bx--col-lg-8">
      <cv-inline-notification
        v-if="showNotification"
        @close="hideSuccess"
        :kind="notificationKind"
        :sub-title="notificationText"
      />
      <cv-text-input
        label="Название урока"
        v-model.trim="lessonEdit.name"/>
      <cv-text-input
        label="Описание урока"
        v-model.trim="lessonEdit.description"/>
      <cv-date-picker
        class="deadLine"
        kind="single"
        v-model="lessonEdit.deadline"
        date-label="Дедлайн"
        :cal-options=calOptions
      />
      <cv-search class="search" v-model="query"></cv-search>
      <cv-structured-list class="classwork">
        <template slot="headings">
          <cv-structured-list-heading> Классная работа</cv-structured-list-heading>
        </template>
        <template slot="items">
          <cv-structured-list-item
            class="work" v-for="classwork in getClasswork" :key="classwork.id">
            <div><h4>{{ classwork.name }}</h4></div>
          </cv-structured-list-item>
        </template>
      </cv-structured-list>
      <cv-structured-list class="homework">
        <template slot="headings">
          <cv-structured-list-heading> Домашняя работа</cv-structured-list-heading>
        </template>
        <template slot="items">
          <cv-structured-list-item class="work" v-for="homework in getHomework" :key="homework.id">
            <div><h4>{{ homework.name }}</h4></div>
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
      <cv-button class="finishButton" :disabled="!isChanged" v-on:click="createOrUpdate">
        {{ isNewLesson ? 'Создать урок' : 'Изменить урок' }}
      </cv-button>
    </div>
  </div>
</template>

<script lang="ts">
import searchByProblems from '@/common/searchByProblems'
import EditLessonMaterialsModal from "@/components/EditLesson/EditLessonMaterialsModal.vue";
import EditLessonModal from "@/components/EditLesson/EditLessonModal.vue";
import CatsProblemModel from '@/models/CatsProblemModel';
import LessonModel from "@/models/LessonModel";
import ProblemModel from "@/models/ProblemModel";
import router from "@/router";
import lessonStore from "@/store/modules/lesson";
import Settings20 from '@carbon/icons-vue/es/settings/20';
import TrashCan20 from '@carbon/icons-vue/es/trash-can/20';
import axios from "axios";
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { EditLessonMaterialsModal, EditLessonModal } })
export default class LessonEditView extends Vue {
  @Prop({ required: true }) lessonId!: number;
  TrashCan = TrashCan20;
  Settings = Settings20;
  showNotification = false;
  notificationKind = 'success';
  notificationText = '';
  fetchingLesson = true;

  calOptions = {
    ateFormat: 'Y/m/d',
  }

  store = lessonStore;
  query = '';

  lesson: LessonModel = {
    id: NaN,
    course: NaN,
    description: '',
    name: '',
    problems: [],
    materials: [],
    deadline: '',
    lessonContent: '',
  };
  lessonEdit: LessonModel = { ...this.lesson, course: this.lesson.course };

  hideSuccess() {
    this.showNotification = false;
  }

  async created() {
    this.lesson = await this.store.fetchLessonById(this.lessonId);
    this.lessonEdit = { ...this.lesson };
    this.fetchingLesson = false;
  }

  createOrUpdate(): void {
    if (this.isNewLesson)
      delete this.lessonEdit.id;
    const request = (this.isNewLesson) ?
      axios.post('http://localhost:8000/api/lesson/', this.lessonEdit) :
      axios.patch(`http://localhost:8000/api/lesson/${this.lessonEdit.id}/`, this.lessonEdit);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = (this.lessonId) ? 'Урок успешно изменён' : 'Урок успешно создан';
      if (this.isNewLesson) {
        this.store.addLessonToArray(response.data);
        router.replace(
          { name: 'lesson-edit', params: { lessonId: response.data.id.toString() } },
        );
      }
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    })
    request.finally(() => this.showNotification = true);
  }

  get getClasswork(): Array<ProblemModel | CatsProblemModel> {
    return this.search(this.lessonEdit.problems.filter(x => x.type === 'CW'));
  }

  get getHomework(): Array<ProblemModel | CatsProblemModel> {
    return this.search(this.lessonEdit.problems.filter(x => x.type === 'HW'));
  }

  search(problems: Array<ProblemModel | CatsProblemModel>): Array<ProblemModel | CatsProblemModel> {
    return searchByProblems(this.query, problems);
  }

  get isNewLesson(): boolean {
    return isNaN(this.lessonEdit.id);
  }

  get isChanged(): boolean {
    return !_.isEqual(this.lesson, this.lessonEdit);
  }

  deleteProblem(problem: ProblemModel) {
    //
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
