<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <h1 class="main-title">{{ 'Редактирование урока' }}</h1>
      <div class="lesson-hide-button-container">
        <cv-button-skeleton v-if="changingVisibility || !lesson" kind="ghost"
                            class="lesson-hide-button"/>
        <cv-button v-else
                   class="lesson-hide-button"
                   :icon="hiddenIcon"
                   kind="ghost"
                   v-on:click="changeLessonVisibility">
          {{ (lesson.is_hidden) ? "Открыть урок" : "Скрыть урок" }}
        </cv-button>
      </div>
    </div>
    <cv-loading v-if="fetchingLesson"/>
    <div v-else class="bx--row content">
      <div class="bx--col-lg-5 bx--col-md-5">
        <confirm-modal
          class="confirm--modal"
          :text="approvedText"
          :modal-trigger="modalTrigger"
          :approve-handler="deleteLesson"/>
        <div class="edit-content">
          <cv-inline-notification
            v-if="showNotification"
            @close="hideNotification"
            :kind="notificationKind"
            :sub-title="notificationText"
          />
          <cv-text-input
            class="text_field"
            label="Название урока"
            v-model.trim="lessonEdit.name"/>
          <cv-text-area
            class="text_field"
            label="Описание урока"
            v-model.trim="lessonEdit.description"/>
          <cv-date-picker
            class="deadLine text_field"
            kind="single"
            v-model="lessonEdit.deadline"
            date-label="Дедлайн"
            :cal-options=calOptions
          />
          <div class="action-btns">
            <cv-button kind="danger" @click="showConfirmModal(lessonEdit)">
              Удалить
            </cv-button>
            <cv-button :disabled="!isChanged" @click="createOrUpdate">
              {{ isNewLesson ? 'Создать урок' : 'Изменить' }}
            </cv-button>
          </div>
        </div>
        <div class="lesson-buttons">
          <EditLessonModal @update-problem-list="updateTaskList($event)"
                           @update-exam-list="updateExamList($event)"
                           :lesson="lessonEdit"
                           class="edit--lesson-props"/>
          <EditLessonMaterialsModal @update-material-delete="updateMaterialDelete()"
                                    :_lesson="lessonEdit"
                                    class="edit--lesson-props"/>
        </div>
      </div>

      <div class="bx--col-lg-6 bx--col-md-4">
        <cv-content-switcher>
          <cv-content-switcher-button class="type-of-task-tab" owner-id="CW" selected>
            Классная работа
          </cv-content-switcher-button>
          <cv-content-switcher-button class="type-of-task-tab" owner-id="HW">
            Домашняя работа
          </cv-content-switcher-button>
          <cv-content-switcher-button class="type-of-task-tab" owner-id="EX">
            Доп. задания
          </cv-content-switcher-button>
          <cv-content-switcher-button class="type-of-task-tab" owner-id="Test">
            Тесты
          </cv-content-switcher-button>
        </cv-content-switcher>
        <section class="content-task-list">
          <cv-content-switcher-content owner-id="CW">
            <div v-if="getClasswork.length > 0">
              <div v-if="!fetchingLesson" class="classwork">
                <problem-list-component
                  :is-editing="true"
                  @update-problem-delete="updateProblemDelete($event)"
                  :task-list="getClasswork">
                </problem-list-component>
              </div>
              <div v-else>
                <cv-accordion-skeleton/>
              </div>
            </div>
            <h4 v-else class="empty-tasks">Задания отсутствуют</h4>
          </cv-content-switcher-content>
          <cv-content-switcher-content owner-id="HW">
            <div v-if="getHomework.length > 0">
              <div v-if="!fetchingLesson" class="homework">
                <problem-list-component
                  :is-editing="true"
                  @update-problem-delete="updateProblemDelete($event)"
                  :task-list="getHomework">
                </problem-list-component>
              </div>
              <div v-else>
                <cv-accordion-skeleton/>
              </div>
            </div>
            <h4 v-else class="empty-tasks">Задания отсутствуют</h4>
          </cv-content-switcher-content>
          <cv-content-switcher-content owner-id="EX">
            <div v-if="getExtrawork.length > 0">
              <div v-if="!fetchingLesson" class="extrawork">
                <problem-list-component
                  :is-editing="true"
                  @update-problem-delete="updateProblemDelete($event)"
                  :task-list="getExtrawork">
                </problem-list-component>
              </div>
              <div v-else>
                <cv-accordion-skeleton/>
              </div>
            </div>
            <h4 v-else class="empty-tasks">Задания отсутствуют</h4>
          </cv-content-switcher-content>
          <cv-content-switcher-content owner-id="Test">
            <div v-if="getExams.length > 0">
              <div v-if="!fetchingLesson" class="extrawork">
                <exam-list-component
                  :exams-list="getExams"
                  :is-staff="true"
                  :is-editing="true"
                  @update-exam-delete="updateExamDelete($event)"/>
              </div>
              <div v-else>
                <cv-accordion-skeleton/>
              </div>
            </div>
            <h4 v-else class="empty-tasks">Тесты отсутствуют</h4>
          </cv-content-switcher-content>
        </section>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import searchByProblems from '@/common/searchByTutorial'
