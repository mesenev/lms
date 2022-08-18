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
      <div class="bx--col-lg-9 first--block">
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

          <cv-text-input
            v-model.trim.number="courseEdit.cats_id"
            type="number"
            class="course--cats"
            label="Cats id"/>

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

          <div class="create--change--btn">
            <cv-button-skeleton v-if="fetchingCourse"/>
            <cv-button v-else
                       :disabled="!isChanged"
                       v-on:click="createOrUpdate">
              {{ isNewCourse ? 'Создать' : 'Изменить' }}
            </cv-button>
          </div>

          <EditCourseLessons
            v-if="!isNewCourse && !fetchingCourse"
            :course="courseEdit"
            class="course-props edit--course"/>
          <EditCourseModal
            v-if="!isNewCourse && !fetchingCourse"
            :course-id="courseEdit.id"
            class="course-props add--btn"/>
        </div>
      </div>
      <div class="bx--col-lg-6 second--block" v-if="!isNewCourse">
        <div class="link">
          <h4 class="add-teacher">
            Добавить преподавателя
          </h4>
          <AddTeacherModal class="choose--teacher"
                           :courseId="courseId"/>
        </div>
        <br>
        <div class="link">
          <h4 class="create-link">Создать ссылку-приглашение</h4>
          <cv-number-input
            :light="false"
            :label="'Выберите количество учеников курса'"
            :min="1"
            :step="1"
            v-model="counter"
            class="create-link-input">
          </cv-number-input>
          <br>
          <GenerateLinks
            :counter="counter"
            :courseId="courseId"
            class="generate--link">
            Сгенерировать ссылку
          </GenerateLinks>
          <br>
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
import CourseModel from '@/models/CourseModel';
import router from '@/router';
import courseStore from "@/store/modules/course";
import userStore from '@/store/modules/user';
import axios from 'axios';
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
  counter = 1;
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

  deChanged() {
    this.courseEdit = { ...this.courseEdit, de_options: this.deChecks.sort().join(',') };
  }

  hideSuccess() {
    this.showNotification = false;
  }

  get isChanged(): boolean {
    return !_.isEqual(this.course, this.courseEdit);
  }

  async created() {
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

  createOrUpdate(): void {
    this.catsIdCheck();
    const request = (this.isNewCourse) ?
      axios.post('/api/course/', this.courseEdit) :
      axios.patch(`/api/course/${this.courseEdit.id}/`, this.courseEdit);
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

.description--block
  display flex
  flex-direction row

.add--btn
  float right

.edit--course
  margin-top 2rem

.course--cats
  margin-top 2rem

.course--name
  margin-top 2rem

.course--description
  margin-top 2rem

.course--de
  margin-top 2rem

.create--change--btn
  margin-top 2rem

.first--block
  background-color var(--cds-ui-02)
  margin-top 1rem

.second--block
  margin-top 1rem
  margin-left 5rem
  background-color var(--cds-ui-02)

.main--content
  margin-top 1rem

.page--title
  margin-top 1rem
  display flex
  flex-direction column
  align-items flex-start

.generate--link
  margin-left 2rem
  margin-top 0
  margin-bottom 0

.create-link-input
  margin-left 2rem
  margin-bottom 0.5rem

.create-link
  margin-left 2rem
  margin-top 3rem
  margin-bottom 1rem

.choose--teacher
  margin-left 2rem

.add-teacher
  margin 2rem
  margin-bottom 1rem

.manage-title
  margin-top 1rem

.title
  margin-left 3rem
  margin-top 1rem

.null
  background-color var(--cds-ui-02)

.edit--course-props
  margin-top 10px

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

  .change-btn:not([disabled = disabled])
    background-color var(--cds-ui-05)

  .change-btn
    margin-top 10px

</style>
