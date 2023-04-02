<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div :class="{'bx--offset-lg': isStaff, 'bx--offset-lg-2': !isStaff}" class="main-title">
        <h1 v-if="exam && !loading"> {{ exam.name }} </h1>
        <cv-skeleton-text v-else :heading="true" :width="'35%'" class="main-title"/>
        <div v-if="exam && !loading" class="info-container">
          <div v-if="exam.description" class="description-container">
            <span>
               {{ exam.description }}
            </span>
          </div>
          <div class="test-info">
            <span>Тест</span>
            <span>
              Макс. балл <strong> {{ exam.max_points }} </strong>
            </span>
            <span>
              Режим тестирования: <strong> {{ exam.test_mode }} </strong>
            </span>
            <div v-if="isStaff" class="visibility">
              <cv-button-skeleton v-if="changingVisibility" kind="ghost"/>
              <cv-button v-else
                         class="test-hide-button"
                         :icon="hiddenIcon"
                         kind="ghost"
                         @click="changeExamVisibility">
                {{ (exam.is_hidden) ? "Открыть тест" : "Скрыть тест" }}
              </cv-button>
            </div>
          </div>
        </div>
        <cv-skeleton-text v-else :heading="false" :paragraph="true" :line-count="2" width="70%"/>
      </div>
    </div>
    <cv-row :class="isStaff ? 'main-items' : 'header-container'">
      <cv-column :style="loading || solutionLoading ? 'text-align: -webkit-center' : ''"
                 :lg="isStaff ? {'span' : 8, 'offset' : 0} : {'offset': 2}">
        <div v-if="isStaff ? !loading && !solutionLoading : !loading"
             class="test-container">
          <div v-if="!isStaff && isExamVerified" class="student-results question-container">
            <div class="results">
              <span v-if="incorrectAnswers > 0"> Неверных ответов: <strong>{{
                  incorrectAnswers
                }}</strong> </span>
              <span v-else> Все ответы даны верно! </span>
              <span>
                Итоговый балл:
                <strong>{{ finalPoints }}</strong>
                из
                <strong>{{ exam.max_points }}</strong>
              </span>
            </div>
          </div>
          <div class="question-container" :style="setVerdictBorder(question.index.toString())"
               v-for="(question, index) in questions"
               :key="index">
            <h4 class="question-header">
              {{ question.text }}
              <cv-radio-group v-if="isStaff && solutionId" class="verdict-btns">
                <cv-radio-button
                  :checked="studentSolution.question_verdicts[question.index] === 'incorrect'"
                  @click="setVerdict(question.index, false)" label="✖" value="0"
                  :name="'verdict ' + question.index"/>
                <cv-radio-button
                  :checked="studentSolution.question_verdicts[question.index] === 'correct'"
                  @click="setVerdict(question.index, true)" label="✔" value="1"
                  :name="'verdict ' + question.index"/>
              </cv-radio-group>
            </h4>
            <p class="question-description">{{ question.description }}</p>
            <cv-radio-group class="answers" :vertical="true" v-if="isQuestionRadioType(question)">
              <cv-radio-button v-model="userAnswers[question.index].submitted_answers[0]"
                               v-for="(answer, id) in question.all_answers" :key="id" :name="index"
                               :label="answer" :value="answer"
                               :disabled="disableField"/>
            </cv-radio-group>
            <div class="answers-checkbox" v-else-if="isQuestionCheckboxType(question)">
              <cv-checkbox v-model="userAnswers[question.index].submitted_answers"
                           v-for="(answer, id) in question.all_answers" :key="id"
                           :value="answer"
                           :label="answer" :disabled="disableField"/>
            </div>
            <cv-text-input v-model="userAnswers[question.index].submitted_answers[0]"
                           v-else-if="isQuestionInputType(question)" placeholder="Введите ответ"
                           :disabled="disableField"/>
            <cv-text-area v-model="userAnswers[question.index].submitted_answers[0]"
                          v-else-if="isQuestionTextType(question)" placeholder="Введите ответ"
                          :disabled="disableField"/>
          </div>
        </div>
        <div v-if="isStaff ? !loading && !solutionLoading : !loading" class="submit-container">
          <div class="submit">
            <cv-button v-if="!submitting" @click="submitHandler" :disabled="!disableHandler">
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
      <cv-column v-if="isStaff">
        <div v-if="!loading && solutionId" class="results-container">
          <div v-if="!solutionLoading" class="results">
            <span> Статус: <strong>{{ status }}</strong> </span>
            <span>
              Итоговый балл:
              <strong>{{ finalPoints }}</strong>
              из
              <strong>{{ exam.max_points }}</strong>
            </span>
          </div>
          <cv-inline-loading v-else :active="true"/>
        </div>
        <div v-if="!loading" class="item student-list-container">
          <cv-structured-list v-if="submittedSolutions.length" class="student-list" condensed selectable @change="changeStudent">
            <template slot="headings">
              <cv-structured-list-heading class="pupil-title">Список учеников
              </cv-structured-list-heading>
            </template>
            <template slot="items">
              <cv-structured-list-item
                v-for="solution in submittedSolutions"
                :key="solution.id"
                :checked="checkedStudent(solution.student)"
                :value="solution.student.toString()"
                class="student-list--item"
                name="student">
                <cv-structured-list-data>
                  <user-component :user-id="solution.student"
                                  class="student-list--item--user-component"/>
                </cv-structured-list-data>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
          <empty-list-component v-else class="empty-list" text="Решения отсутствуют"
                                    list-of="solutions"/>
        </div>
        <cv-skeleton-text v-else :heading="false" width="70%" :line-count="5" :paragraph="true"/>
      </cv-column>
    </cv-row>
  </div>
