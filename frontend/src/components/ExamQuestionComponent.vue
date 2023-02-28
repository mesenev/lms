<template>
  <div class="question-container">
    <div class="question-header">
      <cv-text-area v-model="question.text" class="question" placeholder="Вопрос"/>
      <cv-dropdown
        v-model="question.answer_type"
        class="answer-type"
        placeholder="Тип ответа" @change="answerTypeChange">
        <cv-dropdown-item value="input">Короткий ответ</cv-dropdown-item>
        <cv-dropdown-item value="text">Параграф</cv-dropdown-item>
        <cv-dropdown-item value="radio">Radio</cv-dropdown-item>
        <cv-dropdown-item value="checkbox">Checkbox</cv-dropdown-item>
      </cv-dropdown>
    </div>
    <cv-text-input placeholder="Описание (опционально)" v-model="question.description"/>
    <div class="short-answer" v-if="inputType">
      <span>Ответ</span>
      <cv-text-input class="short-answer-input"
                     placeholder="Введите верный ответ" v-model="question.correct_answers[0]"/>
    </div>
    <div class="long-answer" v-if="textType">
      <span>Ответ</span>
      <cv-text-area class="long-answer-input"
                    placeholder="Введите верный ответ" v-model="question.correct_answers[0]"/>
    </div>
    <div class="radio-container" v-if="radioType">
      <div class="answers" id="radio" v-for="(answer, index) in question.all_answers" :key="index">
        <span>вариант ответа</span>
        <div class="answer-variant">
          <cv-text-input v-model="question.all_answers[index]"/>
          <component v-if="question.all_answers.length > 1" class="action-btn" :is="closeFilled24"
                     @click="deleteAnswer(answer)"/>
        </div>
      </div>
      <cv-link @click="addAnswer">Добавить вариант ответа</cv-link>
      <div class="answer-container">
        <span>Выберите верные варианты ответа</span>
        <cv-dropdown class="answer" v-model="question.correct_answers[0]">
          <cv-dropdown-item :value="answer" v-for="answer in question.all_answers" :key="answer">
            {{ answer }}
          </cv-dropdown-item>
        </cv-dropdown>
      </div>
    </div>
    <div class="checkbox-container radio-container" v-if="checkboxType">
      <div class="answers" id="checkbox" v-for="(answer, index) in question.all_answers" :key="index">
        <span>вариант ответа</span>
        <div class="answer-variant">
          <cv-text-input v-model="question.all_answers[index]"/>
          <component v-if="question.all_answers.length > 1" class="action-btn" :is="closeFilled24"
                     @click="deleteAnswer(answer)"/>
        </div>
      </div>
      <cv-link @click="addAnswer">Добавить вариант ответа</cv-link>
      <div class="answer-container">
        <span>Выберите верные варианты ответа</span>
        <cv-multi-select :options="checkboxAnswers" v-model="question.correct_answers"
                         :light="true"/>
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
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import trashCan24 from "@carbon/icons-vue/lib/trash-can/24"
import closeFilled24 from "@carbon/icons-vue/lib/close--filled/24"
import QuestionModel, { ANSWER_TYPE } from "@/models/QuestionModel";
import questionStore from "@/store/modules/question";

@Component({ components: { trashCan24, closeFilled24 } })
export default class ExamQuestionComponent extends Vue {
  @Prop({ required: true }) _question!: QuestionModel;
  questionStore = questionStore;
  trashCan24 = trashCan24;
  closeFilled24 = closeFilled24;
  question = { ...questionStore.newQuestion };

  async created() {
    this.question = this._question;
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

  answerTypeChange() {
    this.question.correct_answers = [''];
    this.question.all_answers = [''];
  }

  addAnswer() {
    this.question.all_answers.push('');
  }

  deleteAnswer(answer: string) {
    this.question.all_answers = this.question.all_answers.filter(x => x != answer)
  }

  deleteQuestion() {
    this.$emit('delete-question');
  }
}
</script>

<style scoped lang="stylus">
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
  max-width 40%

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
