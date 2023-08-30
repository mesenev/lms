<template>
  <div class="question-container" :style="loading ? 'text-align: -webkit-center' : ''">
    <div v-if="!loading">
      <div class="question-header">
        <cv-text-area v-model.trim="question.text" class="question" placeholder="Вопрос">
          <template slot="invalid-message" v-if="!question.text.length && invalidProp">
            {{ emptyInputInvalidText }}
          </template>
        </cv-text-area>
        <cv-dropdown
          v-model="question.answer_type"
          class="answer-type"
          placeholder="Тип ответа" @change="answerTypeChange">
          <cv-dropdown-item value="input">Короткий ответ</cv-dropdown-item>
          <cv-dropdown-item v-if="!autoTestMode" value="text">Параграф</cv-dropdown-item>
          <cv-dropdown-item value="radio">Radio</cv-dropdown-item>
          <cv-dropdown-item value="checkbox">Checkbox</cv-dropdown-item>
        </cv-dropdown>
      </div>
      <cv-text-area placeholder="Описание (опционально)" v-model.trim="question.description"/>
      <div class="short-answer" v-if="inputType">
        <span v-if="autoTestMode">Ответ</span>
        <cv-text-input class="short-answer-input" v-if="autoTestMode"
                       placeholder="Введите верный ответ"
                       v-model.trim="question.correct_answers[0]">
          <template slot="invalid-message" v-if="!correctAnswersLength && invalidProp">
            {{ emptyInputInvalidText }}
          </template>
        </cv-text-input>
        <p class="invalid-text" v-else> {{ manualHelpText }} </p>
      </div>
      <div class="long-answer" v-if="textType">
        <p class="invalid-text"> {{ paragraphHelpText }} </p>
      </div>
      <div class="radio-container" v-if="radioType">
        <div class="answers" id="radio" v-for="(answer, index) in question.all_answers"
             :key="index">
          <span>вариант ответа</span>
          <div class="answer-variant">
            <cv-text-input v-model="question.all_answers[index]">
              <template slot="invalid-message"
                        v-if="!question.all_answers[index].trim().length && invalidProp">
                {{ emptyInputInvalidText }}
              </template>
            </cv-text-input>
            <component v-if="question.all_answers.length > 1" class="action-btn" :is="closeFilled24"
                       @click="deleteAnswer(answer)"/>
          </div>
        </div>
        <cv-link @click="addAnswer">Добавить вариант ответа</cv-link>
        <div class="answer-container">
          <span v-if="!manualTestMode">Выберите верный вариант ответа</span>
          <cv-dropdown @focusout="checkEmptyFields" v-if="!manualTestMode" class="answer"
                       v-model="question.correct_answers[0]">
            <cv-dropdown-item :value="answer" v-for="answer in question.all_answers" :key="answer">
              {{ answer }}
            </cv-dropdown-item>
            <template slot="invalid-message" v-if="!correctAnswersLength && invalidProp">
              {{ emptyDropDownInvalidText }}
            </template>
          </cv-dropdown>
          <p class="invalid-text" v-else> {{ manualHelpText }} </p>
        </div>
      </div>
      <div class="checkbox-container radio-container" v-if="checkboxType">
        <div class="answers" v-for="(answer, index) in question.all_answers" :key="index">
          <span>вариант ответа</span>
          <div class="answer-variant">
            <cv-text-input v-model="question.all_answers[index]">
              <template slot="invalid-message"
                        v-if="!question.all_answers[index].trim().length && invalidProp">
                {{ emptyInputInvalidText }}
              </template>
            </cv-text-input>
            <component v-if="question.all_answers.length > 1" class="action-btn" :is="closeFilled24"
                       @click="deleteAnswer(answer)"/>
          </div>
        </div>
        <cv-link @click="addAnswer">Добавить вариант ответа</cv-link>
        <div class="answer-container">
          <span v-if="!manualTestMode">Выберите верные варианты ответа</span>
          <cv-multi-select v-if="!manualTestMode"
                           :options="checkboxAnswers"
                           v-model="question.correct_answers"
                           :light="true">
            <template slot="invalid-message" v-if="!correctAnswersLength && invalidProp">
              {{ emptyDropDownInvalidText }}
            </template>
          </cv-multi-select>
          <p class="invalid-text" v-else> {{ manualHelpText }} </p>
        </div>
      </div>
      <span>Сумма баллов</span>
      <div class="question-footer">
        <cv-number-input class="points-input" v-model="question.points" :min="0"/>
        <div class="action-btns">
          <component class="action-btn" :is="trashCan24" @click="deleteQuestion"/>
        </div>
      </div>
    </div>
    <cv-loading v-else></cv-loading>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import trashCan24 from "@carbon/icons-vue/lib/trash-can/24"
import closeFilled24 from "@carbon/icons-vue/lib/close--filled/24"
import QuestionModel, { ANSWER_TYPE } from "@/models/QuestionModel";
import questionStore from "@/store/modules/question";
import ExamModel from "@/models/ExamModel";