</template>

<script lang="ts">
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import { Component, Prop, Watch } from "vue-property-decorator";
import examStore from '@/store/modules/exam';
import solutionStore from '@/store/modules/solution';
import userStore from '@/store/modules/user';
import QuestionModel, { ANSWER_TYPE } from "@/models/QuestionModel";
import viewOff from '@carbon/icons-vue/es/view--off/32';
import view from '@carbon/icons-vue/es/view/32';
import api from "@/store/services/api";
import { Dictionary } from "vue-router/types/router";
import SolutionModel from "@/models/SolutionModel";
import _ from "lodash";
import UserComponent from "@/components/UserComponent.vue";
import EmptyListComponent from "@/components/EmptyListComponent.vue";

@Component({ components: { EmptyListComponent, UserComponent } })
export default class ExamView extends NotificationMixinComponent {
  @Prop({ required: false, default: null }) solutionIdProp!: number | null;

  examStore = examStore;
  solutionStore = solutionStore;
  userStore = userStore;
  changingVisibility = false;
  loading = true;
  solutionLoading = false;
  isExamSubmitted = false;
  submitting = false;
  studentSolution: SolutionModel = { ...this.solutionStore.defaultSolution };
  teacherSolution = { ...this.studentSolution };
  solutionId = this.solutionIdProp;
  studentId = NaN;

  userAnswers: Dictionary<{ question_index: number; submitted_answers: Array<string> }> = {};

  verdicts: Dictionary<{ question_index: number; verdict: boolean }> = {};


  async created() {
    if (this.solutionId) {
      if (this.isStaff)
        this.studentSolution = await this.solutionStore.fetchSolutionById(this.solutionId);
      this.studentId = this.studentSolution.student;
    } else if (!this.isStaff) {
      try {
        await this.solutionStore.fetchSolutionsByExamAndUser({
          examId: this.exam?.id as number,
          userId: this.userStore.user.id
        }).then(response => {
          this.studentSolution = { ...response[0] };
        })
      } catch (error) {
        this.studentSolution = { ...this.solutionStore.defaultSolution };
      }
    }
    await this.initFields();
    this.loading = false;
  }

