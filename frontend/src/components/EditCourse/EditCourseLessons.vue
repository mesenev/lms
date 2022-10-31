<template>
  <div>
    <div class="main-lesson-container" v-if="course.lessons.length">
      <h4 class="lesson--list--title">Уроки</h4>
      <cv-search label="Поиск"
                 v-model="searchQueryForCourseLessons">
      </cv-search>
      <div class="lesson--list">
        <cv-structured-list id="lessons">
          <template slot="items">
            <cv-structured-list-item class="lesson-card"
                                     v-for="lesson in courseLessons"
                                     :key="lesson.id">
              <LessonCard :lesson="lesson"
                          :main-icon="TrashCan"
                          :second-icon="Settings"
                          :manipulation="deleteLesson">
              </LessonCard>
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
import LessonCard from '@/components/EditCourse/LessonCard.vue';
import lessonStore from '@/store/modules/lesson';
import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import Settings20 from '@carbon/icons-vue/es/settings/20';
import TrashCan20 from '@carbon/icons-vue/es/trash-can/20';
import { Component, Prop, Vue } from 'vue-property-decorator';
import api from '@/store/services/api'

@Component({
  components: {
    LessonCard,
    TrashCan20,
    Settings20,
  },
})
export default class EditCourseLessons extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  lessonStore = lessonStore;

  TrashCan = TrashCan20;

  Settings = Settings20;

  searchQueryForCourseLessons = '';

  get courseLessons(): LessonModel[] {
    return searchByLessons(this.searchQueryForCourseLessons, this.course.lessons)
      .sort((a, b) => {
        return a.id - b.id
      });
  }

  async deleteLesson(lesson: LessonModel) {
    this.course.lessons = this.course.lessons.filter((x: LessonModel) => x.id != lesson.id);
    await this.lessonStore.deleteLesson(lesson.id);
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

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)
</style>
