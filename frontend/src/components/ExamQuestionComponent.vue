<template>
  <div class="question-container" :style="loading ? 'text-align: -webkit-center' : ''">
    <div v-if="!loading">
      <div class="question-header">
        <cv-text-area v-model.trim="question.text" class="question" placeholder="Вопрос">
          <template v-slot:invalid-message v-if="!question.text.length && invalidProp">
            {{ emptyInputInvalidText }}
          </template>
        </cv-text-area>
        <cv-dropdown
            v-model:value="question.answer_type"
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
          <template v-slot:invalid-message v-if="!correctAnswersLength && invalidProp">
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
            <cv-text-input v-model.trim="question.all_answers[index]">
              <template v-slot:invalid-message
                        v-if="!question.all_answers[index].length && invalidProp">
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
          <cv-dropdown @focusout="checkEmptyFields" v-if="!manualTestMode" class="answer"
                       v-model:value="question.correct_answers[0]">
            <cv-dropdown-item :value="answer" v-for="answer in question.all_answers" :key="answer">
              {{ answer }}
            </cv-dropdown-item>
            <template v-slot:invalid-message v-if="!correctAnswersLength && invalidProp">
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
            <cv-text-input v-model.trim="question.all_answers[index]">
              <template v-slot:invalid-message
                        v-if="!question.all_answers[index].length && invalidProp">
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
                           v-model:value="question.correct_answers"
                           :light="true">
            <template v-slot:invalid-message v-if="!correctAnswersLength && invalidProp">
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

<script lang="ts" setup>
import trashCan24 from "@carbon/icons-vue/lib/trash-can/24"
import closeFilled24 from "@carbon/icons-vue/lib/close--filled/24"
import type { PropType } from "vue";
import type { QuestionModel } from "@/models/QuestionModel";
import type { ExamModel } from "@/models/ExamModel";
import useQuestionStore from "@/stores/modules/question";
import { computed, onMounted, onUpdated, ref, watch } from "vue";
import { ANSWER_TYPE } from "@/models/QuestionModel";

const props = defineProps({
  _question: { type: Object as PropType<QuestionModel>, required: true },
  exam: { type: Object as PropType<ExamModel>, required: true },
  invalidProp: { type: Boolean, required: true }
})

const emits = defineEmits(['set-fields-empty', 'delete-question'])

const questionStore = useQuestionStore();
const loading = ref(true);
const question = ref<QuestionModel>({ ...questionStore.newQuestion });

const manualHelpText = ref('');
const paragraphHelpText = ref('');
const emptyInputInvalidText = ref('');
const emptyDropDownInvalidText = ref('');

onMounted(async () => {
  emptyInputInvalidText.value = 'Заполните поле!';
  emptyDropDownInvalidText.value = 'Выберите вариант ответа!';
  manualHelpText.value = 'В текущем режиме проверки ответ проверяется вручную';
  paragraphHelpText.value = 'Данный тип ответа проверяется вручную';
  question.value = props._question;
  loading.value = false;
})

onUpdated(() => {
  checkEmptyFields();
})

const inputType = computed(() => {
  return question.value.answer_type === ANSWER_TYPE.INPUT;
})

const textType = computed(() => {
  return question.value.answer_type === ANSWER_TYPE.TEXT_FIELD;
})

const radioType = computed(() => {
  return question.value.answer_type === ANSWER_TYPE.RADIO;
})

const checkboxType = computed(() => {
  return question.value.answer_type === ANSWER_TYPE.CHECKBOXES;
})

const autoTestMode = computed(() => {
  return props.exam.test_mode === 'auto';
})

const manualTestMode = computed(() => {
  return props.exam.test_mode === 'manual';
})

const correctAnswersLength = computed(() => {
  return question.value.correct_answers.length && (question.value.correct_answers[0] ?? '').length;
})

const checkboxAnswers = computed(() => {
  return question.value.all_answers.map(item => {
    const nameVal = item.toLowerCase();
    return {
      name: nameVal,
      label: item,
      value: nameVal,
      disabled: false,
    }
  })
})

watch(() => props.exam.test_mode, () => {
  if (autoTestMode.value && textType.value) {
    answerTypeChange();
    question.value.answer_type = 'input';
  }
  if (manualTestMode.value)
    question.value.correct_answers = [];
})


function checkEmptyFields() {
  let isAllAnswersInvalid = false;
  let isCorrectAnswersInvalid = false;
  if (!textType.value && !inputType.value) {
    if (question.value.all_answers.length) {
      question.value.all_answers.forEach(value => {
        if (!value.length)
          isAllAnswersInvalid = true;
      })
    } else
      isAllAnswersInvalid = true;
    if (!manualTestMode.value) {
      if (question.value.correct_answers.length)
        question.value.correct_answers.forEach(value => {
          if (!value.length)
            isCorrectAnswersInvalid = true;
        })
      else
        isCorrectAnswersInvalid = true;
    }
  } else if (inputType.value) {
    if (autoTestMode.value) {
      if (question.value.correct_answers.length) {
        question.value.correct_answers.forEach(value => {
          if (!value.length)
            isCorrectAnswersInvalid = true;
        })
      } else
        isCorrectAnswersInvalid = true;
    }
  }
  emits('set-fields-empty', {
    isEmpty: !question.value.text.length
        || isAllAnswersInvalid
        || isCorrectAnswersInvalid,
    question: question.value.index,
  });
}

function answerTypeChange() {
  question.value.correct_answers = [];
  question.value.all_answers = [''];
}

function addAnswer() {
  question.value.all_answers.push('');
}

function deleteAnswer(answer: string) {
  question.value.all_answers = question.value.all_answers.filter(x => x != answer);
  question.value.correct_answers = question.value.correct_answers.filter(x => x != answer);
}

function deleteQuestion() {
  emits('delete-question');
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

:deep() .bx--label
  display none

:deep() .bx--dropdown__wrapper.bx--list-box__wrapper
  max-width 50%

:deep() .bx--list-box__field
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

:deep() .bx--number
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