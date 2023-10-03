<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить урок
    </cv-button>
    <cv-modal class="add_lesson_modal"
              id="add_lesson_modal"
              :visible="modalVisible"
              :disableTeleport="true"
              @modal-hidden="modalHidden"
              :primary-button-disabled="primaryButtonDisabled"
              @primary-click="addLesson"
              @secondary-click="() => {}">
      <template v-slot:label>{{ course.name }}</template>
      <template v-slot:title>
        Добавить урок
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button owner-id="create-lesson" selected>
            Создать новый
          </cv-content-switcher-button>
          <cv-content-switcher-button owner-id="select-lesson" :disabled="true">
            Выбрать из существующих
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template v-slot:content>
        <cv-inline-notification
          v-if="showNotification"
          :kind="notificationKind"
          @close="hideNotification"
          :sub-title="notificationText"
        />
        <section class="modal--content">
          <cv-content-switcher-content owner-id="create-lesson">
            <div class="content-1">
              <cv-text-input class="modal--content--input"
                             label="Название курса" v-model.trim="course.name" disabled/>
              <cv-text-input class="modal--content--input"
                             label="Автор" v-model.trim="authorUsername" disabled/>
              <cv-text-input class="modal--content--input"
                             placeholder="Введите название урока"
                             label="Название урока" v-model.trim="currentLesson.name">
                <template v-slot:invalid-message v-if="showInvalidMessage && !currentLesson.name.length">
                  {{ emptyInputInvalidText }}
                </template>
              </cv-text-input>
              <cv-text-input class="modal--content--input"
                             placeholder="Введите описание урока"
                             label="Описание урока" v-model.trim="currentLesson.description"/>
              <span style="font-style: italic">
              Добавление к уроку материалов и задач доступно после создания урока.
            </span>
            </div>
          </cv-content-switcher-content>
          <cv-content-switcher-content owner-id="select-lesson">
            <div class="content-2" hidden>
              <div>
                <cv-structured-list>
                  <template v-slot:items>
                    <cv-search v-model:value="searchQueryForAllLessons"></cv-search>
                    <cv-structured-list-item
                      class="lesson-card"
                      v-for="lesson in allLessons"
                      :key="lesson.id">
                      <LessonCard
                        :lesson="lesson"
                        :main-icon="AddAlt32"
                        :change-main-icon="SubtractAlt32"
                        :manipulation="chooseLesson">
                      </LessonCard>
                    </cv-structured-list-item>
                  </template>
                </cv-structured-list>
              </div>
            </div>
          </cv-content-switcher-content>
        </section>
      </template>
      <template v-slot:primary-button>
        Добавить
      </template>
    </cv-modal>
  </div>
</template>

<!-- TODO: get counts from num-input -->

<script lang="ts" setup>
import searchByLessons from '@/common/searchByTutorial';
import LessonCard from '@/components/EditCourse/LessonCard.vue';
import AddAlt32 from '@carbon/icons-vue/es/add--alt/32';
import SubtractAlt32 from '@carbon/icons-vue/es/subtract--alt/32';
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import useCourseStore from "@/stores/modules/course";
import useLessonStore from "@/stores/modules/lesson";
import { computed, ref } from "vue";
import type { LessonModel } from "@/models/LessonModel";
import api from "@/stores/services/api";
import type { CourseModel } from "@/models/CourseModel";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  courseId: { type: Number, required: true }
})


const courseStore = useCourseStore();
const lessonStore = useLessonStore();
const currentLesson = ref<LessonModel>({ ...lessonStore.getNewLesson, course: props.courseId });
const fetchingLessons = ref(true);
const selectedNew = ref(true);
const creationLoader = ref(false);

const lessons = ref<LessonModel[]>([]);
const modalVisible = ref(false);
const searchQueryForAllLessons = ref('');
const showInvalidMessage = ref(false);
const emptyInputInvalidText = 'Заполните поле!';

const primaryButtonDisabled = computed((): boolean => {
  return !lessons.value.length && creationLoader.value;
})

const course = computed(() => {
  return courseStore.currentCourse || courseStore.newCourse;
})

const allLessons = computed((): LessonModel[] => {
  return searchByLessons(searchQueryForAllLessons.value, freeLessons.value);
})

const freeLessons = computed((): LessonModel[] => {
  // TODO: fix this
  return [];
})

const authorUsername = computed(() => {
  return course.value.author?.username as string;
})

function showModal() {
  modalVisible.value = true;
  showNotification.value = false;
  currentLesson.value = { ...lessonStore.getNewLesson, course: props.courseId };
  creationLoader.value = false;
}

function modalHidden() {
  modalVisible.value = false;
}

function actionSelected(value: string) {
  selectedNew.value = value === 'create-lesson';
}

const getSelected = computed((): string => {
  return lessons.value.concat(currentLesson.value)
    .map((l) => l.name)
    .sort((a, b) => a < b ? -1 : 1)
    .join(' ');
})

async function addLesson() {
  if (selectedNew.value) {
    checkCorrectFields();
    if (showInvalidMessage.value)
      return;
    creationLoader.value = true;
    await createNewLesson();
  }
}

function chooseLesson() {
  //;
}

function checkCorrectFields() {
  showInvalidMessage.value = !currentLesson.value.name.length;
}

async function createNewLesson() {
  await api.post('/api/lesson/', currentLesson.value)
    .then(response => {
      const course = courseStore.currentCourse as CourseModel;
      course.lessons.push(response.data as LessonModel);
      lessonStore.setLessons({ [course.id]: course.lessons });
      modalHidden();
    })
    .catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    })
    .finally(() => {
      creationLoader.value = false;
    })
}

</script>

<style scoped lang="stylus">
:deep() .bx--modal-content:focus
  outline none

.lesson_list
  margin-bottom 0

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)

.switcher
  margin-bottom: 5px

.cv-text-input
  margin-bottom 1rem

:deep() .bx--modal-content
  margin-bottom 0

:deep() .bx--text-input:disabled
  background-color var(--cds-ui-02)

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
</style>
