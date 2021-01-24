<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить задание
    </cv-button>
    <cv-modal
      :primary-button-disabled="!selected.length || selectedNew" :visible="modalVisible"
      class="add_lesson_modal" size="default"
      @modal-hidden="modalHidden"
      @primary-click="addProblem">
      <template slot="label">{{ lesson.name }}</template>
      <cv-inline-notification
        v-if="showNotification"
        @close="() => showNotification=false"
        kind="error"
        :sub-title="notificationText"/>
      <template slot="title">
        Добавить задание
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button content-selector=".content-1" selected>
            Импортировать задачу из cats
          </cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2">
            Создать новую задачу
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template slot="content">
        <section class="modal--content">
          <div class="content-1">
            <div>
              <cv-data-table
                v-if="!fetchingCatsProblems" ref="table"
                v-model="selected" :columns="columns" :data="catsFilteredProblems"
                class="cats-problems-table" @search="onSearch">
                <template slot="batch-actions">
                  <div></div>
                </template>
              </cv-data-table>
              <cv-data-table-skeleton v-else/>
            </div>
          </div>
          <div class="content-2" hidden>
            <cv-text-input v-model.trim="lesson.name" disabled label="Название урока"/>
            <cv-text-input v-model.trim="currentProblem.name" label="Название задания"/>
            <cv-text-input v-model.trim="currentProblem.description" label="Описание задания"/>
            <h5>Тип задачи</h5>
            <cv-radio-group
              :vertical="vertical">
              <cv-radio-button
                v-model="currentProblem.type"
                label="Классная работа"
                name="group-1" value="CW"/>
              <cv-radio-button
                v-model="currentProblem.type"
                label="Домашнаяя работа"
                name="group-1" value="HW"/>
            </cv-radio-group>
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
import CatsProblemModel from '@/models/CatsProblemModel';
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import { problemStore } from '@/store';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import axios from 'axios';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { AddAlt20, SubtractAlt20 } })
export default class EditLessonModal extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;

  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  vertical = false;
  problemStore = problemStore;
  currentProblem: ProblemModel = { ...this.problemStore.getNewProblem, lesson: this.lesson.id };
  fetchingProblems = true;
  selectedNew = false;
  showNotification = false;
  notificationKind = 'success';
  notificationText = '';
  creationLoader = false;
  selected = [];

  columns = ['id', 'Название', 'Статус'];

  problems: ProblemModel[] = [];
  catsProblems: CatsProblemModel[] = [];
  catsProblemsTruncated: { id: number; name: string; status: string }[] = [];
  fetchingCatsProblems = true;
  modalVisible = false;
  searchQueryForAllProblems = '';

  get catsFilteredProblems() {
    return searchByProblems(this.searchQueryForAllProblems, this.catsProblemsTruncated);
  }

  async created() {
    if (!this.lesson.course) return
    await this.fetchCatsProblems()
  }

  async fetchCatsProblems() {
    this.fetchingCatsProblems = true;
    await axios.get(`/api/cats-problems/${this.lesson.course}/`)
      .then(response => { this.catsProblems = response.data; })
      .catch(error => {
        console.log(error.response);
        this.notificationKind = 'error';
        this.notificationText = `Ошибка получения списка задач: ${error.response}`;
        this.showNotification = true;
      })
    this.catsProblems.map(value => {
      this.catsProblemsTruncated.push(
        { id: value.id, name: value.name, status: value.status },
      )
    });
    this.catsProblemsTruncated = [...this.catsProblemsTruncated];
    this.fetchingCatsProblems = false;
  }

  get freeProblems(): ProblemModel[] {
    return this.problemStore.problems.filter((l) => {
      return !this.lesson.problems.map((lessonProblem) => lessonProblem.id).includes(l.id);
    });
  }

  onSearch(value: string) {
    this.searchQueryForAllProblems = value;
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

  async addProblem() {
    if (!this.lesson.id) {
      this.notificationKind = 'error';
      this.notificationText = 'id урока не указано!';
      this.showNotification = true;
      throw new Error('add cats problems  -- course id not found!');
    }
    if (this.selectedNew)
      return
    if (!this.selectedNew) {
      const selected_ids = this.selected.map(e => {
        return (this.catsFilteredProblems[e as number] as unknown as { id: number })['id'];
      })
      const data = this.catsProblems.filter(element => {
        return selected_ids.find(e => e === element.id);
      });
      await axios.post(`/api/add-cats-problems-to-lesson/${this.lesson.id}/`, data)
        .then(async (answer) => {
          if (answer.status == 200) {
            this.modalHidden();
            // await this.fetchCatsProblems();
          }
        }).catch(answer => {
          this.notificationKind = 'error';
          this.notificationText = `Произошла ошибка при добавлении задач. ${answer.message}`;
          this.showNotification = true;
        })

    }
  }
}
</script>

<style scoped lang="stylus">
.bx--modal-content:focus
  outline none

.change-btn
  background-color var(--cds-interactive-02)

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
