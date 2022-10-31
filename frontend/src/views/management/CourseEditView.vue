<template>
  <div class="bx--grid">
    <div class="bx--row page--title">
      <div>
        <h1 v-if="!fetchingCourse"
            class="title">{{ isNewCourse ? 'Создание курса' : 'Редактирование курса' }}
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
      <div v-bind:class="(!isNewCourse)? 'bx--col-lg-5 bx--col-md-4  col-content':'bx--col-lg-6 col-content'">
        <div class="items">
          <cv-inline-notification
            v-if="showNotification"
            @close="hideSuccess"
            :kind="notificationKind"
            :sub-title="notificationText"
          />
          <cv-text-input
            label="Автор"
            :disabled="true"
            :value="`${courseEdit.author.first_name}
             ${courseEdit.author.last_name}
              (${courseEdit.author.username})`.trim()"
          />

          <cv-combo-box
            auto-filter
            @change="setNewCatsId"
            class="cv-dropdown course--cats"
            label="Введите название турнира"
            auto-highlight
            :options="contestsFromCats"
          >
          </cv-combo-box>

          <cv-text-input
            v-model.trim="courseEdit.name"
            class="course--name"
            label="Название курса"/>
          <cv-text-input
            v-model.trim="courseEdit.description"
            class="course--description"
            label="Описание курса"/>
          <cv-multi-select
            v-model="deChecks"
            :options="deOptions"
            class="course--de"
            label="Выберите среды разработки"
            title="Доступные среды для отправки решений"
            @change="deChanged"/>
          <div class="btns--container">
            <cv-button-skeleton v-if="fetchingCourse"/>
            <div class="btns" v-else>
              <AddTeacherModal
                v-if="!isNewCourse"
                class="choose--teacher"
                :courseId="courseId"/>
              <cv-button
                :disabled="!isChanged"
                @click="createOrUpdate">
                {{ isNewCourse ? 'Создать' : 'Изменить' }}
              </cv-button>
            </div>
          </div>
        </div>
      </div>
      <div class="bx--col-lg-6 bx--col-md-6 col-content" v-if="!isNewCourse">
        <div class="lessons">
          <EditCourseLessons
            v-if="!isNewCourse && !fetchingCourse"
            :course="store.currentCourse"
            class="course-props edit--course"/>
          <div class="lessons-modal">
            <GenerateLinks
              :courseId="courseId"
              class="generate--link"/>
            <EditCourseModal
              v-if="!isNewCourse && !fetchingCourse"
              :course-id="store.currentCourse.id"
              class="course-props add--btn"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import AddTeacherModal from "@/components/EditCourse/AddTeacherModal.vue";
import EditCourseLessons from '@/components/EditCourse/EditCourseLessons.vue';
import EditCourseModal from '@/components/EditCourse/EditCourseModal.vue';
import GenerateLinks from "@/components/EditCourse/GenerateLinks.vue";
import CatsContestModel, { ContestModel } from "@/models/ContestModel";
import CourseModel from '@/models/CourseModel';
import router from '@/router';
import courseStore from "@/store/modules/course";
import userStore from '@/store/modules/user';
import api from '@/store/services/api';
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: {
    AddTeacherModal, EditCourseLessons, EditCourseModal, GenerateLinks,
  },
})
export default class CourseEditView extends Vue {
  @Prop() courseId!: number | null;
  sendingInfo = false;
  fetchingCourse = true;
  store = courseStore;
  userStore = userStore;
  showNotification = false;
  notificationKind = 'success';
  notificationText = '';
  course: CourseModel = { ...courseStore.newCourse };
  courseEdit = { ...this.course };
  deChecks: string[] = [];
  deOptions = [
  {
    value: '3', label: 'Cross-platform C/C++ compiler',
    name: 'Cross-platform C/C++ compiler', disabled: false,
  },
  {
    value: '681949', label: 'Python 3.8.1',
    name: 'Python 3.8.1', disabled: false,
  },
];
  contestsFromCats: ContestModel[] = [];

  deChanged() {
    this.courseEdit = { ...this.courseEdit, de_options: this.deChecks.sort().join(',') };
  }

  hideSuccess() {
    this.showNotification = false;
  }

  get isChanged(): boolean {
    return !_.isEqual(this.course, this.courseEdit);
  }

  setNewCatsId(cats_id: number) {
    try {
      this.courseEdit.cats_id = cats_id;
    }
    catch (error) {
      console.log(error);
    }
  }

  async created() {
    (await this.fetchContests()).forEach(value => {
      this.contestsFromCats.push({ value: value.id.toString(), label: value.name, name: value.name});
    });
    if (this.courseId === null) {
      this.fetchingCourse = false;
      return;
    }
    this.course = await this.store.fetchCourseById(this.courseId);
    this.courseEdit = { ...this.course };
    this.deChecks = this.courseEdit.de_options.split(',');
    this.fetchingCourse = false;
  }

  get isNewCourse(): boolean {
    return isNaN(this.courseEdit.id);
  }

  catsIdCheck() {
    if (!this.courseEdit.cats_id) {
      this.courseEdit.cats_id = -1;
    }
  }

  async fetchContests(): Promise<CatsContestModel[]> {
    let answer = { data: {} };
    await api.get('api/cats-contests/')
      .then(response => {
        answer = response;
      })
      .catch(error => {
        console.log(error);
      })
    return answer.data as CatsContestModel[];
}

  createOrUpdate(): void {
    this.catsIdCheck();
    const request = (this.isNewCourse) ?
      api.post('/api/course/', this.courseEdit) :
      api.patch(`/api/course/${this.courseEdit.id}/`, this.courseEdit);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = (this.courseId) ? 'Курс успешно изменён' : 'Курс успешно создан';
      if (this.isNewCourse) {
        this.store.addCourseToArray(response.data);
        this.userStore.addStaffToArray(response.data.id);
        router.replace(
          { name: 'course-edit', params: { courseId: response.data.id.toString() } },
        );
      }
      this.course = { ...response.data };
      this.courseEdit = { ...this.course };
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    })
    request.finally(() => this.showNotification = true);
  }
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
  margin-top 1rem
  margin-right 1rem

.main--content
  margin-top 1rem

.page--title
  margin-top 1rem
  display flex
  flex-direction column
  align-items flex-start

.lessons
  background-color var(--cds-ui-background)
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

.title
  margin-left 3rem
  margin-top 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

  .change-btn:not([disabled = disabled])
    background-color var(--cds-ui-05)

  .change-btn
    margin-top 10px

</style>
