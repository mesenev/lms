// TODO: import as obj from @/views
import CourseView from '@/views/CourseView.vue';
import HomeView from '@/views/HomeView.vue';
import LessonView from '@/views/LessonView.vue';
import MaterialView from '@/views/MaterialView.vue';
import ProblemView from '@/views/ProblemView.vue';
import ProfileView from "@/views/ProfileView.vue";
import RegistrationView from '@/views/RegistrationView.vue';
import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import managementRoutes from './CourseManagement';

Vue.use(VueRouter);
const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    props: true,
  },
  {
    path: '/course/:courseId',
    name: 'CourseView',
    component: CourseView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId, ...route.params };
    },
  },
  {
    path: '/course/:courseId/lesson/:lessonId',
    name: 'LessonView',
    component: LessonView,
    props: (route) => {
      const lessonId = Number.parseInt(route.params.lessonId as string, 10);
      return { lessonId, ...route.params };
    },
  },
  {
    path: '/course/:courseId/lesson/:lessonId/problem/:problemId/:submitId',
    name: 'ProblemView',
    component: ProblemView,
    props: (route) => {
      const problemId = Number.parseInt(route.params.problemId as string, 10);
      const submitIdProp = Number.parseInt(route.params.submitId as string, 10);
      return { problemId, submitIdProp, ...route.params };
    },
  },
  {
    path: '/course/:courseId/lesson/:lessonId/problem/:problemId',
    name: 'ProblemView',
    component: ProblemView,
    props: (route) => {
      const problemId = Number.parseInt(route.params.problemId as string, 10);
      return { problemId, ...route.params };
    },
  },
  {
    path: '/course/:courseId/lesson/:lessonId/material/:materialId',
    name: 'MaterialView',
    component: MaterialView,
    props: (route) => {
      const materialId = Number.parseInt(route.params.materialId as string, 10);
      return { materialId, ...route.params };
    },
  },
  {
    path: '/registration',
    name: 'RegistrationView',
    component: RegistrationView,
  },
  {
    path: '/profile',
    name: 'profile-page',
    component: ProfileView,
  },
  ...managementRoutes,
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
