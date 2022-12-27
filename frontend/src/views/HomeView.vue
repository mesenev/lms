<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1>Список курсов</h1>
      </div>
    </div>
    <div class=" bx--row">
      <confirm-modal :text="approvedText"
                     :approve-handler="deleteCourse"
                     :modal-trigger="confirmModalTrigger">
      </confirm-modal>
      <cv-inline-notification
        v-if="showNotification"
        @close="() => showNotification=false"
        kind="error"
        :sub-title="notificationText"
      />
      <div :class="(courses.length) ? 'items bx--col-lg-6 bx--col-md-6'
      : 'empty-items bx--col-lg-6 bx--col-md-6'">
        <cv-data-table-skeleton v-if="loading" :columns="1" :rows="6"/>
        <div v-else-if="courses.length">
          <cv-search
            label="label"
            placeholder="search"
            v-model.trim="searchValue">
          </cv-search>
          <cv-structured-list>
            <template slot="items">
              <cv-structured-list-item
                v-for="course in filterCourses" :key="course.id" class="item">
                <Course :courseProp='course' @show-confirm-modal="showConfirmModal($event)"/>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
        </div>
        <empty-list-component v-else list-of="courses" :text="emptyText"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Course from '@/components/lists/CourseListComponent.vue';
import courseStore from "@/store/modules/course";
import Vue from 'vue';
import Component from 'vue-class-component';
import EmptyListComponent from "@/components/EmptyListComponent.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CourseModel from "@/models/CourseModel";
import api from "@/store/services/api";
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";

@Component({ components: { Course, EmptyListComponent, ConfirmModal } })
export default class HomeView extends NotificationMixinComponent {
  private store = courseStore;
  searchValue = "";
  loading = true;
  emptyText = '';
  deletingCourseId: number | null = null;
  approvedText = '';
  confirmModalTrigger = false;

  async created() {
    this.emptyText = 'В данный момент нет доступных курсов.'
    await this.store.fetchUserCourses();
    this.loading = false;
  }

  get courses() {
    return this.store.courses;
  }

  get filterCourses() {
    return this.courses.filter(c => {
      return c.name.toLowerCase().includes(this.searchValue.toLowerCase())
    })
  }

  showConfirmModal(deletingCourse: CourseModel) {
    this.deletingCourseId = deletingCourse.id;
    this.approvedText = `Удалить курс: ${deletingCourse.name}`;
    this.confirmModalTrigger = !this.confirmModalTrigger;
  }

  async deleteCourse() {
    if (!this.deletingCourseId)
      throw Error;
    await api.delete(`/api/course/${this.deletingCourseId}/`)
      .then(() => {
        this.store.setCourses(this.courses.filter(x => x.id !== this.deletingCourseId));
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

.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.empty-items
  background-color var(--cds-ui-background)
  padding 1rem

.items
  background-color var(--cds-ui-01)
  padding var(--cds-spacing-05)
  min-height 600px

  .bx--structured-list-thead
    display none

.item
  min-height 85px
</style>
