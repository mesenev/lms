<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить задание
    </cv-button>
    <cv-modal
        :primary-button-disabled="addButtonDisabled"
        :visible="modalVisible"
        class="add_lesson_modal"
        @modal-hidden="modalHidden"
        @primary-click="primaryHandler">
      <template v-slot:label>{{ lesson.name }}</template>
      <template v-slot:title>
        Добавить задание
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button parent-switcher="Problems" owner-id="Problems"
                                      selected>
            Импортировать задачу из cats
          </cv-content-switcher-button>
          <cv-content-switcher-button parent-switcher="Exams" owner-id="Exams">
            Создать тест
          </cv-content-switcher-button>
        </cv-content-switcher>
        <cv-content-switcher-content parent-switcher="Problems" owner-id="Problems">
          <cv-inline-notification
              v-if="showNotification"
              @close="() => showNotification=false"
              :kind="notificationKind"
              :sub-title="notificationText"/>
        </cv-content-switcher-content>
      </template>
      <template v-slot:content>
        <section class="modal--content">
          <cv-content-switcher-content parent-switcher="Problems" owner-id="Problems">
            <div class="content-1">
              <div class="problem-type-selection">
                <h5>Выберите способ тестирования</h5>
                <cv-radio-group>
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
              </div>
              <div class="problem-type-selection">
                <h5>Тип задачи</h5>
                <cv-radio-group
                    @change="(newType) => problemType = newType"
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
              <div>
                <cv-data-table
                    v-if="!fetchingCatsProblems" ref="table"
                    v-model:rowsSelected="selected" :columns="columns" :data="catsFilteredProblems"
                    :stickyHeader="true"
                    class="cats-problems-table" :expanding-search="false"
                    @search="onSearch">
                  <template v-slot:batch-actions>
                    <div></div>
                  </template>
                </cv-data-table>
                <cv-data-table-skeleton v-else/>
              </div>
            </div>
            <div class="content-2" hidden>
              <cv-text-input :model-value="lesson.name" disabled label="Название урока"/>
              <cv-text-input v-model.trim="currentProblem.name" label="Название задания"/>
              <cv-text-input v-model.trim="currentProblem.description" label="Описание задания"/>
            </div>
          </cv-content-switcher-content>
          <cv-content-switcher-content parent-switcher="Exams" owner-id="Exams">
            <div class="exam-container">
              <div class="exam-container-head">
                <p>Настройки теста</p>
                <cv-dropdown v-model:value="exam.test_mode" class="testing-type-dropdown"
                             placeholder="Выберите опцию"
                             label="Способ тестирования">
                  <template v-slot:invalid-message v-if="showInvalidMessage && !exam.test_mode">
                    Выберите способ тестирования!
                  </template>
                  <cv-dropdown-item value="auto">Auto</cv-dropdown-item>
                  <cv-dropdown-item value="manual">Manual</cv-dropdown-item>
                  <cv-dropdown-item value="auto_and_manual">Auto & Manual</cv-dropdown-item>
                </cv-dropdown>
              </div>
              <div class="exam-fields">
                <cv-text-input v-model="exam.name" label="Название теста">
                  <template v-slot:invalid-message v-if="!exam.name && showInvalidMessage">
                    {{ emptyInputInvalidText }}
                  </template>
                </cv-text-input>
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
      <template v-slot:primary-button>
        {{ isExamsSelected ? 'Создать тест и перейти к редактированию' : 'Добавить задачу' }}
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts" setup>
import searchByProblems from '@/common/searchByTutorial';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import _ from 'lodash';
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import type { PropType } from "vue";
import type { LessonModel } from "@/models/LessonModel";
import useProblemStore from "@/stores/modules/problem";
import { computed, onMounted, ref, watch } from "vue";
import type { ProblemModel } from "@/models/ProblemModel";
import type { CatsProblemModel } from "@/models/CatsProblemModel";
import useExamStore from "@/stores/modules/exam";
import type { ExamModel } from "@/models/ExamModel";
import api from "@/stores/services/api";
import { useRouter } from "vue-router";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  lesson: { type: Object as PropType<LessonModel>, required: true }
})

const emits = defineEmits(['update-problem-list', 'update-exam-list']);

const router = useRouter();

const problemStore = useProblemStore();
const currentProblem = ref<ProblemModel>({ ...problemStore.getNewProblem, lesson: props.lesson.id });
const selected = ref([]);
const columns = ['id', 'Название', 'Статус'];

const problems = ref<ProblemModel[]>([]);
const catsProblems = ref<CatsProblemModel[]>([]);
const catsProblemsTruncated = ref<{ id: number; name: string; status: string }[]>([]);
const fetchingCatsProblems = ref(true);
const modalVisible = ref(false);
const searchQueryForAllProblems = ref('');
const testingMode = ref('');
const problemType = ref('');
const loading = ref(false);

const contentType = ref('Problems');
const examStore = useExamStore();
const exam = ref<ExamModel>({ ...examStore.newExam, lesson: props.lesson.id });
const emptyInputInvalidText = 'Заполните поле!';
const showInvalidMessage = ref(false);


const catsFilteredProblems = computed(() => {
  return searchByProblems(searchQueryForAllProblems.value, catsProblemsTruncated.value);
})

