import CourseView from '@/views/CourseView.vue';
import CourseCalendarView from '@/views/management/CourseCalendarView.vue';
import CourseEditView from '@/views/management/CourseEditView.vue';
import CourseProgressView from '@/views/management/CourseProgressView.vue';
import SolutionsListView from '@/views/management/SolutionsListView.vue';
import { RouteConfig } from 'vue-router';

const courseRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'CourseView',
    component: CourseView,
  },
  {
    path: 'progress',
    name: 'course-progress',
    component: CourseProgressView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'edit',
    name: 'course-edit',
    component: CourseEditView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'solutions-list',
    name: 'course-solutions-list',
    component: SolutionsListView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'schedule',
    name: 'course-calendar',
    component: CourseCalendarView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },

];


export default courseRoutes;
