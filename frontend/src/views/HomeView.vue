<template>
  <div class="home-view bx--grid">
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
        <div v-else-if="courses.length" class="courses-panel">
          <cv-search
            label="label"
            placeholder="Поиск"
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
        <div v-else class="courses-panel courses-panel--empty">
          <empty-list-component list-of="courses" :text="emptyText"/>
        </div>
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

.home-view
  width 100%

.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.empty-items
  padding 0
  background transparent

.items
  padding 0
  min-height 0
  background transparent

  .bx--structured-list-thead
    display none

.courses-panel
  min-height 28rem
  padding 1rem
  border-radius 8px
  background rgba(118, 118, 118, .34)
  box-shadow 0 18px 40px rgba(0, 0, 0, .08)
  backdrop-filter blur(2px)

.courses-panel--empty
  display flex
  align-items flex-start

.courses-panel :deep(.bx--search)
  margin-bottom 1.5rem

.courses-panel :deep(.bx--search-input)
  height 1.55rem
  border 1px solid #9f9f9f
  border-radius 5px
  background rgba(255, 255, 255, .88)
  color #222

.courses-panel :deep(.bx--search-input::placeholder)
  color #b5b5b5

.courses-panel :deep(.bx--structured-list)
  margin-bottom 0
  background transparent

.courses-panel :deep(.bx--structured-list-row)
  border 0

.courses-panel :deep(.list-element)
  min-height 3rem
  align-items center
  margin-bottom .45rem
  padding .45rem .9rem
  border-radius 5px
  background rgba(255, 255, 255, .78)
  color #161616
  box-shadow 0 1px 0 rgba(255, 255, 255, .4) inset

.courses-panel :deep(.list-element:hover)
  background rgba(255, 255, 255, .9)

.courses-panel :deep(.list-element--title)
  margin 0
  color #111
  font-size .95rem
  font-weight 700

.courses-panel :deep(.list-element--info)
  color #353535
  font-size .86rem

.item
  min-height auto
</style>
