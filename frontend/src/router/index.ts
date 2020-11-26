import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Home from '../views/Home.vue';
import CourseView from '../views/CourseView.vue';
import LessonView from '../views/LessonView.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/course/1',
    name: 'Course',
    component: CourseView,
  },
  {
    path: '/course/1/lesson/1',
    name: 'Lesson',
    component: LessonView,
  },
  // {
  //   path: '/administration-panel',
  //   name: 'AdministrationPanel',
  //   component: () => import('../views/AdminIndex.vue'),
  // },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
