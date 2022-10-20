<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>{{ isNewLesson ? 'Создание урока' : 'Редактирование урока' }}</h1>
    </div>
    <cv-loading v-if="fetchingLesson"/>
    <div v-else class="bx--row content">
      <div class="bx--col-lg-8 bx--col-md-4 bx--col-sm-2">
        <cv-inline-notification
          v-if="showNotification"
          @close="hideNotification"
          :kind="notificationKind"
          :sub-title="notificationText"
        />
        <cv-text-input
          class="text_field"
          label="Название урока"
          v-model.trim="lessonEdit.name"/>
        <cv-text-input
          class="text_field"
          label="Описание урока"
          v-model.trim="lessonEdit.description"/>
        <cv-date-picker
          class="deadLine text_field"
          kind="single"
          v-model="lessonEdit.deadline"
          date-label="Дедлайн"
          :cal-options=calOptions
        />
      </div>

      <div class="bx--col-lg-8 bx--col-md-4 bx--col-sm-2">
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
            <cv-structured-list-item
              v-for="homework in getHomework"
              :key="homework.id"
              class="work">
              <div><h4>{{ homework.name }}</h4></div>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
        <div class="lesson-buttons">
          <EditLessonModal @update-problem-list="updateClassworkList($event)"
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
  </div>
</template>

<script lang="ts">
import searchByProblems from '@/common/searchByTutorial'
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import EditLessonMaterialsModal from '@/components/EditLesson/EditLessonMaterialsModal.vue';
import EditLessonModal from '@/components/EditLesson/EditLessonModal.vue';
import CatsProblemModel from '@/models/CatsProblemModel';
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import router from '@/router';
import lessonStore from '@/store/modules/lesson';
import materialStore from '@/store/modules/material';
import TrashCan20 from '@carbon/icons-vue/es/trash-can/20';
import api from '@/store/services/api'
import _ from 'lodash';
import { Component, Prop } from 'vue-property-decorator';
import { Mutation } from "vuex-module-decorators";


@Component({ components: { EditLessonMaterialsModal, EditLessonModal } })
export default class LessonEditView extends NotificationMixinComponent {

  @Prop({ required: true }) lessonId!: number;
  TrashCan = TrashCan20;
  store = lessonStore;
  materialStore = materialStore;
  fetchingLesson = true;
  lesson: LessonModel = this.store.getNewLesson;
  lessonEdit: LessonModel = { ...this.lesson }
  calOptions = { dateFormat: 'Y-m-d' }
  query = '';

  async created() {
    if (this.lessonId) {
      this.lesson = this.store.currentLesson as LessonModel;
      await this.materialStore.fetchMaterialsByLessonId(this.lesson.id)
    }
    this.lessonEdit = { ...this.lesson };
    this.fetchingLesson = false;
  }

  createOrUpdate(): void {
    const request = (this.isNewLesson) ?
      api.post('/api/lesson/', this.lessonEdit) :
      api.patch(`/api/lesson/${this.lessonEdit.id}/`, this.lessonEdit);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = (this.lessonId) ? 'Урок успешно изменён' : 'Урок успешно создан';
      if (this.isNewLesson) {
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
    return this.lessonEdit.problems.filter(x => x.type === 'CW');
  }

  @Mutation
  updateClassworkList(new_problems: Array<ProblemModel | CatsProblemModel>){
    this.lessonEdit = { ...this.lesson }
    new_problems.forEach(element => {
      this.getClasswork.push(element as ProblemModel)
    })
  }

  get getHomework(): Array<ProblemModel | CatsProblemModel> {
    return this.lessonEdit.problems.filter(x => x.type === 'HW');
  }


  searchByTutorial(problems: Array<ProblemModel | CatsProblemModel>):
    Array<ProblemModel | CatsProblemModel> {
    return searchByProblems(this.query, problems);
  }

  get isNewLesson(): boolean {
    return isNaN(this.lessonEdit.id);
  }

  get isChanged(): boolean {
    return !_.isEqual(this.lesson, this.lessonEdit);
  }

  deleteProblem(problem: ProblemModel) {
    return problem;
    //
  }
}
</script>

<style scoped lang="stylus">
.text_field
  min-width 10rem
  max-width 18rem
  padding-top 2rem

.content
  display flex

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
