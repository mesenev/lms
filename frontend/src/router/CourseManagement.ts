import CourseRegistrationView from '@/views/CourseRegistrationView.vue';
import CourseCalendarView from '@/views/management/CourseCalendarView.vue';
import CourseEditView from '@/views/management/CourseEditView.vue';
import CourseProgressView from '@/views/management/CourseProgressView.vue';
import LessonEditView from "@/views/management/LessonEditView.vue";
import LessonProgressView from '@/views/management/LessonProgressView.vue'
import MaterialEditView from "@/views/management/MaterialEditView.vue";
import ProblemEditView from '@/views/management/ProblemEditView.vue';
import SolutionsListView from '@/views/management/SolutionsListView.vue';

import { RouteConfig } from 'vue-router';

// TODO: consult is it optimal (I bet it's not)

const routes: Array<RouteConfig> = [
  {
    path: '/course-registration/:link/',
    name: 'course-registration',
    component: CourseRegistrationView,
    props: (route) => {
      return { linkProp: route.params.link }
    },
  },
  {
    path: '/course-add',
    name: 'course-add',
    component: CourseEditView,
    props: () => {
      return { courseId: null };
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
    path: '/course/:courseId/lesson/:lessonId/progress',
    name: 'lesson-progress',
    component: LessonProgressView,
    props: (route) => {
      const lessonId = Number.parseInt(route.params.lessonId as string, 10);
      return { lessonId };
    },
  },
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
    path: '/course/:courseId/lesson/:lessonId/problem/:problemId/edit',
    name: 'problem-edit',
    component: ProblemEditView,
    props: (route) => {
      const problemId = Number.parseInt(route.params.problemId as string, 10);
      return { problemId };
    },
  },
  {
    path: '/course/:courseId/lesson/:lessonId/edit',
    name: 'lesson-edit',
    component: LessonEditView,
    props: (route) => {
      const lessonId = Number.parseInt(route.params.lessonId as string, 10);
      return { lessonId };
    },
  },
  {
    path: '/course/:courseId/lesson/:lessonId/material/:materialId/edit',
    name: 'material-edit',
    component: MaterialEditView,
    props: (route) => {
      const materialId = Number.parseInt(route.params.materialId as string, 10);
      return { materialId };
    },
  },
];


export default routes;
