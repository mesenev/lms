<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1 v-if="!loading && lesson" class=""> Урок: {{ lesson.name }} </h1>
        <cv-skeleton-text v-else :heading="true" class="main-title" width="'35%'"/>
        <div v-if="!loading && lesson" class="lesson-info">
          <span>
            Дедлайн: {{ lesson.deadline }}
          </span>
          <div v-if="isStaff">
            <cv-button-skeleton v-if="changingVisibility || !lesson" kind="ghost"/>
            <cv-button v-else
                       class="lesson-hide-button"
                       :icon="hiddenIcon"
                       kind="ghost"
                       @click="changeLessonVisibility">
              {{ (lesson.is_hidden) ? "Открыть урок" : "Скрыть урок" }}
            </cv-button>
          </div>
        </div>
        <cv-skeleton-text v-else width="'35%'"/>
        <div class="description-container">
          <span v-if="!loading && lesson" class="lesson-description">
             {{ lesson.description }}
          </span>
          <cv-skeleton-text v-else width="'35%'"/>
        </div>
      </div>
    </div>
    <div class="bx--row lesson-content">
      <div :class="(isProblemsEmpty) ? 'empty-items bx--col-lg-6 bx--col-md-6'
      : 'items bx--col-lg-6 bx--col-md-6'">
        <div v-if="!loading">
          <div v-if="isProblemsEmpty">
            <empty-list-component list-of="problems" :text="emptyProblemsText"/>
          </div>
          <div v-else class="content-tasks-problems">
            <div v-if="classwork.length > 0" class="classwork">
              <h4 class="classwork-title title">Классная работа</h4>
              <problem-list-component :task-list="classwork"></problem-list-component>
            </div>
            <div v-if="homework.length > 0" class="homework">
              <h4 class="homework-title title">Домашняя работа</h4>
              <problem-list-component :task-list="homework"/>
            </div>
            <div v-if="extrawork.length > 0" class="extrawork">
              <h4 class="classwork-title title">Дополнительные задания</h4>
              <problem-list-component :task-list="extrawork"/>
            </div>
            <div v-if="exams.length > 0" class="tests">
              <h4 class="classwork-title title">Тесты</h4>
              <!-- <exam-list-component :exams-list="exams"/> -->
            </div>
          </div>
        </div>
        <cv-skeleton-text :paragraph="true" :line-count="5" v-else/>
      </div>
      <div
          :class="(!loading && isMaterialsEmpty) ? ('bx--col-lg-4 bx--col-md-4 content-info-empty')
         : ('bx--col-lg-4 bx--col-md-4 content-info')">
        <div v-if="!loading">
          <div v-if="isMaterialsEmpty" class="content-info-empty">
            <empty-list-component :text="emptyMaterialsText" list-of="materials"/>
          </div>
          <div v-else>
            <h2 class="content-info-title">Материалы</h2>
            <div class="content-info-materials" v-if="!loading">
              <cv-structured-list class="list">
                <template v-slot:items>
                  <cv-structured-list-item
                      v-for="material in studentMaterials"
                      :key="material.id">
                    <material-list-component :material-prop="material"
                                             :show-visibility="true"
                                             :is-staff="isStaff"/>
                  </cv-structured-list-item>
                  <template v-if="isStaff">
                    <cv-structured-list-item
                        v-for="material in teacherMaterials"
                        :key="material.id">
                      <material-list-component :material-prop="material"
                                               :show-visibility="true"
                                               :is-staff="isStaff"/>
                    </cv-structured-list-item>
                  </template>
                </template>
              </cv-structured-list>
            </div>
          </div>
        </div>
        <cv-skeleton-text :paragraph="true" :line-count="5" v-else/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { MaterialModel } from '@/models/MaterialModel';
import type { ProblemModel } from '@/models/ProblemModel';
import useLessonStore from '@/stores/modules/lesson';
import useMaterialStore from '@/stores/modules/material';
import useProblemStore from '@/stores/modules/problem';
import useUserStore from '@/stores/modules/user';
import useExamStore from '@/stores/modules/exam';
import viewOff from '@carbon/icons-vue/es/view--off/32';
import view from '@carbon/icons-vue/es/view/32';
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";
import type { ExamModel } from "@/models/ExamModel";
import { ref, Ref, onMounted, computed } from "vue";
import CvStructuredList from "@/components/CvStructuredList/CvStructuredList.vue";
import CvStructuredListItem from "@/components/CvStructuredList/CvStructuredListItem.vue";
import MaterialListComponent from "@/components/lists/MaterialListComponent.vue";