  async initFields() {
    this.exam?.questions.forEach((question) => {
      this.userAnswers[question.index] = { question_index: question.index, submitted_answers: [] };
      this.verdicts[question.index] = { question_index: question.index, verdict: false };
    })
    if (this.studentSolution.id) {
      this.teacherSolution = _.cloneDeep(this.studentSolution);
      this.studentSolution.user_answers.forEach((answer) => {
        this.userAnswers[answer.question_index] = answer;
      })
    }
    this.userAnswers = { ...this.userAnswers };
    this.verdicts = { ...this.verdicts };
  }

  @Watch('$route.params.solutionId', { immediate: true, deep: true })
  async unUrlChange() {
    if (this.$route.params.solutionId) {
      this.solutionLoading = true;
      this.solutionId = Number(this.$route.params.solutionId);
      this.changeExistedSolution();
      await this.initFields();
      this.solutionLoading = false;
    }
  }

  get isStaff(): boolean {
    return this.userStore.user.staff_for.includes(Number(this.$route.params.courseId));
  }

  get questions() {
    if (this.isStaff &&
      this.solutionId &&
      this.exam?.test_mode === 'auto_and_manual' &&
      this.exam?.questions
        .filter(x => this.studentSolution.question_verdicts[x.index] === 'await_verification').length
    )
    {
      return this.exam?.questions
        .filter(x => this.studentSolution.question_verdicts[x.index] === 'await_verification');
    }
    return this.exam?.questions;
  }

  get submittedSolutions(): Array<SolutionModel> {
    return this.solutionStore.solutions;
  }

  get exam() {
    return this.examStore.currentExam;
  }

  get finalPoints() {
    return this.exam?.questions
      .filter(x => this.studentSolution.question_verdicts[x.index] === 'correct')
      .map(x => x.points)
      .reduce((a, b) => a + b, 0);
  }

  get status() {
    if (['AWAIT VERIFICATION', 'await'].includes(this.studentSolution.status))
      return 'Ожидает проверки';
    return 'Проверено';
  }

  get isExamVerified() {
    return ['VERIFIED', 'verified'].includes(this.studentSolution.status);
  }

  get incorrectAnswers() {
    return Object.values(this.studentSolution.question_verdicts).filter(x => x === 'incorrect').length;
  }

  get hiddenIcon() {
    return (this.exam?.is_hidden) ? viewOff : view;
  }

  get isSolutionChanged(): boolean {
    return !_.isEqual(this.studentSolution.question_verdicts, this.teacherSolution.question_verdicts);
  }

  get isStudentSolutionExist() {
    return this.submittedSolutions.filter(x => x.student === this.userStore.user.id).length > 0;
  }

  get disableHandler() {
    if (this.isStaff)
      return this.isSolutionChanged;
    return !this.disableField;
  }

  get disableField() {
    if (this.isStaff) {
      return true;
    }
    return this.isExamSubmitted || this.isStudentSolutionExist;
  }

  setVerdict(question_index: number, question_verdict: boolean) {
    if (this.isStaff) {
      this.teacherSolution.question_verdicts[question_index] = question_verdict ? 'correct' : 'incorrect';
    }
  }

  setVerdictBorder(question_index: string) {
    const CORRECT_BORDER = 'border: 2px solid yellowgreen';
    const INCORRECT_BORDER = 'border: 2px solid red';
    const AWAIT_BORDER = 'border: 2px solid var(--cds-ui-01)';
    if (this.isStaff && this.solutionId) {
      if (this.teacherSolution.question_verdicts[question_index] === 'correct')
        return CORRECT_BORDER;
      if (this.teacherSolution.question_verdicts[question_index] === 'incorrect')
        return INCORRECT_BORDER;
    }
    return AWAIT_BORDER;
  }

  async changeExamVisibility() {
    this.changingVisibility = true;
    await this.examStore.patchExam(
      { id: this.exam?.id as number, is_hidden: !this.exam?.is_hidden },
    );
    this.changingVisibility = false;
  }