@Component({ components: { trashCan24, closeFilled24 } })
export default class ExamQuestionComponent extends Vue {
  @Prop({ required: true }) _question!: QuestionModel;
  @Prop({ required: true }) exam!: ExamModel;
  @Prop({required: true}) invalidProp!: boolean;
  questionStore = questionStore;
  trashCan24 = trashCan24;
  closeFilled24 = closeFilled24;
  loading = false;
  question = { ...this.questionStore.newQuestion };

  manualHelpText = '';
  paragraphHelpText = '';
  emptyInputInvalidText = '';
  emptyDropDownInvalidText = '';

  async created() {
    this.loading = true;
    this.emptyInputInvalidText = 'Заполните поле!';
    this.emptyDropDownInvalidText = 'Выберите вариант ответа!';
    this.manualHelpText = 'В текущем режиме проверки ответ проверяется вручную';
    this.paragraphHelpText = 'Данный тип ответа проверяется вручную';
    this.question = this._question;
    this.loading = false;
  }

  async updated() {
    this.checkEmptyFields();
  }

  get inputType() {
    return this.question.answer_type === ANSWER_TYPE.INPUT;
  }

  get textType() {
    return this.question.answer_type === ANSWER_TYPE.TEXT_FIELD;
  }

  get radioType() {
    return this.question.answer_type === ANSWER_TYPE.RADIO;
  }

  get checkboxType() {
    return this.question.answer_type === ANSWER_TYPE.CHECKBOXES;
  }

  get autoTestMode() {
    return this.exam.test_mode === 'auto';
  }

  get manualTestMode() {
    return this.exam.test_mode === 'manual';
  }

  get correctAnswersLength() {
    return this.question.correct_answers.length && (this.question.correct_answers[0] ?? '').trim().length;
  }

  get checkboxAnswers() {
    return this.question.all_answers.map(item => {
      const nameVal = item.toLowerCase();
      return {
        name: nameVal,
        label: item,
        value: nameVal,
        disabled: false,
      }
    })
  }

  inputHandler(answer: string, index: number) {
    this.question.all_answers[index] = answer.trim();
  }

  @Watch('exam.test_mode')
  onTestModeChange() {
    if (this.autoTestMode && this.textType) {
      this.answerTypeChange();
      this.question.answer_type = 'input';
    }
    if (this.manualTestMode)
      this.question.correct_answers = [];
  }

  checkEmptyFields() {
    let isAllAnswersInvalid = false;
    let isCorrectAnswersInvalid = false;
    if (!this.textType && !this.inputType) {
      if (this.question.all_answers.length) {
        this.question.all_answers.forEach(value => {
          if (!value.trim().length)
            isAllAnswersInvalid = true;
        })
      } else
        isAllAnswersInvalid = true;
      if (!this.manualTestMode) {
        if (this.question.correct_answers.length)
          this.question.correct_answers.forEach(value => {
            if (!value.trim().length)
              isCorrectAnswersInvalid = true;
          })
        else
          isCorrectAnswersInvalid = true;
      }
    } else if (this.inputType) {
      if (this.autoTestMode) {
        if (this.question.correct_answers.length) {
          this.question.correct_answers.forEach(value => {
            if (!value.trim().length)
              isCorrectAnswersInvalid = true;
          })
        } else
          isCorrectAnswersInvalid = true;
      }
    }
    this.$emit('set-fields-empty',{
      isEmpty: !this.question.text.length
              || isAllAnswersInvalid
              || isCorrectAnswersInvalid,
      question: this.question.index,
    });
  }

  answerTypeChange() {
    this.question.correct_answers = [];
    this.question.all_answers = [''];
  }

  addAnswer() {
    this.question.all_answers.push('');
  }

  deleteAnswer(answer: string) {
    this.question.all_answers = this.question.all_answers.filter(x => x != answer);
    this.question.correct_answers = this.question.correct_answers.filter(x => x != answer);
  }

  deleteQuestion() {
    this.$emit('delete-question');
  }
}
</script>

<style scoped lang="stylus">
.invalid-text
  font-style italic

.question-container
  line-height var(--cds-body-long-01-line-height, 1.43);
  background var(--cds-ui-01)
  padding 1rem
  border-radius 5px
  margin-top 1rem

.question-header
  display flex
  flex-direction row
  justify-content space-between
  margin-bottom 1rem

.question
  width 50%

/deep/ .bx--label
  display none

.answer-type /deep/ .bx--dropdown__wrapper.bx--list-box__wrapper
  max-width 50%

/deep/ .bx--list-box__field
  display flex

.answer-type
  width 40%
  align-items end

.short-answer
  width 50%
  margin-top 1rem
  margin-bottom 1rem

.long-answer
  margin-top 1rem
  margin-bottom 1rem

.answer-variant
  display flex
  align-items center
  gap 1rem

.radio-container
  margin-top 1rem
  display flex
  flex-direction column
  gap 0.5rem
  width 50%

.answer-container
  margin-top 1rem
  margin-bottom 1rem

.points-input /deep/ .bx--number
  width 11rem

.question-footer
  display flex

.action-btns
  background var(--cds-ui-02)
  display flex
  gap 1rem
  border-radius 5px
  padding 1rem

.action-btn
  cursor pointer
  transition ease-in-out 0.1s

.action-btn:active
  transform scale(0.9)
</style>
