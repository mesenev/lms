<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить материал
    </cv-button>
    <cv-modal size="default"
              class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="!problems.length && !currentProblem.name"
              @primary-click="addProblem"
              @secondary-click="() => {}">
      <template slot="label">{{ lesson.name }}</template>
      <cv-inline-notification
        v-if="showNotification"
        @close="() => showNotification=false"
        kind="error"
        :sub-title="notificationText"
      />
      <template slot="title">
        Добавить материалы
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button content-selector=".content-1" selected>
            Создать новый
          </cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2">
            Выбрать из существующих
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template slot="content">
        <section class="modal--content">
          <div class="content-1">
            <cv-text-input label="Название урока" v-model.trim="lesson.name" disabled/>
            <cv-text-input label="Название" v-model.trim="currentProblem.name"/>
            <span>Редактирование материалов доступно после создания</span>

          </div>
          <div class="content-2" hidden>
            <div>
              <cv-structured-list>
                <template slot="items">
                  <cv-search v-model="searchQueryForAllProblems"></cv-search>
                  <cv-structured-list-item
                    class="problem-card"
                    v-for="problem in allProblems"
                    :key="problem.id">
                    <ProblemCard
                      :problem="problem"
                      :main-icon="AddAlt32"
                      :change-main-icon="SubtractAlt32"
                      :manipulation="chooseProblem">
                    </ProblemCard>
                  </cv-structured-list-item>
                </template>
              </cv-structured-list>
            </div>
          </div>
        </section>
      </template>
      <template slot="primary-button">
        Добавить
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import searchByProblems from '@/common/searchByProblems';
import LessonModel from '@/models/LessonModel';
import { lessonStore, problemStore } from '@/store';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import axios from 'axios';
import { Component, Prop, Vue } from 'vue-property-decorator';
@Component({ components: { AddAlt20, SubtractAlt20 } })
export default class EditLessonMaterialsModal extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;
  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  problemStore = problemStore;
  currentProblem: ProblemModel = { ...this.problemStore.getNewProblem,lesson: this.lesson.id };
  fetchingProblems = true;
  selectedNew = true;
  showNotification = false;
  notificationText = '';
  creationLoader = false;
  problems: ProblemModel[] = [];
  modalVisible = false;
  searchQueryForAllProblems = '';
  get allProblems(): ProblemModel[] {
    return searchByProblems(this.searchQueryForAllProblems, this.freeProblems);
  }
  get freeProblems(): ProblemModel[] {
    return this.problemStore.problems.filter((l) => {
      return !this.lesson.problems.map((lessonProblem) => lessonProblem.id).includes(l.id);
    });
  }
  async created() {
    if (this.problemStore.problems.length === 0)
      await this.problemStore.fetchLessons();
    this.fetchingProblems = false;
  }
  showModal() {
    this.modalVisible = true;
    this.showNotification = false;
    this.currentProblem = { ...this.problemStore.getNewProblem, lesson: this.lesson.id };
  }
  modalHidden() {
    this.modalVisible = false;
  }
  actionSelected() {
    this.selectedNew = !this.selectedNew;
  }
  get getSelected(): string {
    return this.problems.concat(this.currentProblem)
      .map((l) => l.name)
      .sort((a, b) => a < b ? -1 : 1)
      .join(' ');
  }
  chooseProblem(problem: ProblemModel) {
    if (!this.problems.includes(problem)) {
      this.problems.push(problem);
    } else {
      this.problems = this.problems.filter((l) => problems !== l);
    }
  }
  async addProblem() {
    if (this.selectedNew) {
      this.creationLoader = true;
      await this.createNewProblem();
      this.creationLoader = false;
    }
    if (this.problems.every((l) => l.name)) {
      // this.lessons.forEach((lesson) => this.lessonStore.addLessonToCourse(lesson));
      // this.lessons = [];
    }
  }
  async createNewProblem() {
    delete this.currentProblem.id;
    const request = axios.post('http://localhost:8000/api/problem/', this.currentProblem);
    request.then(response => {
      this.lesson.problems.push(response.data as ProblemModel);
      this.modalHidden();
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    });
  }
}
</script>

<style scoped lang="stylus">
.bx--modal-content:focus
  outline none
.change-btn
  background-color var(--cds-interactive-02)
  margin-left 25px
.lesson_list
  margin-bottom 0
.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)
.switcher
  margin-bottom: 5px
.add_lesson_modal .bx--modal-container
  height 75vh
.add_lesson_modal .bx--modal-footer
  height 3.5rem
.add_lesson_modal .bx--btn
  height 3rem
  border none
.add_lesson_modal .bx--btn--secondary
  background-color var(--cds-hover-secondary)
  &:hover, &:active, &:focus
    outline none
    box-shadow none
    border none
.add_lesson_modal .bx--btn--primary[disabled = disabled],
.add_lesson_modal .bx--btn--primary
  background-color var(--cds-ui-05)
.modal--content
  height 400px
</style>
