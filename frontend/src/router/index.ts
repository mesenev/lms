// TODO: import as obj from @/views
import courseRoutes from '@/router/course';
import lessonRoutes from '@/router/lesson';
import CourseViewLayout from '@/views/CourseViewLayout.vue';
import HomeView from '@/views/HomeView.vue';
import LessonViewLayout from '@/views/LessonViewLayout.vue';
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
  },
  {
    path: '/course/:courseId',
    component: CourseViewLayout,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId, ...route.params };
    },
    children: [
      ...courseRoutes,
      {
        path: 'lesson/:lessonId',
        component: LessonViewLayout,
        children: [
          ...lessonRoutes,
        ],
        props: (route) => {
          const lessonId = Number.parseInt(route.params.lessonId as string, 10);
          return { lessonId, ...route.params };
        },
      },
    ],
  },
  {
    path: '/registration',
    name: 'RegistrationView',
    component: RegistrationView,
  },
  {
    path: '/profile/:userId',
    name: 'profile-page',
    component: ProfileView,
    props: (route) => {
      const userId = Number.parseInt(route.params.userId as string, 10);
      return { userId, ...route.params };
    },
  },
  ...managementRoutes,
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
