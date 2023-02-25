<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить задание
    </cv-button>
    <cv-modal
      :primary-button-disabled="addButtonDisabled"
      :visible="modalVisible"
      class="add_lesson_modal" :size="selectedNew ? 'large' : 'default'"
      @modal-hidden="modalHidden"
      @primary-click="primaryHandler">
      <template slot="label">{{ lesson.name }}</template>
      <cv-inline-notification
        v-if="showNotification"
        @close="() => showNotification=false"
        kind="error"
        :sub-title="notificationText"/>
      <template slot="title">
        Добавить задание
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button owner-id="Problems" selected>
            Импортировать задачу из cats
          </cv-content-switcher-button>
          <cv-content-switcher-button owner-id="Tests">
            Создать тест
          </cv-content-switcher-button>
        </cv-content-switcher>
        <cv-content-switcher-content owner-id="Problems">
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
                <cv-inline-notification
                  v-if="showNotification"
                  @close="() => showNotification=false"
                  kind="error"
                  :sub-title="notificationText"/>
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
          <cv-content-switcher-content owner-id="Tests">
            <div :class="expanded ? 'expand-container expanded' : 'expand-container'">
              <div @click="expand" class="expand-container-head">
                <p>Настройки теста</p>
                <component class="expand-btn" :is="expanded ? chevronUp : chevronDown"/>
              </div>
              <div class="expand-fields">
                <cv-text-input v-model="test.name" label="Название теста"/>
                <cv-text-area v-model="test.description" label="Описание"/>
                <cv-dropdown v-model="test.test_mode" class="testing-type-dropdown"
                             label="Способ тестирования"
                             placeholder="Выберите способ тестирования">
                  <cv-dropdown-item value="auto">Auto</cv-dropdown-item>
                  <cv-dropdown-item value="manual">Manual</cv-dropdown-item>
                  <cv-dropdown-item value="auto_and_manual">Auto & Manual</cv-dropdown-item>
                </cv-dropdown>
                <cv-date-picker kind="single" date-label="Дедлайн"/>
              </div>
            </div>
            <div class="questions" v-for="question in test.questions" :key="question.id">
              <test-question-component :_question="question" :test-id="test.id"
                                       @delete-question="deleteQuestion(question.id)"/>
            </div>
            <div class="action-container">
              <div class="action-btns">
                <component class="action-btn" :is="addAlt" @click="addQuestion"/>
                <component class="action-btn" :is="image"/>
                <component class="action-btn" :is="videoAdd"/>
                <component class="action-btn" :is="attachment"/>
              </div>
            </div>
          </cv-content-switcher-content>
        </section>
      </template>
      <template slot="primary-button">{{ selectedNew ? 'Создать тест' : 'Добавить задачу' }}
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
import testStore from '@/store/modules/test';
import questionStore from '@/store/modules/question';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import { Component, Prop } from 'vue-property-decorator';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import api from '@/store/services/api';
import TestQuestionComponent from "@/components/TestQuestionComponent.vue";
import chevronUp from "@carbon/icons-vue/lib/chevron--up/24";
import chevronDown from "@carbon/icons-vue/lib/chevron--down/24";
import addAlt from "@carbon/icons-vue/lib/add--alt/24";
import videoAdd from "@carbon/icons-vue/lib/video--add/24";
import image from "@carbon/icons-vue/lib/image/24";
import attachment from "@carbon/icons-vue/lib/attachment/24";
import TestModel from "@/models/TestModel";
import _ from 'lodash';


@Component({
  components: {
    AddAlt20,
    SubtractAlt20,
    TestQuestionComponent,
    chevronUp,
    chevronDown,
    addAlt,
    videoAdd,
    image,
    attachment,
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

  chevronUp = chevronUp;
  chevronDown = chevronDown;
  image = image;
  addAlt = addAlt;
  videoAdd = videoAdd;
  attachment = attachment;

  testStore = testStore;
  questionStore = questionStore;
  test: TestModel = { ...testStore.newTest };
  questionCount = 0;
  expanded = false;


  get catsFilteredProblems() {
    return searchByProblems(this.searchQueryForAllProblems, this.catsProblemsTruncated);
  }

  async created() {
    if (!this.lesson.course) return
    this.test = _.cloneDeep(this.test);
    this.addQuestion();
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

  actionSelected() {
    this.selectedNew = !this.selectedNew;
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
    if (this.selectedNew)
      await this.createTest();
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

  expand() {
    this.expanded = !this.expanded;
  }

  addQuestion() {
    this.questionCount++;
    const newQuestion = _.cloneDeep(this.questionStore.newQuestion);
    newQuestion.id = this.questionCount;
    this.test.questions.push(newQuestion);
  }

  deleteQuestion(id: number) {
    if (this.test.questions.length > 1) {
      this.test.questions = this.test.questions.filter(x => x.id !== id);
    }
  }

  async createTest() {
    let tests = this.testStore.tests[this.lesson.id];
    tests ? this.test.id = tests.length : this.test.id = 0;
    tests ? tests.push(this.test) : tests = [this.test];
    await this.testStore.setTests({ [this.lesson.id]: tests });
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

//.modal--content
//  height 400px

.problem-type-selection
  margin-top 2rem

.expand-container-head
  cursor pointer
  display flex
  align-items center
  justify-content space-between
  margin-bottom 1rem

.expand-container
  max-height 3.25rem
  overflow hidden
  transition all .3s ease
  background var(--cds-ui-01)
  padding 1rem

.expand-container.expanded
  max-height 500px

.testing-type-dropdown
  width 40%

.testing-type-dropdown /deep/ .bx--list-box__menu
  max-height 5rem

/deep/ .bx--list-box__field
  display flex

.action-container
  display flex
  justify-content end

.expand-fields
  display flex
  flex-direction column
  gap 1rem

.action-btns
  background var(--cds-ui-01)
  display flex
  gap 1rem
  border-radius 5px
  margin-top 1rem
  padding 1rem

.action-btn
  cursor pointer
  transition ease-in-out 0.1s

.action-btn:active
  transform scale(0.9)

</style>
