<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1>Список курсов</h1>
      </div>
    </div>
    <div class=" bx--row">
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
            v-model:value.trim="searchValue">
          </cv-search>
          <cv-structured-list>
            <template v-slot:items>
              <cv-structured-list-item
                v-for="course in filterCourses" :key="course.id" class="item">
                <Course :courseProp='course'/>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
        </div>
        <empty-list-component v-else list-of="courses" :text="emptyText"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import useCourseStore from "@/stores/modules/course";
import Course from "@/components/lists/CourseListComponent.vue";
import { computed, onMounted, ref } from "vue";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const courseStore = useCourseStore();
const searchValue = ref("");
const loading = ref(true);
const emptyText = ref('');

onMounted(async () => {
  emptyText.value = 'В данный момент нет доступных курсов.'
  await courseStore.fetchUserCourses();
  loading.value = false;
})

const courses = computed(() => {
  return courseStore.courses;
})

const filterCourses = computed(() => {
  return courses.value.filter(c => {
    return c.name.toLowerCase().includes(searchValue.value.toLowerCase())
  })
})
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

  :deep() .bx--search-input
    background-color var(--cds-ui-background)

.item
  min-height 85px
</style>
