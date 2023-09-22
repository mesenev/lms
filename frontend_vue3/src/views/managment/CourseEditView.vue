<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div>
        <h1 v-if="!fetchingCourse"
            class="main-title">{{ isNewCourse ? 'Создание курса' : 'Редактирование курса' }}
        </h1>
        <cv-skeleton-text
            v-else
            :heading="true"
            :width="'35%'"
            class="main-title"
            v-text="'Подождите...'"/>
      </div>
    </div>
    <div class="bx--row main--content">
      <div
          v-bind:class="(!isNewCourse)? 'bx--col-lg-5 bx--col-md-4  col-content':'bx--col-lg-6 col-content'">
        <div class="items">
          <confirm-modal
              ref="confirmModal"
              :text="approvedText"
              :approve-handler="deleteCourse"
              :modal-trigger="confirmModalTrigger"/>
          <cv-inline-notification
              v-if="showNotification"
              :kind="notificationKind"
              :sub-title="notificationText"
              @close="hideSuccess"
          />
          <cv-text-input
              :disabled="true"
              :value="`${author.first_name}
             ${author.last_name}
              (${author.username})`.trim()"
              label="Автор"
          />

          <cv-combo-box
              :disabled="!userStore.user.cats_account"
              :options="catsContests"
              :auto-filter="true"
              :auto-highlight="true"
              class="cv-dropdown course--cats"
              :label="(!userStore.user.cats_account)? 'Привязать турнир можно только с действующим cats-аккаунтом':'Введите название турнира'"
              @change="setNewCatsId"
          >
          </cv-combo-box>

          <cv-skeleton-text
              v-if="fetchingCourse"
              :heading="true"
              class="course--name"/>
          <cv-text-input
              v-else
              v-model.trim="courseEdit.name"
              class="course--name"
              label="Название курса">
            <template v-slot:invalid-message v-if="!courseEdit.name">
              {{ emptyInputInvalidText }}
            </template>
          </cv-text-input>

          <cv-skeleton-text
              v-if="fetchingCourse"
              :paragraph="true"
              class="course--description"/>
          <cv-text-area
              v-else
              v-model.trim="courseEdit.description"
              class="course--description"
              label="Описание курса"/>

          <cv-dropdown-skeleton
              v-if="fetchingCourse"
              :inline="true"/>
          <cv-multi-select
              v-else
              v-model:value="deChecks"
              :options="deOptions"
              class="course--de"
              label="Выберите среды разработки"
              title="Доступные среды для отправки решений"
              @change="deChanged"/>
          <div class="btns--container">
            <cv-button-skeleton v-if="fetchingCourse"/>
            <div v-else class="btns">
              <AddTeacherModal
                  v-if="!isNewCourse"
                  :courseId="course.id"
                  class="choose--teacher"/>
              <cv-button
                  :disabled="!isChanged"
                  @click="createOrUpdate">
                {{ isNewCourse ? 'Создать' : 'Изменить' }}
              </cv-button>
            </div>
            <cv-button
                style="margin-top: 1rem"
                v-if="!isNewCourse && !fetchingCourse"
                class="delete-btn"
                @click="showConfirmModal"
                kind="danger">
              Удалить
            </cv-button>
          </div>
        </div>
      </div>
      <div v-if="!isNewCourse && !fetchingCourse" class="bx--col-lg-6 bx--col-md-6 col-content">
        <div class="lessons">
          <EditCourseLessons
              :course="currentCourse"
              class="course-props edit--course"/>
          <div class="lessons-modal">
            <GenerateLinks
                :courseId="course.id"
                class="generate--link"/>
            <EditCourseModal
                :course-id="course.id"
                class="course-props add--btn"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, toRaw, watch } from "vue";
import useCourseStore from "@/stores/modules/course";
import useUserStore from "@/stores/modules/user";
import type { CourseModel } from "@/models/CourseModel";
import type { CatsContestModel, ContestModel } from "@/models/ContestModel";
import _ from 'lodash';
import type { AuthorModel } from "@/models/UserModel";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import api from "@/stores/services/api";
import { useRouter } from "vue-router";
import ConfirmModal from "@/components/ConfirmModal.vue";
import AddTeacherModal from "@/components/EditCourse/AddTeacherModal.vue";
import EditCourseLessons from "@/components/EditCourse/EditCourseLessons.vue";
import EditCourseModal from "@/components/EditCourse/EditCourseModal.vue";
import GenerateLinks from "@/components/EditCourse/GenerateLinks.vue";

const props = defineProps({
  courseId: { type: Number, required: true }
})

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const router = useRouter();
const sendingInfo = ref(false);
const fetchingCourse = ref(true);
const courseStore = useCourseStore();
const userStore = useUserStore();
const approvedText = ref('');
const emptyInputInvalidText = ref('Заполните поле!');
const confirmModalTrigger = ref(false);
const course = ref<CourseModel>({ ...courseStore.newCourse });
const courseEdit = ref({ ...course.value });
const deChecks = ref<string[]>([]);
const deOptions = [
  {
    value: '3', label: 'Cross-platform C/C++ compiler',
    name: 'Cross-platform C/C++ compiler', disabled: false,
  },
  {
    value: '681949', label: 'Python 3.8.1',
    name: 'Python 3.8.1', disabled: false,
  },
];
const contestsFromCats = ref<ContestModel[]>([]);

watch(() => deChecks.value, () => deChanged());

onMounted(async () => {
  if (userStore.user.cats_account)
    (await fetchContests()).forEach(value => {
      contestsFromCats.value.push({
        name: value.name,
        label: value.name,
        value: value.id.toString(),
      });
    });

  if (props.courseId === null) {
    fetchingCourse.value = false;
    return;
  }

  course.value = await courseStore.fetchCourseById(props.courseId as number);
  courseEdit.value = { ...course.value };
  deChecks.value = courseEdit.value.de_options.split(',');
  fetchingCourse.value = false;
})

const catsContests = computed(() => {
  return contestsFromCats.value.map(item => {
    return {
      name: item.name,
      value: item.value,
      label: item.label
    }
  });
})

const isChanged = computed(() => {
  return !_.isEqual(course.value, courseEdit.value);
})

const isNewCourse = computed(() => {
  return isNaN(courseEdit.value.id);
})

const author = computed(() => {
  return course.value.author as AuthorModel;
})

const currentCourse = computed(() => {
  return courseStore.currentCourse as CourseModel;
})

function showConfirmModal() {
  approvedText.value = `Удалить курс: ${courseEdit.value.name}`;
  confirmModalTrigger.value = !confirmModalTrigger.value;
}

function deChanged() {
  courseEdit.value = { ...courseEdit.value, de_options: deChecks.value.sort().join(',') };
}

function hideSuccess() {
  showNotification.value = false;
}

function setNewCatsId(cats_id: number) {
  try {
    courseEdit.value.cats_id = cats_id;
  } catch (error) {
    console.log(error);
  }
}


function catsIdCheck() {
  if (!courseEdit.value.cats_id) {
    courseEdit.value.cats_id = -1;
  }
}

async function fetchContests(): Promise<CatsContestModel[]> {
  let answer = { data: {} };
  await api.get('/api/cats-contests/')
      .then(response => {
        answer = response;
      })
      .catch(error => {
        console.log(error);
      });
  return answer.data as CatsContestModel[];
}

function createOrUpdate(): void {
  catsIdCheck();
  const request = (isNewCourse.value) ?
      api.post('/api/course/', courseEdit.value) :
      api.patch(`/api/course/${courseEdit.value.id}/`, courseEdit.value);
  request.then(response => {
    notificationKind.value = 'success';
    notificationText.value = (props.courseId) ? 'Курс успешно изменён' : 'Курс успешно создан';
    if (isNewCourse.value) {
      courseStore.addCourseToArray(response.data);
      userStore.addStaffToArray(response.data.id);
      router.replace(
          { name: 'course-edit', params: { courseId: response.data.id.toString() } },
      );
    }
    course.value = { ...response.data };
    courseEdit.value = { ...course.value };
    courseStore.changeCurrentCourse({ ...response.data });
  });
  request.catch(error => {
    notificationText.value = `Что-то пошло не так: ${error.message}`;
    notificationKind.value = 'error';
  });
  request.finally(() => showNotification.value = true);
}

async function deleteCourse() {
  if (isNewCourse.value)
    throw Error;
  await api.delete(`/api/course/${courseEdit.value.id}/`)
      .then(async () => {
        courseStore.setCourses(courseStore.courses.filter(x => x.id != courseEdit.value.id));
        // await (this as any).$refs.confirmModal?.hideModal();
        await router.replace({ name: 'home', path: '/' });
      })
      .catch(error => {
        notificationKind.value = 'error';
        notificationText.value = `Что-то пошло не так: ${error.message}`;
        showNotification.value = true;
      })
}
</script>

<style lang="stylus" scoped>
.course--cats
  margin-top 2rem

.course--name
  margin-top 2rem

.course--description
  margin-top 2rem

.course--de
  margin-top 2rem

.btns--container
  margin-top 2rem

.btns
  display flex
  justify-content space-between
  overflow-wrap break-word

.col-content
  margin-right 1rem
  padding-left 0

.lessons
  background-color var(--cds-ui-01)
  padding 1rem

.lessons-modal
  display flex
  justify-content space-between

.generate--link
  margin-top 0
  margin-bottom 0

.choose--teacher
  margin-right 1rem

.add-teacher
  margin 2rem
  margin-bottom 1rem

.manage-title
  margin-top 1rem

.items
  background-color var(--cds-ui-01)
  padding var(--cds-spacing-05)

  /deep/ .bx--text-input
    background-color var(--cds-ui-background)

  /deep/ .bx--text-area
    background-color var(--cds-ui-background)

  /deep/ .bx--list-box
    background-color var(--cds-ui-background)

  .change-btn:not([disabled = disabled])
    background-color var(--cds-ui-05)

  .change-btn
    margin-top 10px

</style>
