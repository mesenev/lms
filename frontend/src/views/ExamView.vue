<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div class="bx--offset-lg-2 main-title">
        <h1 v-if="exam && !loading"> {{ exam.name }} </h1>
        <cv-skeleton-text v-else :heading="true" :width="'35%'" class="main-title"/>
        <div class="info-container">
          <div class="test-info">
            <span>Тест</span>
            <span>
              Макс. балл <strong> {{ exam.points }} </strong>
            </span>
            <span>
              Режим тестирования: <strong> {{ exam.test_mode }} </strong>
            </span>
            <div v-if="isStaff" class="visibility">
              <cv-button-skeleton v-if="changingVisibility || !this.exam" kind="ghost"/>
              <cv-button v-else
                         class="test-hide-button"
                         :icon="hiddenIcon"
                         kind="ghost"
                         @click="changeExamVisibility">
                {{ (exam.is_hidden) ? "Открыть тест" : "Скрыть тест" }}
              </cv-button>
            </div>
          </div>
          <div class="description-container">
            <span v-if="!loading && exam" class="lesson-description">
               {{ exam.description }}
            </span>
            <cv-skeleton-text v-else width="'35%'"/>
          </div>
        </div>
      </div>
    </div>
    <cv-row class="main-items" justify="center">
      <cv-column :lg="{'span' : 8, 'offset' : 2}">
        <div v-if="!loading" class="test-container">
          <div class="question-container" v-for="(question, index) in exam.questions" :key="index">
            <h4 class="question-title"> {{ question.text }} </h4>
            <p class="question-description">{{ question.description }}</p>
            <cv-radio-group class="answers" :vertical="true" v-if="isQuestionRadioType(question)">
              <cv-radio-button v-model="userAnswers[question.index].submitted_answers[0]"
                               v-for="(answer, id) in question.all_answers" :key="id" :name="index"
                               :label="answer" :value="answer"
                               :disabled="isTestSubmitted"/>
            </cv-radio-group>
            <div class="answers-checkbox" v-else-if="isQuestionCheckboxType(question)">
              <cv-checkbox v-model="userAnswers[question.index].submitted_answers"
                           v-for="(answer, id) in question.all_answers" :key="id"
                           :value="answer"
                           :label="answer" :disabled="isTestSubmitted"/>
            </div>
            <cv-text-input v-model="userAnswers[question.index].submitted_answers[0]"
                           v-else-if="isQuestionInputType(question)" placeholder="Введите ответ"
                           :disabled="isTestSubmitted"/>
            <cv-text-area v-model="userAnswers[question.index].submitted_answers[0]"
                          v-else-if="isQuestionTextType(question)" placeholder="Введите ответ"
                          :disabled="isTestSubmitted"/>
          </div>
        </div>
        <div v-if="!loading" class="submit-container">
          <div class="question-container submit">
            <cv-button v-if="!submitting" @click="submitExam" :disabled="isTestSubmitted">
              Отправить
            </cv-button>
            <cv-button-skeleton v-else/>
          </div>
          <cv-inline-notification
            v-if="showNotification"
            @close="hideNotification"
            :kind="notificationKind"
            :sub-title="notificationText"/>
        </div>
        <cv-loading v-else/>
      </cv-column>
    </cv-row>
  </div>
</template>

<script lang="ts">
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import { Component, Prop } from "vue-property-decorator";
import examStore from '@/store/modules/exam';
import userStore from '@/store/modules/user';
import QuestionModel, { ANSWER_TYPE } from "@/models/QuestionModel";
import viewOff from '@carbon/icons-vue/es/view--off/32';
import view from '@carbon/icons-vue/es/view/32';
import api from "@/store/services/api";
import { Dictionary } from "vue-router/types/router";

@Component({ components: {} })
export default class ExamView extends NotificationMixinComponent {
  @Prop({ required: true }) examId!: number;

  examStore = examStore;
  userStore = userStore;
  changingVisibility = false;
  loading = true;
  isTestSubmitted = false;
  submitting = false;

  userAnswers: Dictionary<{ question_index: number; submitted_answers: Array<string> }> = {};


  async created() {
    this.exam?.questions.forEach((question) => {
      this.userAnswers[question.index] = { question_index: question.index, submitted_answers: [] };
    })
    this.userAnswers = { ...this.userAnswers };
    this.loading = false;
  }

  get isStaff(): boolean {
    return this.userStore.user.staff_for.includes(Number(this.exam?.lesson));
  }

  get exam() {
    return this.examStore.currentExam;
  }

  get hiddenIcon() {
    return (this.exam?.is_hidden) ? viewOff : view;
  }

  async changeExamVisibility() {
    this.changingVisibility = true;
    await this.examStore.patchExam(
      { id: this.examId, is_hidden: !this.exam?.is_hidden },
    );
    this.changingVisibility = false;
  }

  isQuestionInputType(question: QuestionModel) {
    return question.answer_type === ANSWER_TYPE.INPUT;
  }

  isQuestionTextType(question: QuestionModel) {
    return question.answer_type === ANSWER_TYPE.TEXT_FIELD;
  }

  isQuestionRadioType(question: QuestionModel) {
    return question.answer_type === ANSWER_TYPE.RADIO;
  }

  isQuestionCheckboxType(question: QuestionModel) {
    return question.answer_type === ANSWER_TYPE.CHECKBOXES;
  }

  async submitExam() {
    console.log(this.userAnswers);
    this.submitting = true;
    await api.post('/api/solution/', {
      user_answers: Object.values(this.userAnswers),
      score: 0,
      correct_questions_indexes: [],
      student: userStore.user.id,
      exam: this.exam?.id,
    }).then(() => {
      this.notificationKind = 'success';
      this.notificationText = "Тест отправлен на проверку";
      this.isTestSubmitted = true;
    }).catch(error => {
      this.notificationKind = 'success';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
    }).finally(() => {
      this.showNotification = true;
      this.submitting = false;
    });
  }
}
</script>

<style scoped lang="stylus">
h1
  color var(--cds-ui-05)
  font-weight bold

span
  margin-left 0.5rem

.info-container
  display block

.description-container
  max-width 60%
  word-break break-word
  background-color var(--cds-ui-01)
  margin-top 0.5rem
  padding 1rem

.test-info
  color var(--cds-ui-04)
  margin-top 0.5rem
  display inline-flex
  align-items center

.visibility
  margin-left 1rem

.test-container
  color var(--cds-text-01)
  display flex
  flex-direction column
  gap 1rem

.question-container
  background-color var(--cds-ui-01)
  border-radius 5px
  padding 1rem
  width 70%

.question-title
  margin-bottom 0.5rem

.question-description
  margin-left 0.5rem
  margin-bottom 1rem

.answers
  margin-left 1rem

  /deep/ .bx--radio-button-group
    gap 1.5rem

.answers-checkbox
  margin-left 1rem

  /deep/ .bx--form-item.bx--checkbox-wrapper:not(:last-of-type)
    margin-bottom 1.5rem

.cv-text-input
  margin-left 1rem
  width 40%

.cv-text-area
  margin-left 1rem

/deep/ .bx--text-input
  border-radius 5px
  border 1px solid var(--cds-ui-05)

/deep/ .bx--text-area
  border-radius 5px
  border 1px solid var(--cds-ui-05)

.submit-container
  display flex
  gap 1rem
  flex-direction row
  width 60%

.submit
  width fit-content
  margin-top 0.5rem
</style>
