import CourseCalendarView from '@/views/management/CourseCalendarView.vue';
import SolutionsListView from '@/views/management/SolutionsListView.vue';
import { RouteConfig } from 'vue-router';
import CourseProgressView from '@/views/management/CourseProgressView.vue';
import CourseEditView from '@/views/management/CourseEditView.vue';
import ProblemEditView from '@/views/management/ProblemEditView.vue';

// TODO: consult is it optimal (I bet it's not)
const routes: Array<RouteConfig> = [
  {
    path: '/course/:courseId/progress',
    name: 'course-progress',
    component: CourseProgressView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: '/course/:courseId/solutions-list',
    name: 'course-solutions-list',
    component: SolutionsListView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: '/course/:courseId/schedule',
    name: 'course-calendar',
    component: CourseCalendarView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: '/course/:courseId/edit',
    name: 'course-edit',
    component: CourseEditView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: '/course/:problemId/edit',
    name: 'problem-edit',
    component: ProblemEditView,
    props: (route) => {
      const problemId = Number.parseInt(route.params.problemId as string, 10);
      return { problemId };
    },
  },
];


export default routes;
