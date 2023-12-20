<template>
  <div>
    <div class="main-lesson-container" v-if="course.lessons.length">
      <h4 class="lesson--list--title">Уроки</h4>
      <cv-search v-model:value="searchQueryForCourseLessons"/>
      <div class="lesson--list">
        <cv-structured-list id="lessons">
          <template v-slot:items>
            <cv-structured-list-item class="lesson-card"
                                     v-for="lesson in courseLessons"
                                     :key="lesson.id">
              <div class="lesson" @click="toLesson(lesson)">
                <div class="title">
                  <h5>{{ lesson.name }}</h5>
                  <cv-tag v-for="problem in lessonProblems(lesson)"
                          :key="problem"
                          kind="red"
                          :label="problem">
                  </cv-tag>
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

<script lang="ts" setup>
import searchByLessons from '@/common/searchByTutorial';
import _ from "lodash";
import type { PropType } from "vue";
import type { CourseModel } from "@/models/CourseModel";
import useLessonStore from "@/stores/modules/lesson";
import { computed, ref } from "vue";
import type { LessonModel } from "@/models/LessonModel";
import { useRouter } from "vue-router";

const props = defineProps({
  course: { type: Object as PropType<CourseModel>, required: true }
})

const router = useRouter();

const lessonStore = useLessonStore();
const searchQueryForCourseLessons = ref("");

const courseLessons = computed((): LessonModel[] => {
  return searchByLessons(searchQueryForCourseLessons.value, props.course.lessons)
      .sort((a, b) => {
        return a.id - b.id;
      });
})

function lessonProblems(lesson: LessonModel) {
  const problems: string[] = [];
  for (const [key, value] of Object.entries(lesson)) {
    if (_.isArrayLike(value) && _.isEmpty(value) && key === 'problems') {
      problems.push(`Empty ${key}`);
    }
  }
  return problems;
}

function toLesson(lesson: LessonModel) {
  router.push({ name: 'LessonView', params: { lessonId: lesson.id.toString() } });
}

</script>

<style lang="stylus" scoped>
.bx--modal-content:focus
  outline none

.no-lessons-title-container
  text-align center

.no-lessons-title
  color var(--cds-text-01)
  margin 1rem

#lessons
  margin-bottom 0

.lesson--list--title
  color var(--cds-text-01)
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
  color var(--cds-text-01)
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
  cursor pointer

  :deep() .bx--tag
    cursor pointer

.icons
  color var(--cds-inverse-02)

:deep() .bx--search-input
  background-color var(--cds-ui-background)
</style>
