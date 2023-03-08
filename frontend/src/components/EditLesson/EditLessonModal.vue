<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить задание
    </cv-button>
    <cv-modal
      :primary-button-disabled="addButtonDisabled"
      :visible="modalVisible"
      class="add_lesson_modal" size="default"
      @modal-hidden="modalHidden"
      @primary-click="primaryHandler">
      <template slot="label">{{ lesson.name }}</template>
      <template slot="title">
        Добавить задание
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button owner-id="Problems"
                                      selected>
            Импортировать задачу из cats
          </cv-content-switcher-button>
          <cv-content-switcher-button owner-id="Exams">
            Создать тест
          </cv-content-switcher-button>
        </cv-content-switcher>
        <cv-content-switcher-content owner-id="Problems">
          <cv-inline-notification
            v-if="showNotification"
            @close="() => showNotification=false"
            :kind="notificationKind"
            :sub-title="notificationText"/>
          <span style="padding-top: 20px">Выберите способ тестирования</span>
          <cv-radio-group style="margin-top: 10px; padding-bottom: 20px">

            <cv-radio-button label="автоматическое"
                             value="auto"
                             v-model="testingMode"
            />
            <cv-radio-button label="ручное"
                             value="manual"
                             v-model="testingMode"
            />
            <cv-radio-button label="автоматическое и ручное"
                             value="auto_and_manual"
                             v-model="testingMode"
            />
          </cv-radio-group>
        </cv-content-switcher-content>
      </template>
      <template slot="content">
        <section class="modal--content">
          <cv-content-switcher-content owner-id="Problems">
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
            </div>
            <div class="problem-type-selection">
              <h5>Тип задачи</h5>
              <cv-radio-group
                @change="(newType) => this.problemType = newType"
                :vertical="false">
                <cv-radio-button
                  v-model="problemType"
                  label="Классная работа"
                  name="group-1" value="CW"/>
                <cv-radio-button
                  v-model="problemType"
                  label="Домашняя работа"
                  name="group-1" value="HW"/>
                <cv-radio-button
                  v-model="problemType"
                  label="Дополнительные задания"
                  name="group-1" value="EX"/>
              </cv-radio-group>
            </div>
          </cv-content-switcher-content>
          <cv-content-switcher-content owner-id="Exams">
            <div class="exam-container">
              <div class="exam-container-head">
                <p>Настройки теста</p>
                <cv-dropdown v-model="exam.test_mode" class="testing-type-dropdown"
                             label="Способ тестирования"
                             placeholder="Тестирование">
                  <cv-dropdown-item value="auto">Auto</cv-dropdown-item>
                  <cv-dropdown-item value="manual">Manual</cv-dropdown-item>
                  <cv-dropdown-item value="auto_and_manual">Auto & Manual</cv-dropdown-item>
                </cv-dropdown>
              </div>
              <div class="exam-fields">
                <cv-text-input v-model="exam.name" label="Название теста"/>
                <cv-text-area v-model="exam.description" label="Описание"/>
              </div>
            </div>
            <cv-inline-notification
              v-if="showNotification"
              @close="() => showNotification=false"
              :kind="notificationKind"
              :sub-title="notificationText"/>
          </cv-content-switcher-content>
        </section>
      </template>
      <template slot="primary-button">
        {{ isExamsSelected ? 'Создать тест и перейти к редактированию' : 'Добавить задачу' }}
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import searchByProblems from '@/common/searchByTutorial';
import CatsProblemModel from '@/models/CatsProblemModel';
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import problemStore from '@/store/modules/problem';
import examStore from '@/store/modules/exam';
import questionStore from '@/store/modules/question';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import { Component, Prop } from 'vue-property-decorator';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import api from '@/store/services/api';
import ExamQuestionComponent from "@/components/ExamQuestionComponent.vue";
import ExamModel from "@/models/ExamModel";
import _ from 'lodash';
import QuestionModel from "@/models/QuestionModel";
import router from "@/router";


@Component({
  components: {
    AddAlt20,
    SubtractAlt20,
    ExamQuestionComponent,
  }
})
export default class EditLessonModal extends NotificationMixinComponent {
  @Prop({ required: true }) lesson!: LessonModel;

  problemStore = problemStore;
  currentProblem: ProblemModel = { ...this.problemStore.getNewProblem, lesson: this.lesson.id };
  selectedNew = false;
  selected = [];
  columns = ['id', 'Название', 'Статус'];

  problems: ProblemModel[] = [];
  catsProblems: CatsProblemModel[] = [];
  catsProblemsTruncated: { id: number; name: string; status: string }[] = [];
  fetchingCatsProblems = true;
  modalVisible = false;
  searchQueryForAllProblems = '';
  testingMode = '';
  problemType = '';
  loading = false;

