<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <div class="bx--offset-lg-2 main-title">
        <h1>Редактирование теста</h1>
      </div>
    </div>
    <cv-row class="main-items" justify="center">
      <cv-column :lg="{'span' : 8, 'offset' : 2}">
        <div class="test-container">
          <div :class="expanded ? 'expand-container expanded' : 'expand-container'">
            <div @click="expand" class="expand-container-head">
              <p>Настройки теста</p>
              <component class="expand-btn" :is="expanded ? chevronUp : chevronDown"/>
            </div>
            <div class="expand-fields">
              <cv-text-input v-model="testEdit.name" label="Название теста"/>
              <cv-text-area v-model="testEdit.description" label="Описание"/>
              <cv-dropdown v-model="testEdit.test_mode" class="testing-type-dropdown"
                           label="Способ тестирования"
                           placeholder="Выберите способ тестирования">
                <cv-dropdown-item value="auto">Auto</cv-dropdown-item>
                <cv-dropdown-item value="manual">Manual</cv-dropdown-item>
                <cv-dropdown-item value="auto_and_manual">Auto & Manual</cv-dropdown-item>
              </cv-dropdown>
              <cv-date-picker kind="single" date-label="Дедлайн"/>
            </div>
          </div>
          <div class="questions" v-for="question in testEdit.questions" :key="question.id">
            <test-question-component :_question="question" :test-id="testEdit.id"
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
        </div>
        <div class="change-container">
          <div class="change">
            <cv-button @click="changeTest" :disabled="!isChanged">Изменить</cv-button>
          </div>
        </div>
      </cv-column>
    </cv-row>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import TestQuestionComponent from "@/components/TestQuestionComponent.vue";
import TestModel from "@/models/TestModel";
import testStore from "@/store/modules/test";
import questionStore from "@/store/modules/question";
import chevronUp from "@carbon/icons-vue/lib/chevron--up/24";
import chevronDown from "@carbon/icons-vue/lib/chevron--down/24";
import addAlt from "@carbon/icons-vue/lib/add--alt/24";
import videoAdd from "@carbon/icons-vue/lib/video--add/24";
import image from "@carbon/icons-vue/lib/image/24";
import attachment from "@carbon/icons-vue/lib/attachment/24";
import _ from "lodash";

@Component({
  components: {
    TestQuestionComponent,
    chevronUp,
    chevronDown,
    addAlt,
    videoAdd,
    image,
    attachment,
  }
})
export default class TestEditView extends NotificationMixinComponent {
  @Prop({ required: true }) testId!: number;

  testStore = testStore;
  questionStore = questionStore;
  chevronUp = chevronUp;
  chevronDown = chevronDown;
  image = image;
  addAlt = addAlt;
  videoAdd = videoAdd;
  attachment = attachment;
  expanded = false;

  _test: TestModel = { ...testStore.newTest };
  testEdit = { ...this._test };

  async created() {
    this._test = await this.testStore.fetchTestById(this.testId);
    this.testEdit = _.cloneDeep(this._test);
  }

  get isChanged() {
    return !_.isEqual(this._test, this.testEdit);
  }

  expand() {
    this.expanded = !this.expanded;
  }

  addQuestion() {
    const newQuestion = _.cloneDeep(this.questionStore.newQuestion);
    newQuestion.id = this.testEdit.questions.length;
    this.testEdit.questions.push(newQuestion);
  }

  deleteQuestion(id: number) {
    if (this.testEdit.questions.length > 1) {
      this.testEdit.questions = this.testEdit.questions.filter(x => x.id !== id);
    }
  }

  changeTest() {
    return true;
  }
}
</script>

<style scoped lang="stylus">
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

span
  margin-bottom 0.25rem

/deep/ .bx
  &--text
    &-input
      background-color var(--cds-ui-background)

    &-area
      background-color var(--cds-ui-background)

  &--list
    &-box
      background-color var(--cds-ui-background)

      &__field
        display flex

  &--number
    input[type=number]
      background-color var(--cds-ui-background)

/deep/ .bx--date-picker__input
  background-color var(--cds-ui-background)
  width auto

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

.change-container
  display flex
  gap 1rem
  flex-direction row
  width 60%

.change
  background-color var(--cds-ui-01)
  border-radius 5px
  padding 1rem
  width fit-content
  margin-top 0.5rem
</style>
