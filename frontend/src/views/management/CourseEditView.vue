<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-8">
        <div>
          <h1 class="title">{{ isNewCourse ? 'Создание курса' : 'Редактирование курса' }}</h1>
        </div>
        <br>  <!-- TODO: get off br -->
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
            :value="`${courseEdit.author.first_name} ${courseEdit.author.last_name} (${courseEdit.author.username})`.trim()"
          />
          <cv-text-input label="Название курса" v-model.trim="courseEdit.name"/>
          <cv-text-input label="Описание курса" v-model.trim="courseEdit.description"/>
          <cv-button v-if="!fetchingCourse" :disabled="!isChanged" v-on:click="createOrUpdate">
            {{ isNewCourse ? 'Создать' : 'Изменить' }}
          </cv-button>
          <cv-button-skeleton v-if="fetchingCourse"></cv-button-skeleton>
          <EditCourseLessons
            v-if="!isNewCourse"
            :course="courseEdit"
            class="edit&#45;&#45;course-props"/>
          <EditCourseModal
            :course="courseEdit"
            class="edit&#45;&#45;course-props"/>
        </div>
      </div>
      <div class="bx--col-lg-5">
        <div class="link">
          <h4 class="add-teacher">
            Добавить преподавателя
          </h4>
          <AddTeacherModal/>
        </div>
        <div class="link">
          <h4 class="create-link">Создать ссылку-приглашение</h4>
          <cv-number-input
            :light="true"
            :label="'Выберите количество учеников курса'"
            :min="1"
            :step="1"
            v-model="counter"
            class="create-link-input">
          </cv-number-input>
          <br>
          <GenerateLinks
            :counter="counter"
            :courseId="courseId">
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

@Component({ components: { AddTeacherModal, EditCourseLessons, EditCourseModal, GenerateLinks } })
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
  course: CourseModel = {
    id: NaN,
    name: '',
    author: { ...userStore.user },
    lessons: [],
    completed: false,
    description: '',
    students: [],
  };
  courseEdit = { ...this.course };

  hideSuccess() {
    this.showNotification = false;
  }

  created() {
    if (this.courseId === null) {
      this.fetchingCourse = false;
      return;
    }
    this.course = this.store.currentCourse as CourseModel;
    this.courseEdit = { ...this.course };
  }

  createOrUpdate(): void {
    if (this.isNewCourse)
      delete this.courseEdit.id;
    const request = (this.isNewCourse) ?
      axios.post('/api/course/', this.courseEdit) :
      axios.patch(`/api/course/${this.courseEdit.id}/`, this.courseEdit);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = (this.courseId) ? 'Курс успешно изменён' : 'Курс успешно создан';
      if (this.isNewCourse) {
        this.store.addCourseToArray(response.data);
        router.replace(
          { name: 'course-edit', params: { courseId: response.data.id.toString() } },
        );
      }
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    })
    request.finally(() => this.showNotification = true);
  }

  get isNewCourse(): boolean {
    return isNaN(this.courseEdit.id);
  }

  get isChanged(): boolean {
    return !_.isEqual(this.course, this.courseEdit);
  }
}
</script>

<style lang="stylus">


.create-link-input
  margin-left 0.2rem
  padding-bottom 0.5rem

.items
  margin-top 2rem

.create-link
  margin-top 2rem
  margin-left 0.2rem
  padding-bottom 0.5rem

.add-teacher
  margin-top 7rem
  margin-left 0.2rem
  padding-bottom 0.5rem

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