  contentType = 'Problems';
  examStore = examStore;
  questionStore = questionStore;
  exam: ExamModel = { ...this.examStore.newExam, lesson: this.lesson.id };
  expanded = false;


  get catsFilteredProblems() {
    return searchByProblems(this.searchQueryForAllProblems, this.catsProblemsTruncated);
  }

  async created() {
    if (!this.lesson.course) return
    this.exam = _.cloneDeep(this.exam);
    await this.fetchCatsProblems()
  }

  async fetchCatsProblems() {
    this.fetchingCatsProblems = true;
    await api.get(`/api/cats-problems/${this.lesson.course}/`)
      .then(response => {
        this.catsProblems = response.data;
      })
      .catch(error => {
        console.log(error.response);
        this.notificationKind = 'error';
        this.notificationText = `Ошибка получения списка задач: ${error.message}`;
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

  onSearch(value: string) {
    this.searchQueryForAllProblems = value;
  }

  showModal() {
    this.modalVisible = true;
    this.showNotification = false;
    this.currentProblem = { ...this.problemStore.getNewProblem, lesson: this.lesson.id };
  }

  modalHidden() {
    this.problemType = '';
    this.testingMode = '';
    this.modalVisible = false;
  }

  actionSelected(type: string) {
    this.setContentType(type);
    this.selectedNew = !this.selectedNew;
  }

  setContentType(type: string) {
    this.contentType = type;
  }

  get isExamsSelected() {
    return this.contentType === 'Exams';
  }

  get selectedIds() {
    return this.selected.map(e => {
      return (this.catsFilteredProblems[e as number] as unknown as { id: number })['id'];
    })
  }

  get addButtonDisabled() {
    // debugger;
    if (this.selectedNew)
      return false;
    else
      return (!this.selected.length || this.selectedNew) || !this.problemType
        || !this.testingMode || this.loading;
  }

  get selectedCatsProblems() {
    return this.catsProblems.filter(element => {
      return this.selectedIds.find(e => e === element.id);
    });
  }

  get areUsedTasks() {
    return this.lesson.problems.filter(element => {
      return this.selectedCatsProblems.find(e => e.id === element.cats_id)?.id
        && element.type === this.problemType;
    }).length > 0;
  }

  async primaryHandler() {
    if (this.isExamsSelected)
      await this.createExam();
    else
      await this.addProblem();
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
    if (this.testingMode === '') {
      this.notificationText = 'Выберите режим тестирования';
      this.showNotification = true;
      return
    }
    if (this.areUsedTasks) {
      this.notificationKind = 'error';
      this.notificationText = `Урок уже содержит одну из выбранных задач.`;
      this.showNotification = true;
      return;
    }
    if (!this.selectedNew) {
      this.loading = true;
      const data = this.selectedCatsProblems;
      const problemTypes = new Map<string, number>([['CW', 0], ['HW', 1], ['EX', 2]]);
      data.forEach(element => element.test_mode = this.testingMode);
      await api.post(
        `/api/lesson/${this.lesson.id}/add_cats_problems/`,
        { problem_data: data, problem_type: problemTypes.get(this.problemType) },
      )
        .then(async (answer) => {
          if (answer.status == 200) {
            const newProblems = (answer.data as ProblemModel[]).map(element => {
              element.type = this.problemType;
              return element;
            });
            this.$emit("update-problem-list", newProblems as ProblemModel[]);
            this.modalHidden();
            // await this.fetchCatsProblems();
          }
        }).catch(answer => {
          this.notificationKind = 'error';
          this.notificationText = `Произошла ошибка при добавлении задач. ${answer.message}`;
          this.showNotification = true;
        }).finally(() => {
          this.loading = false;
        })
    }
  }

  async createExam() {
    await api.post('/api/exam/', this.exam).then(response => {
      this.notificationKind = 'success';
      this.notificationText = 'Тест успешно создан';
      this.$emit('update-exam-list', response.data as ExamModel);
      router.replace(
        { name: 'exam-edit', params: { examId: response.data.id.toString() } },
      );
    }).catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    }).finally(() => {
      this.showNotification = true;
    })
  }
}
</script>

<style scoped lang="stylus">
.add_lesson_modal /deep/ .bx--modal-container
  background var(--cds-ui-background)

/deep/ .bx--modal-content:focus
  outline none

.change-btn
  background-color var(--cds-interactive-02)

  &:hover
    border var(--cds-ui-01) 1px solid

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

.problem-type-selection
  margin-top 2rem

.testing-type-dropdown
  /deep/ .bx--dropdown__wrapper.bx--list-box__wrapper
    max-width 50%
    align-self end


/deep/ .bx--list-box__field
  display flex

.action-container
  display flex
  justify-content end

.exam-container
  background-color var(--cds-ui-01)
  padding 1rem

.exam-container-head
  display flex
  justify-content space-between

.exam-fields
  display flex
  flex-direction column
  gap 1rem
</style>