onMounted(async () => {
  if (!props.lesson.course) return
  exam.value = _.cloneDeep(exam.value);
  await fetchCatsProblems()
})

async function fetchCatsProblems() {
  fetchingCatsProblems.value = true;
  await api.get(`/api/cats-problems/${props.lesson.course}/`)
      .then(response => {
        catsProblems.value = response.data;
      })
      .catch(error => {
        console.log(error.response);
        notificationKind.value = 'error';
        notificationText.value = `Ошибка получения списка задач: ${error.message}`;
        showNotification.value = true;
      })
  catsProblems.value.map(value => {
    catsProblemsTruncated.value.push(
        { id: value.id, name: value.name, status: value.status },
    )
  });
  catsProblemsTruncated.value = [...catsProblemsTruncated.value];
  fetchingCatsProblems.value = false;
}

function onSearch(value: string) {
  searchQueryForAllProblems.value = value;
}

function showModal() {
  modalVisible.value = true;
  showNotification.value = false;
  currentProblem.value = { ...problemStore.getNewProblem, lesson: props.lesson.id };
}

function modalHidden() {
  problemType.value = '';
  testingMode.value = '';
  modalVisible.value = false;
}

function actionSelected(type: string) {
  hideNotification();
  setContentType(type);
}

function setContentType(type: string) {
  contentType.value = type;
}

function clearData() {
  selected.value = [];
}

function checkCorrectFields() {
  showInvalidMessage.value = !exam.value.name || !exam.value.test_mode;
}

const isExamsSelected = computed(() => {
  return contentType.value === 'Exams';
})

const selectedIds = computed(() => {
  return selected.value.map(e => {
    return (catsFilteredProblems.value[e as number] as unknown as { id: number })['id'];
  })
})

const addButtonDisabled = computed(() => {
  if (isExamsSelected.value)
    return loading.value;
  else
    return !selected.value.length || loading.value;
})

const selectedCatsProblems = computed(() => {
  return catsProblems.value.filter(element => {
    return selectedIds.value.find(e => e === element.id);
  });
})

const areUsedTasks = computed(() => {
  return props.lesson.problems.filter(element => {
    return selectedCatsProblems.value.find(e => e.id === element.cats_id)?.id
        && element.type === problemType.value;
  }).length > 0;
})

async function primaryHandler() {
  if (isExamsSelected.value) {
    checkCorrectFields();
    if (showInvalidMessage.value)
      return;
    await createExam();
  } else
    await addProblem();
}

async function addProblem() {
  if (!props.lesson.id) {
    notificationKind.value = 'error';
    notificationText.value = 'id урока не указано!';
    showNotification.value = true;
    throw new Error('add cats problems  -- course id not found!');
  }
  if (contentType.value !== 'Problems')
    return
  if (testingMode.value === '') {
    notificationKind.value = 'error';
    notificationText.value = 'Выберите режим тестирования';
    showNotification.value = true;
    return
  }
  if (problemType.value === '') {
    notificationKind.value = 'error';
    notificationText.value = 'Выберите тип задачи';
    showNotification.value = true;
    return
  }
  if (areUsedTasks.value) {
    notificationKind.value = 'error';
    notificationText.value = `Урок уже содержит одну из выбранных задач.`;
    showNotification.value = true;
    return;
  }
  if (contentType.value === 'Problems') {
    loading.value = true;
    const data = selectedCatsProblems.value;
    const problemTypes = new Map<string, number>([['CW', 0], ['HW', 1], ['EX', 2]]);
    data.forEach(element => element.test_mode = testingMode.value);
    await api.post(
        `/api/lesson/${props.lesson.id}/add_cats_problems/`,
        { problem_data: data, problem_type: problemTypes.get(problemType.value) },
    )
        .then(async (answer) => {
          if (answer.status == 200) {
            const newProblems = (answer.data as ProblemModel[]).map(element => {
              element.type = problemType.value;
              return element;
            });
            emits("update-problem-list", newProblems as ProblemModel[]);
            modalHidden();
            clearData();
            // await this.fetchCatsProblems();
          }
        }).catch(answer => {
          notificationKind.value = 'error';
          notificationText.value = `Произошла ошибка при добавлении задач. ${answer.message}`;
          showNotification.value = true;
        }).finally(() => {
          loading.value = false;
        })
  }
}

async function createExam() {
  loading.value = true;
  await api.post('/api/exam/', exam.value).then(async response => {
    notificationKind.value = 'success';
    notificationText.value = 'Тест успешно создан';
    emits('update-exam-list', response.data as ExamModel);
    await modalHidden();
    await router.push(
        { name: 'exam-edit', params: { examId: response.data.id.toString() } },
    );
  }).catch(error => {
    notificationText.value = `Что-то пошло не так: ${error.message}`;
    notificationKind.value = 'error';
  }).finally(() => {
    loading.value = false;
    showNotification.value = true;
  })
}
</script>

<style scoped lang="stylus">
.add_lesson_modal /deep/ .bx--modal-container
  background var(--cds-ui-background)

/deep/ .bx--modal-content:focus
  outline none

/deep/ .bx--modal-content
  margin-bottom var(--cds-spacing-04)
  padding-top 0

/deep/ .bx--text-input,
/deep/ .bx--text-area,
/deep/ .bx--dropdown
  background-color var(--cds-ui-background)

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
  margin-bottom 1rem

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
