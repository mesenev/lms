<template>
  <div class="bx--grid">
    <div class="bx--row page--title">
      <div>
        <h1 class="title" v-if="!fetchingCourse">{{ isNewCourse ? 'Создание курса' : 'Редактирование курса' }}</h1>
        <cv-skeleton-text v-text="'Подождите...'" v-else :heading="true" :width="'35%'" class="main-title"/>
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
            :value="`${courseEdit.author.first_name} ${courseEdit.author.last_name} (${courseEdit.author.username})`.trim()"
          />
          <cv-text-input class="course--name" label="Название курса" v-model.trim="courseEdit.name"/>

          <div class="description--block">
            <cv-text-input class="course--description" label="Описание курса" v-model.trim="courseEdit.description"/>
            <cv-button-skeleton v-if="fetchingCourse"/>
            <cv-button class="create--change--btn" v-else :disabled="!isChanged" v-on:click="createOrUpdate">
              {{ isNewCourse ? 'Создать' : 'Изменить' }}
            </cv-button>
          </div>

          <EditCourseLessons
            v-if="!isNewCourse"
            :course="courseEdit"
            class="edit&#45;&#45;course-props edit--course"/>
          <EditCourseModal
            v-if="!isNewCourse"
            :course-id="courseEdit.id"
            class="edit&#45;&#45;course-props add--btn"/>
        </div>
      </div>
      <div class="bx--col-lg-6 second--block">
        <div class="link">
          <h4 class="add-teacher">
            Добавить преподавателя
          </h4>
          <AddTeacherModal class="choose--teacher"
                           :courseId="courseId"/>
        </div>
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

  hideSuccess() {
    this.showNotification = false;
  }

  async created() {
    if (this.courseId === null) {
      this.fetchingCourse = false;
      return;
    }
    this.course = await this.store.fetchCourseById(this.courseId);
    this.courseEdit = { ...this.course };
    this.fetchingCourse = false;
  }

  createOrUpdate(): void {
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

.description--block
  display flex
  flex-direction row

.create--change--btn
  margin-top 3.5rem
  margin-left 0.5rem
  margin-bottom 0

.add--btn
  float right

.edit--course
  margin-top 2rem

.course--name
  margin-top 2rem

.course--description
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
