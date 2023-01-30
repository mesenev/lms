<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>{{ isNewLesson ? 'Создание урока' : 'Редактирование урока' }}</h1>
    </div>
    <cv-loading v-if="fetchingLesson"/>
    <div v-else class="bx--row content">
      <div class="bx--col-lg-5 bx--col-md-5">
        <div class="edit-content">
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
          <div class="finishButton">
            <cv-button :disabled="!isChanged" v-on:click="createOrUpdate">
              {{ isNewLesson ? 'Создать урок' : 'Изменить урок' }}
            </cv-button>
          </div>
        </div>
        <div class="lesson-buttons">
          <EditLessonModal @update-problem-list="updateTaskList($event)"
                           :lesson="lessonEdit"
                           class="edit--lesson-props"/>
          <EditLessonMaterialsModal @update-material-delete="updateMaterialDelete($event)"
                                    :lesson="lessonEdit"
                                    class="edit--lesson-props"/>
        </div>
      </div>

      <div class="bx--col-lg-5 bx--col-md-4">
        <cv-content-switcher size="small">
          <cv-content-switcher-button class="type-of-task-tab" owner-id="CW" selected>
            Классная работа
          </cv-content-switcher-button>
          <cv-content-switcher-button class="type-of-task-tab" owner-id="HW">
            Домашняя работа
          </cv-content-switcher-button>
          <cv-content-switcher-button class="type-of-task-tab" owner-id="EX">
            Доп. задания
          </cv-content-switcher-button>
        </cv-content-switcher>
        <section class="content-task-list">
          <cv-content-switcher-content owner-id="CW">
            <div v-if="getClasswork.length > 0">
              <div v-if="!fetchingLesson" class="classwork">
                <problem-list-component
                  :is-editing="true"
                  @update-problem-delete="updateProblemDelete($event)"
                  :task-list="getClasswork">
                </problem-list-component>
              </div>
              <div v-else>
                <cv-accordion-skeleton/>
              </div>
            </div>
            <h4 v-else class="empty-tasks">Задания отсутствуют</h4>
          </cv-content-switcher-content>
          <cv-content-switcher-content owner-id="HW">
            <div v-if="getHomework.length > 0">
              <div v-if="!fetchingLesson" class="homework">
                <problem-list-component
                  :is-editing="true"
                  @update-problem-delete="updateProblemDelete($event)"
                  :task-list="getHomework">
                </problem-list-component>
              </div>
              <div v-else>
                <cv-accordion-skeleton/>
              </div>
            </div>
            <h4 v-else class="empty-tasks">Задания отсутствуют</h4>
          </cv-content-switcher-content>
          <cv-content-switcher-content owner-id="EX">
            <div v-if="getExtrawork.length > 0">
              <div v-if="!fetchingLesson" class="extrawork">
                <problem-list-component
                  :is-editing="true"
                  @update-problem-delete="updateProblemDelete($event)"
                  :task-list="getExtrawork">
                </problem-list-component>
              </div>
              <div v-else>
                <cv-accordion-skeleton/>
              </div>
            </div>
            <h4 v-else class="empty-tasks">Задания отсутствуют</h4>
          </cv-content-switcher-content>
        </section>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import searchByProblems from '@/common/searchByTutorial'
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import EditLessonMaterialsModal from '@/components/EditLesson/EditLessonMaterialsModal.vue';
import EditLessonModal from '@/components/EditLesson/EditLessonModal.vue';
import ProblemListComponent from "@/components/lists/ProblemListComponent.vue";
import CatsProblemModel from '@/models/CatsProblemModel';
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import router from '@/router';
import lessonStore from '@/store/modules/lesson';
import materialStore from '@/store/modules/material';
import problemStore from '@/store/modules/problem';
import api from '@/store/services/api';
import _ from 'lodash';
import {Component, Prop} from 'vue-property-decorator';


@Component({components: {EditLessonMaterialsModal, EditLessonModal, ProblemListComponent}})
export default class LessonEditView extends NotificationMixinComponent {

  @Prop({required: true}) lessonId!: number;
  store = lessonStore;
  materialStore = materialStore;
  problemStore = problemStore;
  fetchingLesson = true;
  lesson: LessonModel = this.store.getNewLesson;
  lessonEdit: LessonModel = {...this.lesson};
  calOptions = {dateFormat: 'Y-m-d'};
  query = '';

  async created() {
    if (this.lessonId) {
      this.lesson = this.store.currentLesson as LessonModel;
      await this.materialStore.fetchMaterialsByLessonId(this.lesson.id)
    }
    this.lessonEdit = {...this.lesson};
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
          {name: 'lesson-edit', params: {lessonId: response.data.id.toString()}},
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

  updateTaskList(new_problems: Array<ProblemModel | CatsProblemModel>) {
    this.lessonEdit = {...this.lesson}
    new_problems.forEach(element => {
      this.lessonEdit.problems.push(element as ProblemModel)
    })
    this.problemStore.setProblems({[this.lessonId]: this.lessonEdit.problems});
  }

  updateProblemDelete(deleted_problem_id: number) {
    this.lessonEdit.problems = this.lessonEdit.problems
      .filter(x => x.id != deleted_problem_id);
    this.lesson.problems = this.lessonEdit.problems;
    this.problemStore.setProblems({[this.lessonId]: this.lessonEdit.problems});
  }

  updateMaterialDelete() {
    this.lesson.materials = this.lessonEdit.materials;
  }

  get getHomework(): Array<ProblemModel | CatsProblemModel> {
    return this.lessonEdit.problems.filter(x => x.type === 'HW');
  }

  get getExtrawork(): Array<ProblemModel | CatsProblemModel> {
    return this.lessonEdit.problems.filter(x => x.type === 'EX');
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
}
</script>

<style scoped lang="stylus">
.text_field
  margin 2rem
  max-width 23rem

/deep/.bx--text-input
  background-color var(--cds-ui-background)

.cv-date-picker >>> .bx--date-picker__input
  background-color var(--cds-ui-background)
  width auto

.bx--col
  margin: 2rem

.lesson-buttons
  display flex
  flex-direction row
  justify-content space-between
  max-width 27rem

.works-col
  margin-right 0
  margin-bottom 1rem
  margin-left 1rem
  margin-top 1rem
  display flex

.work div
  padding 1rem 1rem 0.5rem 1rem

.classwork, .homework, .extrawork
  max-height 300px
  overflow-y auto
  border var(--cds-ui-05) 1px solid
  margin: 20px 0

.edit-content
  padding-top 1px
  padding-right 20px
  padding-bottom 20px
  background-color var(--cds-ui-01)
  max-width 27rem

.empty-tasks
  color var(--cds-text-01)
  margin-top 1rem
  text-align center

.lesson-buttons
  margin-top 25px
  margin-bottom 25px

.finishButton
  display flex
  flex-direction row
  justify-content flex-end

.search
  margin 10px 0

.addButton
  background-color var(--cds-interactive-02)
  margin-left 25px

.main-content
  border 2px black solid;
  margin: 50px

.change__btn
  margin-top: 10px
  background-color: var(--cds-ui-05)

  &:hover
    background-color: var(--cds-ui-04)

.accordion /deep/ .bx--accordion__content
  padding-right 0

.type-of-task-tab
  background-color: var(--cds-active-secondary)
  color: white

.header
  color var(--cds-text-01)
  display flex
  flex-direction row
  align-items baseline
</style>