import _ from 'lodash';
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import useLessonStore from "@/stores/modules/lesson";
import useMaterialStore from "@/stores/modules/material";
import useProblemStore from "@/stores/modules/problem";
import useCourseStore from "@/stores/modules/course";
import useExamStore from "@/stores/modules/exam";
import { computed, onMounted, ref } from "vue";
import type { LessonModel } from "@/models/LessonModel";
import type { CourseModel } from "@/models/CourseModel";
import { useRouter } from "vue-router";
import api from "@/stores/services/api";
import type { ProblemModel } from "@/models/ProblemModel";
import type { CatsProblemModel } from "@/models/CatsProblemModel";
import type { ExamModel } from "@/models/ExamModel";
import ConfirmModal from "@/components/ConfirmModal.vue";
import EditLessonModal from "@/components/EditLesson/EditLessonModal.vue";
import EditLessonMaterialsModal from "@/components/EditLesson/EditLessonMaterialsModal.vue";
import ExamListComponent from "@/components/lists/ExamListComponent.vue";
import ProblemListComponent from "@/components/lists/ProblemListComponent.vue";
import viewOff from '@carbon/icons-vue/es/view--off/32';
import view from '@carbon/icons-vue/es/view/32';

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  lessonId: { type: Number, required: true }
})

const router = useRouter();

const lessonStore = useLessonStore();
const materialStore = useMaterialStore();
const problemStore = useProblemStore();
const courseStore = useCourseStore();
const examStore = useExamStore();
const fetchingLesson = ref(true);
const lesson = ref<LessonModel>(lessonStore.getNewLesson);
const lessonEdit = ref<LessonModel>({ ...lesson.value });
const calOptions = { dateFormat: 'd/m/Y' };
const query = ref('');
const modalTrigger = ref(false);
const approvedText = ref('');
const changingVisibility = ref(false);

onMounted(async () => {
  if (props.lessonId) {
    lesson.value = lessonStore.currentLesson ?? await lessonStore.fetchLessonById(props.lessonId);
    await materialStore.fetchMaterialsByLessonId(lesson.value.id);
    await examStore.fetchExamsByLessonId(lesson.value.id);
  }
  lessonEdit.value = { ...lesson.value };
  fetchingLesson.value = false;
})

const getClasswork = computed((): Array<ProblemModel | CatsProblemModel> => {
  return lessonEdit.value.problems.filter(x => x.type === 'CW');
})

const getHomework = computed((): Array<ProblemModel | CatsProblemModel> => {
  return lessonEdit.value.problems.filter(x => x.type === 'HW');
})

const getExtrawork = computed((): Array<ProblemModel | CatsProblemModel> => {
  return lessonEdit.value.problems.filter(x => x.type === 'EX');
})

const getExams = computed((): Array<ExamModel> => {
  return lessonEdit.value.exams;
})

const hiddenIcon = computed(() => {
  return (lesson.value?.is_hidden) ? viewOff : view;
})


const isNewLesson = computed((): boolean => {
  return isNaN(lessonEdit.value.id);
})

const isChanged = computed((): boolean => {
  return !_.isEqual(lesson.value, lessonEdit.value);
})

async function changeLessonVisibility() {
  changingVisibility.value = true;
  await lessonStore.patchLesson(
    { id: props.lessonId, is_hidden: !lesson.value?.is_hidden },
  );
  lesson.value.is_hidden = !lesson.value.is_hidden;
  lessonEdit.value.is_hidden = lesson.value.is_hidden;
  changingVisibility.value = false;
}

async function deleteLesson() {
  await lessonStore.deleteLesson(lessonEdit.value.id).then(async () => {
    const curCourse = courseStore.currentCourse as CourseModel;
    curCourse.lessons = curCourse.lessons.filter(x => x.id != lessonEdit.value.id);
    lessonStore.setLessons({ [lessonEdit.value.course]: curCourse.lessons });
    courseStore.changeCurrentCourse(curCourse);
    await router.push(
      { name: 'CourseView', params: { courseId: curCourse.id.toString() } }
    );
  }).catch(error => {
    notificationKind.value = 'error';
    notificationText.value = `Что-то пошло не так: ${error.message}`;
    showNotification.value = true;
  });
}

