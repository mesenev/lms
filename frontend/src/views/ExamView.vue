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
                         :disabled="isExamEmpty"
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
      <cv-column v-if="!isExamEmpty" :style="loading || solutionLoading ? 'text-align: -webkit-center' : ''"
                 :lg="isStaff ? {'span' : 8, 'offset' : 0} : {'offset': 2}">
        <div v-if="isStaff ? !loading && !solutionLoading : !loading"
             class="test-container">
          <div v-if="exam && !isStaff && isExamVerified" class="student-results question-container">
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
      <cv-column v-else :lg="{'span' : 2, 'offset' : 0}">
        <empty-list-component text="Заполните тест" list-of="questions"/>
      </cv-column>
      <cv-column v-if="isStaff && !isExamEmpty && exam">
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
          <cv-inline-loading v-else :active="true" state="loading"/>
        </div>
        <div v-if="!loading" class="item student-list-container">
          <cv-structured-list v-if="submittedSolutions.length" class="student-list" condensed selectable
                              @change="changeStudent">
            <template v-slot:headings>
              <cv-structured-list-heading class="pupil-title">Список учеников
              </cv-structured-list-heading>
            </template>
            <template v-slot:items>
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

<script lang="ts" setup>
import viewOff from '@carbon/icons-vue/es/view--off/32';
import view from '@carbon/icons-vue/es/view/32';
import _ from "lodash";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import type { PropType } from "vue";
import { useRoute, useRouter } from "vue-router";
import useExamStore from "@/stores/modules/exam";
import useSolutionStore from "@/stores/modules/solution";
import useUserStore from "@/stores/modules/user";
import { computed, onMounted, ref, watch } from "vue";
import type { SolutionModel } from "@/models/SolutionModel";
import type { QuestionModel } from "@/models/QuestionModel";
import { ANSWER_TYPE } from "@/models/QuestionModel";
import api from "@/stores/services/api";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";
import UserComponent from "@/components/UserComponent.vue";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  solutionIdProp: { type: Object as PropType<number | null>, required: false, default: null }
})

const router = useRouter();
const route = useRoute();


const examStore = useExamStore();
const solutionStore = useSolutionStore();
const userStore = useUserStore();
const changingVisibility = ref(false);
const loading = ref(true);
const solutionLoading = ref(false);
const isExamSubmitted = ref(false);
const submitting = ref(false);
const studentSolution = ref<SolutionModel>({ ...solutionStore.defaultSolution });
const teacherSolution = ref<SolutionModel>({ ...studentSolution.value });
const solutionId = ref(props.solutionIdProp);
const studentId = ref(NaN);

const userAnswers = ref<Dictionary<{ question_index: number; submitted_answers: Array<string> }>>({});

const verdicts = ref<Dictionary<{ question_index: number; verdict: boolean }>>({});


onMounted(async () => {
  if (solutionId.value) {
    if (isStaff.value)
      studentSolution.value = await solutionStore.fetchSolutionById(solutionId.value);
    studentId.value = studentSolution.value.student;
  } else if (!isStaff.value) {
    try {
      await solutionStore.fetchSolutionsByExamAndUser({
        examId: exam.value?.id as number,
        userId: userStore.user.id
      }).then(response => {
        studentSolution.value = { ...response[0] };
      })
    } catch (error) {
      studentSolution.value = { ...solutionStore.defaultSolution };
    }
  }
  await initFields();
  loading.value = false;
})

async function initFields() {
  exam.value?.questions.forEach((question) => {
    userAnswers.value[question.index] = { question_index: question.index, submitted_answers: [] };
    verdicts.value[question.index] = { question_index: question.index, verdict: false };
  })
  if (studentSolution.value.id) {
    teacherSolution.value = _.cloneDeep(studentSolution.value);
    studentSolution.value.user_answers.forEach((answer) => {
      userAnswers.value[answer.question_index] = answer;
    })
  }
  userAnswers.value = { ...userAnswers.value };
  verdicts.value = { ...verdicts.value };
}

watch(() => route.params.solutionId, async () => {
  if (route.params.solutionId) {
    solutionLoading.value = true;
    solutionId.value = Number(route.params.solutionId);
    changeExistedSolution();
    await initFields();
    solutionLoading.value = false;
  }
}, { immediate: true, deep: true })

const isExamEmpty = computed(() => {
  return !exam.value?.questions.length;
})

const isStaff = computed((): boolean => {
  return userStore.user.staff_for.includes(Number(route.params.courseId));
})

const questions = computed(() => {
  if (isStaff.value &&
      solutionId.value &&
      exam.value?.test_mode === 'auto_and_manual' &&
      exam.value?.questions
          .filter(x => studentSolution.value.question_verdicts[x.index] === 'await_verification').length
  ) {
    return exam.value?.questions
        .filter(x => studentSolution.value.question_verdicts[x.index] === 'await_verification');
  }
  return exam.value?.questions;
})

const submittedSolutions = computed((): Array<SolutionModel> => {
  return solutionStore.solutions;
})

const exam = computed(() => {
  return examStore.currentExam;
})

const finalPoints = computed(() => {
  return exam.value?.questions
      .filter(x => studentSolution.value.question_verdicts[x.index] === 'correct')
      .map(x => x.points)
      .reduce((a, b) => a + b, 0);
})

const status = computed(() => {
  if (['AWAIT VERIFICATION', 'await'].includes(studentSolution.value.status))
    return 'Ожидает проверки';
  return 'Проверено';
})

const isExamVerified = computed(() => {
  return ['VERIFIED', 'verified'].includes(studentSolution.value.status);
})

const incorrectAnswers = computed(() => {
  return Object.values(studentSolution.value.question_verdicts).filter(x => x === 'incorrect').length;
})