  checkedStudent(studentId: number): boolean {
    return studentId === this.studentId;
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

  changeCurrentSolution(id: number) {
    if (this.solutionId === id)
      return;
    this.$router.push({
      name: 'ExamViewWithSolution', params: {
        courseId: this.$route.params.courseId,
        lessonId: this.$route.params.lessonId,
        solutionId: id.toString(),
      }
    })
  }

  changeExistedSolution() {
    if (this.submittedSolutions.length) {
      if (this.submittedSolutions.filter(x => x.id === this.solutionId).length) {
        this.studentSolution = this.submittedSolutions.filter(x => x.id === this.solutionId)[0];
        this.studentId = this.studentSolution.student;
      } else {
        this.solutionId = null;
        this.$router.push({
          name: 'ExamView', params: {
            courseId: this.$route.params.courseId,
            lessonId: this.$route.params.lessonId,
            examId: this.exam?.id.toString() as string,
          }
        })
      }
    }
  }

  submitHandler() {
    if (this.isStaff && this.solutionId) {
      this.submitSolution();
    } else {
      this.submitExam();
    }
  }

  async changeStudent(id: number) {
    this.studentId = Number(id);
    this.changeCurrentSolution(this.submittedSolutions.filter(x => x.student === Number(id))[0].id);
  }

  async submitExam() {
    this.submitting = true;
    await api.post('/api/solution/', {
      user_answers: Object.values(this.userAnswers),
      solution_points: 0,
      student: userStore.user.id,
      exam: this.exam?.id,
    }).then(() => {
      this.notificationKind = 'success';
      this.notificationText = "Тест отправлен на проверку";
      this.isExamSubmitted = true;
      this.solutionStore.fetchSolutionsByExamAndUser({
        examId: this.exam?.id as number,
        userId: userStore.user.id
      }).then(response => this.studentSolution = { ...response[0] });
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
    }).finally(() => {
      this.showNotification = true;
      this.submitting = false;
    });
  }

  async submitSolution() {
    this.submitting = true;
    const points = this.exam?.questions
      .filter(x => this.studentSolution.question_verdicts[x.index] === 'correct')
      .map(x => x.points)
      .reduce((a, b) => a + b, 0);
    await api.patch(`/api/solution/${this.solutionId}/`, {
      question_verdicts: this.teacherSolution.question_verdicts,
      status: 'verified',
      solution_points: points,
    }).then(() => {
      this.notificationKind = 'success';
      this.notificationText = "Тест успешно оценен";
      this.teacherSolution.status = 'verified';
      this.studentSolution = _.cloneDeep(this.teacherSolution)
    }).catch(error => {
      this.notificationKind = 'error';
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

.test-info
  span
    margin-left 0.5rem

  span:not(:first-of-type)
    margin-left 1rem

.main-title
  margin-top 1rem

.info-container
  display block

.description-container
  max-width 45rem
  word-break break-word
  color var(--cds-text-02)
  font-weight var(--cds-display-02-font-weight);
  margin-top 0.5rem
  padding 0.5rem

.test-info
  color var(--cds-text-05)
  font-weight 500
  margin-top 0.5rem
  display inline-flex
  align-items center

.visibility
  margin-left 1rem

.results-container
  color var(--cds-ui-05)
  padding 1rem
  margin-bottom 0.5rem
  background-color var(--cds-ui-01)

.results
  display flex
  justify-content space-between

.student-results
  border 1px solid var(--cds-ui-05)
  margin-bottom 0.5rem

.student-list--item--user-component
  padding-left 1rem

.student-list-container
  padding 0 1rem 1rem 1rem
  background-color var(--cds-ui-01)

.test-container
  color var(--cds-text-01)
  display flex
  flex-direction column
  gap 1rem
  max-width 45rem
  padding-left 1rem
  padding-right 1rem

.question-container
  background-color var(--cds-ui-01)
  border-radius 5px
  padding 1rem

.question-header
  margin-bottom 0.5rem
  display flex
  justify-content space-between

.verdict-btns
  max-width fit-content

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

.empty-list
  padding-top 1rem
  padding-bottom 1rem
  text-align center

.submit-container
  display flex
  gap 1rem
  flex-direction row
  width 60%
  margin-top 1.5rem
  padding-left 1rem

  .submit
    width fit-content

</style>
