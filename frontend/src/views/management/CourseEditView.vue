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
            :value="`${courseEdit.author.first_name}
             ${courseEdit.author.last_name}
              (${courseEdit.author.username})`.trim()"
            label="Автор"
          />


          <cv-combo-box
            :disabled="!userStore.user.cats_account"
            :options="contestsFromCats"
            auto-filter
            auto-highlight
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
            <template slot="invalid-message" v-if="!courseEdit.name">
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
            label="Описание курса" />

          <cv-dropdown-skeleton
            v-if="fetchingCourse"
            :inline="true"/>
          <cv-multi-select
            v-else
            v-model="deChecks"
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
                :courseId="courseId"
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
      <div v-if="!isNewCourse" class="bx--col-lg-6 bx--col-md-6 col-content">
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
import ConfirmModal from "@/components/ConfirmModal.vue";

@Component({
  components: {
    ConfirmModal, AddTeacherModal, EditCourseLessons, EditCourseModal, GenerateLinks,
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
  approvedText = '';
  emptyInputInvalidText = 'Заполните поле!'
  confirmModalTrigger = false;
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

  async created() {
    if (this.userStore.user.cats_account)
      (await this.fetchContests()).forEach(value => {
        this.contestsFromCats.push({
          value: value.id.toString(),
          label: value.name,
          name: value.name
        });
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

  get isChanged(): boolean {
    return !_.isEqual(this.course, this.courseEdit);
  }

  get isNewCourse(): boolean {
    return isNaN(this.courseEdit.id);
  }

  showConfirmModal() {
    this.approvedText = `Удалить курс: ${this.courseEdit.name}`;
    this.confirmModalTrigger = !this.confirmModalTrigger;
  }

  deChanged() {
    this.courseEdit = { ...this.courseEdit, de_options: this.deChecks.sort().join(',') };
  }

  hideSuccess() {
    this.showNotification = false;
  }

  setNewCatsId(cats_id: number) {
    try {
      this.courseEdit.cats_id = cats_id;
    } catch (error) {
      console.log(error);
    }
  }


  catsIdCheck() {
    if (!this.courseEdit.cats_id) {
      this.courseEdit.cats_id = -1;
    }
  }

  async fetchContests(): Promise<CatsContestModel[]> {
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
      this.store.changeCurrentCourse({...response.data});
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    });
    request.finally(() => this.showNotification = true);
  }

  async deleteCourse() {
    if (this.isNewCourse)
      throw Error;
    await api.delete(`/api/course/${this.courseEdit.id}/`)
      .then(async () => {
        this.store.setCourses(this.store.courses.filter(x => x.id != this.courseEdit.id));
        await (this as any).$refs.confirmModal?.hideModal();
        await this.$router.replace({ name: 'Home', path: '/' });
      })
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.showNotification = true;
      })
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
