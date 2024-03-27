<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <div class="bx--offset-lg-2 main-title">
        <h1>Редактирование теста</h1>
      </div>
    </div>
    <cv-row v-if="!loading" class="main-items" justify="center">
      <cv-column :lg="{'span' : 8, 'offset' : 2}">
        <div class="exam-container">
          <div :class="expanded ? 'expand-container expanded' : 'expand-container'">
            <div @click="expand" class="expand-container-head">
              <p>Настройки теста</p>
              <component class="expand-btn" :is="expanded ? chevronUp : chevronDown"/>
            </div>
            <div class="expand-fields">
              <cv-dropdown v-model:value="examEdit.test_mode" class="testing-type-dropdown"
                           label="Способ тестирования"
                           placeholder="Выберите способ тестирования">
                <cv-dropdown-item value="auto">Auto</cv-dropdown-item>
                <cv-dropdown-item value="manual">Manual</cv-dropdown-item>
                <cv-dropdown-item value="auto_and_manual">Auto & Manual</cv-dropdown-item>
              </cv-dropdown>
              <cv-text-input v-model.trim="examEdit.name" label="Название теста">
                <template v-if="!examEdit.name.length" v-slot:invalid-message>
                  {{ emptyFieldText }}
                </template>
              </cv-text-input>
              <cv-text-area v-model="examEdit.description" label="Описание (опционально)"/>
              <!--              <cv-date-picker kind="single" date-label="Дедлайн"/>-->
            </div>
          </div>
          <div class="questions" v-for="(question, index) in examEdit.questions" :key="index">
            <exam-question-component
                @set-fields-empty="setFieldsEmpty($event.isEmpty, $event.question)"
                :exam="examEdit" :_question="question" :test-id="examEdit.id"
                :invalid-prop="invalidProp"
                @delete-question="deleteQuestion(question)"/>
          </div>
          <div class="action-container">
            <div class="change-container">
              <div class="change">
                <cv-button v-if="!isExamChanging" @click="changeExam" :disabled="!isChanged">
                  Изменить
                </cv-button>
                <cv-button-skeleton v-else></cv-button-skeleton>
              </div>
              <cv-inline-notification
                  v-if="showNotification"
                  @close="() => showNotification=false"
                  :kind="notificationKind"
                  :sub-title="notificationText"/>
            </div>
            <div class="action-btns">
              <component class="action-btn" :is="addAlt" @click="addQuestion"/>
              <!--              <component class="action-btn" :is="image24"/>-->
              <!--              <component class="action-btn" :is="videoAdd"/>-->
              <!--              <component class="action-btn" :is="attachment"/>-->
            </div>
          </div>
        </div>
      </cv-column>
    </cv-row>
    <div v-else class="bx--row">
      <div class="bx--offset-lg-2">
        <cv-loading/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import chevronUp from "@carbon/icons-vue/lib/chevron--up/24";
import chevronDown from "@carbon/icons-vue/lib/chevron--down/24";
import addAlt from "@carbon/icons-vue/lib/add--alt/24";
import videoAdd from "@carbon/icons-vue/lib/video--add/24";
import image24 from "@carbon/icons-vue/lib/image/24";
import attachment from "@carbon/icons-vue/lib/attachment/24";
import _ from 'lodash';
import useExamStore from "@/stores/modules/exam";
import useQuestionStore from "@/stores/modules/question";
import { computed, onMounted, ref } from "vue";
import type { ExamModel } from "@/models/ExamModel";
import type { QuestionModel } from "@/models/QuestionModel";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import api from "@/stores/services/api";
import ExamQuestionComponent from "@/components/ExamQuestionComponent.vue";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  examId: { type: String, required: true }
})


const examStore = useExamStore();
const questionStore = useQuestionStore();
const expanded = ref(false);
const loading = ref(false);
const isExamChanging = ref(false);
const emptyFieldText = ref('');
const invalidProp = ref(false);
const fieldsValid = ref<Set<number>>(new Set<number>());

const exam = ref<ExamModel>({ ...examStore.newExam });
const examEdit = ref<ExamModel>({ ...exam.value });

onMounted(async () => {
  loading.value = true;
  emptyFieldText.value = 'Заполните поле!';
  exam.value = await examStore.fetchExamById(parseInt(props.examId));
  if (!exam.value.questions.length) {
    exam.value.questions.push(
        _.cloneDeep({
          ...questionStore.newQuestion,
          index: 0,
        })
    )
  }
  examEdit.value = _.cloneDeep(exam.value);
  loading.value = false;
})

const isChanged = computed(() => {
  return !_.isEqual(exam.value, examEdit.value);
})

function expand() {
  expanded.value = !expanded.value;
}

function setFieldsEmpty(isEmpty: boolean, question: number) {
  isEmpty ? fieldsValid.value.add(question) : fieldsValid.value.delete(question);
}

function addQuestion() {
  const newQuestion = _.cloneDeep({
    ...questionStore.newQuestion,
    index: examEdit.value.questions.length > 0 ? Math.max(...examEdit.value.questions.map(question => question.index)) + 1 : 0,
  });
  examEdit.value.questions.push(newQuestion);
  examEdit.value.questions.forEach(value => {
    if (!value.text.length)
      fieldsValid.value.add(value.index);
  })
}

function deleteQuestion(question: QuestionModel) {
  if (examEdit.value.questions.length > 1) {
    examEdit.value.questions = examEdit.value.questions.filter(x => x !== question);
  }
}

async function changeExam() {
  isExamChanging.value = true;
  if (fieldsValid.value.size || !examEdit.value.name.length) {
    notificationText.value = 'Проверьте правильность введенных данных';
    notificationKind.value = 'error';
    showNotification.value = true;
    isExamChanging.value = false;
    invalidProp.value = true;
    return;
  }
  examEdit.value.max_points = 0;
  examEdit.value.questions.forEach((question) => {
    examEdit.value.max_points += question.points;
  })
  await api.patch(`/api/exam/${props.examId}/`, {
    ...examEdit.value,
    questions: examEdit.value.questions
  }).then(response => {
    notificationKind.value = 'success';
    notificationText.value = 'Тест успешно изменен';
    exam.value = response.data;
    examStore.changeCurrentExam(exam.value);
  }).catch(error => {
    examEdit.value.max_points = exam.value.max_points;
    notificationText.value = `Что-то пошло не так: ${error.message}`;
    notificationKind.value = 'error';
  }).finally(() => {
    showNotification.value = true;
    isExamChanging.value = false;
  })
}
</script>

<style scoped lang="stylus">
.main-items
  color var(--cds-text-01)

.exam-container
  min-width 45rem

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

span
  margin-bottom 0.25rem

:deep(.bx--text-input) {
  background-color var(--cds-ui-background)
}

:deep(.bx--text-area) {
  background-color var(--cds-ui-background)
}

:deep(.bx--list-box) {
  background-color var(--cds-ui-background)
}

:deep(.bx--list-box__field) {
  display flex
}

:deep(.bx--number input[type=number]) {
  background-color var(--cds-ui-background)
}

:deep(.bx--date-picker__input) {
  background-color var(--cds-ui-background)
  width auto
}

.action-container
  display flex
  justify-content space-between

.expand-fields
  display flex
  flex-direction column
  gap 1rem

.action-btns
  background var(--cds-ui-01)
  display flex
  gap 1rem
  border-radius 5px
  margin-top 0.5rem
  align-self flex-start
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