const props = defineProps({ lessonId: { type: Number, required: true } })

const lessonStore = useLessonStore();
const problemStore = useProblemStore();
const userStore = useUserStore();
const materialStore = useMaterialStore();
const examStore = useExamStore();
const loading: Ref<boolean> = ref(true);
const changingVisibility: Ref<boolean> = ref(false);
const emptyProblemsText: Ref<string> = ref('');
const emptyMaterialsText: Ref<string> = ref('');

onMounted(async () => {
  emptyProblemsText.value = 'В данный момент нет доступных задач.';
  emptyMaterialsText.value = 'Похоже, доступные материалы отсутствуют.';
  await problemStore.fetchProblemsByLessonId(props.lessonId);
  await materialStore.fetchMaterialsByLessonId(props.lessonId);
  await examStore.fetchExamsByLessonId(props.lessonId);
  loading.value = false;
})

const isProblemsEmpty = computed(() => {
  return (problems.value ?? []).length === 0 && (exams.value ?? []).length === 0;
})

const isMaterialsEmpty = computed(() => {
  if (!isStaff.value)
    return !studentMaterials.value.length;
  return !materialStore.materials[props.lessonId].length;
})

const isStaff = computed((): boolean => {
  return userStore.user.staff_for.includes(Number(lesson.value?.course));
})

const hiddenIcon = computed(() => {
  return (lesson.value?.is_hidden) ? viewOff : view;
})

//TODO: move materials in separate component
const studentMaterials = computed((): Array<MaterialModel> => {
  if (lesson.value)
    return materialStore.materials[props.lessonId].filter(el => !el.is_teacher_only)
        .sort((a, b) => a.id - b.id);
  return [];
})

const teacherMaterials = computed((): Array<MaterialModel> => {
  if (lesson.value)
    return materialStore.materials[props.lessonId].filter(el => el.is_teacher_only)
        .sort((a, b) => a.id - b.id);
  return [];
})

const lesson = computed(() => {
  return lessonStore.currentLesson;
})

const problems = computed(() => {
  return problemStore.problemsByLesson[props.lessonId];
})

const classwork = computed((): Array<ProblemModel> => {
  return problemStore.problemsByLesson[props.lessonId].filter(x => x.type === 'CW');
})

const homework = computed((): Array<ProblemModel> => {
  return problemStore.problemsByLesson[props.lessonId].filter(x => x.type === 'HW');
})

const extrawork = computed((): Array<ProblemModel> => {
  return problemStore.problemsByLesson[props.lessonId].filter(x => x.type === 'EX');
})

const exams = computed((): Array<ExamModel> => {
  return examStore.examsByLesson[props.lessonId];
})

async function changeLessonVisibility() {
  changingVisibility.value = true;
  await lessonStore.patchLesson(
      { id: props.lessonId, is_hidden: !lesson.value?.is_hidden },
  );
  changingVisibility.value = false;
}

</script>

<style scoped lang="stylus">
.lesson-info
  display flex
  flex-direction row
  align-items center
  padding-left 1rem
  font-weight var(--cds-display-02-font-weight)
  margin-top 1rem
  color var(--cds-text-02)
  gap 2rem

.description-container
  max-width 70%
  word-break break-word
  color var(--cds-text-02)
  font-weight var(--cds-display-02-font-weight)
  margin-top var(--cds-spacing-03)
  padding-left 1rem

.lesson-hide-button
  margin-left -1rem

.accordion
  height 100%

.no-problems
  margin 1rem

.content-info-materials
  margin-bottom 1rem


.content-tasks-title
  margin 1rem

.less
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.add
  background-color var(--cds-ui-02)

.back-to-lesson
  background-color transparent
  border 1px solid var(--cds-text-01)
  cursor pointer
  user-select none

.content
  margin-top 1rem

  &-info
    height 100%

    &-title
      color var(--cds-text-01)

    .list
      margin 1rem 0

  &-tasks, &-info
    background-color var(--cds-ui-01)
    padding 1rem

  /deep/ .bx--accordion__heading
    align-items center


.classwork, .homework, .extrawork
  margin-bottom 1rem

  &-title
    font-weight bold
    color var(--cds-text-01)
    padding-left 1rem
    margin 1rem 0

.empty-items
  background-color var(--cds-ui-01)
  padding-top 1rem
  margin-bottom 1rem
  margin-right 1rem
  padding-bottom 1rem

.items
  background-color: var(--cds-ui-01)
  padding-top 1rem
  padding-bottom 1rem
  margin-bottom 1rem
  margin-right 1rem
</style>