function showConfirmModal(deletingLesson: LessonModel) {
  approvedText.value = `Удалить урок: ${deletingLesson.name}`;
  modalTrigger.value = !modalTrigger.value;
}

function createOrUpdate(): void {
  const request = (isNewLesson.value) ?
    api.post('/api/lesson/', lessonEdit.value) :
    api.patch(`/api/lesson/${lessonEdit.value.id}/`, lessonEdit.value);
  request.then(response => {
    notificationKind.value = 'success';
    notificationText.value = (props.lessonId) ? 'Урок успешно изменён' : 'Урок успешно создан';
    if (isNewLesson.value) {
      router.replace(
        { name: 'lesson-edit', params: { lessonId: response.data.id.toString() } },
      );
    }
    lessonStore.changeCurrentLesson({ ...response.data });
    lesson.value = { ...response.data };
    lessonEdit.value = {...response.data};
  });
  request.catch(error => {
    notificationText.value = `Что-то пошло не так: ${error.message}`;
    notificationKind.value = 'error';
  })
  request.finally(() => showNotification.value = true);
}

function updateTaskList(new_problems: Array<ProblemModel | CatsProblemModel>) {
  lessonEdit.value = { ...lesson.value }
  new_problems.forEach(element => {
    lessonEdit.value.problems.push(element as ProblemModel)
  })
  problemStore.setProblems({ [props.lessonId]: lessonEdit.value.problems });
}

function updateExamList(new_exam: ExamModel) {
  lessonEdit.value = { ...lesson.value };
  lessonEdit.value.exams.push(new_exam);
  examStore.setExams({ [props.lessonId]: lessonEdit.value.exams });
}

function updateProblemDelete(deleted_problem_id: number) {
  lessonEdit.value.problems = lessonEdit.value.problems
    .filter(x => x.id != deleted_problem_id);
  lesson.value.problems = lessonEdit.value.problems;
  problemStore.setProblems({ [props.lessonId]: lessonEdit.value.problems });
}

function updateExamDelete(delete_exam_id: number) {
  lessonEdit.value.exams = lessonEdit.value.exams
    .filter(x => x.id != delete_exam_id);
  lesson.value.exams = lessonEdit.value.exams;
  examStore.setExams({ [props.lessonId]: lessonEdit.value.exams });
}

function updateMaterialDelete() {
  lesson.value.materials = lessonEdit.value.materials;
}

function searchByTutorial(problems: Array<ProblemModel | CatsProblemModel>):
  Array<ProblemModel | CatsProblemModel> {
  return searchByProblems(query.value, problems);
}
</script>

<style scoped lang="stylus">
:deep() .text_field
  margin-bottom 1rem

:deep() .bx--text-input, :deep() .bx--text-area
  background-color var(--cds-ui-background)

.cv-date-picker :deep() .bx--date-picker__input
  background-color var(--cds-ui-background)
  width auto

.bx--col
  margin: 2rem

.lesson-buttons
  display flex
  flex-direction row
  justify-content space-between
  max-width 27rem

.works-col
  margin-right 0
  margin-bottom 1rem
  margin-left 1rem
  margin-top 1rem
  display flex

.work div
  padding 1rem 1rem 0.5rem 1rem

.classwork, .homework, .extrawork
  max-height 25rem
  overflow-y auto
  border var(--cds-ui-05) 1px solid
  margin: 20px 0

.edit-content
  padding 1rem
  background-color var(--cds-ui-01)
  max-width 27rem

.empty-tasks
  color var(--cds-text-01)
  margin-top 1rem
  text-align center

.lesson-buttons
  margin-top 25px
  margin-bottom 25px

.action-btns
  display flex
  flex-direction row
  justify-content space-between

.search
  margin 10px 0

.addButton
  background-color var(--cds-interactive-02)
  margin-left 25px

.main-content
  border 2px black solid;
  margin: 50px

.change__btn
  margin-top: 10px
  background-color: var(--cds-ui-05)

  &:hover
    background-color: var(--cds-ui-04)

.accordion :deep() .bx--accordion__content
  padding-right 0

.lesson-hide-button
  margin-left 1rem
  margin-bottom 1rem

.main-title
  margin-bottom: var(--cds-spacing-04)
</style>
