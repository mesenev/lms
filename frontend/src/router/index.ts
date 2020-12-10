import CourseView from '@/views/CourseView.vue';
import HomeView from '@/views/HomeView.vue';
import LessonView from '@/views/LessonView.vue';
import ProblemView from '@/views/ProblemView.vue';
import RegistrationView from '@/views/RegistrationView.vue';
import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';

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
      return { courseId };
    },
  },
  {
    path: '/lesson/:lessonId',
    name: 'LessonView',
    component: LessonView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.problemId as string, 10);
      return { courseId };
    },
  },
  {
    path: '/problem/:problemId',
    name: 'ProblemView',
    component: ProblemView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.problemId as string, 10);
      return { courseId };
    },
  },
  {
    path: '/registration',
    name: 'RegistrationView',
    component: RegistrationView,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
