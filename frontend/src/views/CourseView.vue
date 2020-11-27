<template>
  <div>
    <span>Список курсов</span>

    <ul>
      <li v-for="el in course.activeLessons" :key="el.id">
        <Lesson :lesson="el"/>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import Lesson from '@/components/Lesson.vue';
import CourseModel from '@/models/CourseModel';
import { mainStore } from '@/store';
import { computed, defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'CourseView',
  components: { Lesson },
  props: {
    courseId: {
      type: Number,
      required: true,
    },
    courseProp: {
      type: Object as PropType<CourseModel>,
      required: false,
    },
  },

  setup() {
    const course = computed(() => mainStore.getCourse);
    const fetchCourse = (): void => {
      // const courseFull = store.course;
      // course.activeLessons = courseFull.activeLessons;
      // course.name = courseFull.name;
      // course.completed = courseFull.completed;
    };
    //
    // onMounted(fetchCourse);
    return {
      // store,
      course,
      fetchCourse,
      // lessons: computed((): LessonModel[] => course.activeLessons),
    };
  },

});
</script>

<style scoped>

</style>