const hiddenIcon = computed(() => {
  return (exam.value?.is_hidden) ? viewOff : view;
})

const isSolutionChanged = computed((): boolean => {
  return !_.isEqual(studentSolution.value.question_verdicts, teacherSolution.value.question_verdicts);
})

const isStudentSolutionExist = computed(() => {
  return submittedSolutions.value.filter(x => x.student === userStore.user.id).length > 0;
})

const disableHandler = computed(() => {
  if (isStaff.value)
    return isSolutionChanged.value;
  return !disableField.value;
})

const disableField = computed(() => {
  if (isStaff.value) {
    return true;
  }
  return isExamSubmitted.value || isStudentSolutionExist.value;
})

function setVerdict(question_index: number, question_verdict: boolean) {
  if (isStaff.value) {
    teacherSolution.value.question_verdicts[question_index] = question_verdict ? 'correct' : 'incorrect';
  }
}

function setVerdictBorder(question_index: string) {
  const CORRECT_BORDER = 'border: 2px solid yellowgreen';
  const INCORRECT_BORDER = 'border: 2px solid red';
  const AWAIT_BORDER = 'border: 2px solid var(--cds-ui-01)';
  if (isStaff.value && solutionId.value) {
    if (teacherSolution.value.question_verdicts[question_index] === 'correct')
      return CORRECT_BORDER;
    if (teacherSolution.value.question_verdicts[question_index] === 'incorrect')
      return INCORRECT_BORDER;
  }
  return AWAIT_BORDER;
}

async function changeExamVisibility() {
  changingVisibility.value = true;
  await examStore.patchExam(
      { id: exam.value?.id as number, is_hidden: !exam.value?.is_hidden },
  );
  changingVisibility.value = false;
}

function checkedStudent(_studentId: number): boolean {
  return studentId.value === _studentId;
}

function isQuestionInputType(question: QuestionModel) {
  return question.answer_type === ANSWER_TYPE.INPUT;
}

function isQuestionTextType(question: QuestionModel) {
  return question.answer_type === ANSWER_TYPE.TEXT_FIELD;
}

function isQuestionRadioType(question: QuestionModel) {
  return question.answer_type === ANSWER_TYPE.RADIO;
}

function isQuestionCheckboxType(question: QuestionModel) {
  return question.answer_type === ANSWER_TYPE.CHECKBOXES;
}

function changeCurrentSolution(id: number) {
  if (solutionId.value === id)
    return;
  router.push({
    name: 'ExamViewWithSolution', params: {
      courseId: route.params.courseId,
      lessonId: route.params.lessonId,
      solutionId: id.toString(),
    }
  })
}

function changeExistedSolution() {
  //:ToDo its calling before init cause immediate watcher
  if (submittedSolutions.value.length) {
    if (submittedSolutions.value.filter(x => x.id === solutionId.value).length) {
      studentSolution.value = submittedSolutions.value.filter(x => x.id === solutionId.value)[0];
      studentId.value = studentSolution.value.student;
    } else {
      solutionId.value = null;
      router.push({
        name: 'ExamView', params: {
          courseId: route.params.courseId,
          lessonId: route.params.lessonId,
          examId: exam.value?.id.toString() as string,
        }
      })
    }
  }
}

function submitHandler() {
  if (isStaff.value && solutionId.value) {
    submitSolution();
  } else {
    submitExam();
  }
}

async function changeStudent(id: number) {
  studentId.value = Number(id);
  changeCurrentSolution(submittedSolutions.value.filter(x => x.student === Number(id))[0].id);
}

async function submitExam() {
  submitting.value = true;
  await api.post('/api/solution/', {
    user_answers: Object.values(userAnswers.value),
    solution_points: 0,
    student: userStore.user.id,
    exam: exam.value?.id,
  }).then(() => {
    notificationKind.value = 'success';
    notificationText.value = "Тест отправлен на проверку";
    isExamSubmitted.value = true;
    solutionStore.fetchSolutionsByExamAndUser({
      examId: exam.value?.id as number,
      userId: userStore.user.id
    }).then(response => studentSolution.value = { ...response[0] });
  }).catch(error => {
    notificationKind.value = 'error';
    notificationText.value = `Что-то пошло не так: ${error.message}`;
  }).finally(() => {
    showNotification.value = true;
    submitting.value = false;
  });
}

async function submitSolution() {
  submitting.value = true;
  const points = exam.value?.questions
      .filter(x => studentSolution.value.question_verdicts[x.index] === 'correct')
      .map(x => x.points)
      .reduce((a, b) => a + b, 0);
  await api.patch(`/api/solution/${solutionId.value}/`, {
    question_verdicts: teacherSolution.value.question_verdicts,
    status: 'verified',
    solution_points: points,
  }).then(() => {
    notificationKind.value = 'success';
    notificationText.value = "Тест успешно оценен";
    teacherSolution.value.status = 'verified';
    studentSolution.value = _.cloneDeep(teacherSolution.value)
  }).catch(error => {
    notificationKind.value = 'error';
    notificationText.value = `Что-то пошло не так: ${error.message}`;
  }).finally(() => {
    showNotification.value = true;
    submitting.value = false;
  });
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

  :deep() .bx--radio-button-group
    gap 1.5rem

.answers-checkbox
  margin-left 1rem

  :deep() .bx--form-item.bx--checkbox-wrapper:not(:last-of-type)
    margin-bottom 1.5rem

.cv-text-input
  margin-left 1rem
  width 40%

.cv-text-area
  margin-left 1rem

:deep() .bx--text-input
  border-radius 5px
  border 1px solid var(--cds-ui-05)

:deep() .bx--text-area
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
