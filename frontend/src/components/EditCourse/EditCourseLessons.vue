<template>
  <div>
    <div class="main-lesson-container" v-if="course.lessons.length">
      <h4 class="lesson--list--title">Уроки</h4>
      <cv-search label="Поиск"
                 v-model="searchQueryForCourseLessons">
      </cv-search>
      <confirm-modal class="confirm--modal"
                     :deleting-object="deletingLesson"
                     :modal-trigger="modalTrigger"
                     :delete-method="deleteLesson"/>
      <div class="lesson--list">
        <cv-inline-notification
          v-if="showNotification"
          @close="() => showNotification=false"
          kind="error"
          :sub-title="notificationText"/>
        <cv-structured-list id="lessons">
          <template slot="items">
            <cv-structured-list-item class="lesson-card"
                                     v-for="lesson in courseLessons"
                                     :key="lesson.id">
              <div class="lesson">
                <div class="title">
                  <h5>{{ lesson.name }}</h5>
                  <cv-tag v-for="problem in lessonProblems(lesson)"
                          :key="problem"
                          kind="red"
                          :label="problem">
                 </cv-tag>
                </div>
                <div class="icons">
                  <component :is="TrashCan"
                             class="icon"
                             @click="showConfirmModal(lesson)">
                  </component>
                  <component :is="Settings"
                             class="icon"
                             @click="editLesson(lesson)">
                  </component>
                </div>
              </div>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
    </div>
    <div class="no-lessons-title-container" v-else>
      <h3 class="no-lessons-title">Список уроков пуст!</h3>
    </div>
  </div>
</template>

<script lang="ts">
import searchByLessons from '@/common/searchByTutorial';
import lessonStore from '@/store/modules/lesson';
import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import Settings20 from '@carbon/icons-vue/es/settings/20';
import TrashCan20 from '@carbon/icons-vue/es/trash-can/20';
import { Component, Prop } from 'vue-property-decorator';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import router from "@/router";
import _ from "lodash";

@Component({
  components: {
    TrashCan20,
    Settings20,
    ConfirmModal
  },
})
export default class EditCourseLessons extends NotificationMixinComponent {
  @Prop({ required: true }) course!: CourseModel;
  lessonStore = lessonStore;
  TrashCan = TrashCan20;
  Settings = Settings20;
  searchQueryForCourseLessons = '';
  deletingLesson: LessonModel | undefined;
  modalTrigger = false;

  get courseLessons(): LessonModel[] {
    return searchByLessons(this.searchQueryForCourseLessons, this.course.lessons)
      .sort((a, b) => {
        return a.id - b.id
      });
  }

  lessonProblems(lesson: LessonModel) {
    const problems: string[] = [];
    for (const [key, value] of Object.entries(lesson)) {
      if (_.isArrayLike(value) && _.isEmpty(value) && key === 'problems') {
        problems.push(`Empty ${key}`);
      }
    }
    return problems;
  }

  showConfirmModal(deletingLesson: LessonModel) {
    this.deletingLesson = deletingLesson;
    this.modalTrigger = !this.modalTrigger;
  }

  editLesson(lesson: LessonModel) {
    router.push({name: 'lesson-edit', params: {lessonId: lesson.id.toString()}});
  }

  async deleteLesson() {
    await this.lessonStore.deleteLesson(this.deletingLesson!.id).then(() => {
      console.log("ACCEPTED");
      this.course.lessons =
          this.course.lessons.filter((x: LessonModel) => x.id != this.deletingLesson!.id);
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    });
    this.lessonStore.setLessons({[this.course.id]: this.course.lessons});
  }
}
</script>

<style lang="stylus">
.bx--modal-content:focus
  outline none

.no-lessons-title-container
  text-align center

.no-lessons-title
  margin 1rem

#lessons
  margin-bottom 0

.lesson--list--title
  margin-bottom 1rem

.lesson--list
  margin-bottom 1rem
  max-height 18rem
  overflow-y auto

.lesson
    padding 20px
    display flex
    flex-direction row
    justify-content space-between
    align-items center

.title
  display flex
  flex-direction row
  align-items baseline
  h5
    margin-right: 5px

.icon
  transition ease-in-out 0.1s
.icon:active
  transform scale(0.9)
.icon:nth-child(odd)
  margin: 0 10px

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)
</style>
