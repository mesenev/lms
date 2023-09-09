import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ResetPasswordView from "@/views/ResetPasswordView.vue";
import ProfileView from "@/views/ProfileView.vue";
import CourseEditView from "@/views/managment/CourseEditView.vue";
import courseRoutes from "@/router/course";
import CourseViewLayout from "@/views/CourseViewLayout.vue";
import lessonRoutes from "@/router/lesson";
import LessonViewLayout from "@/views/LessonViewLayout.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
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
      path: '/reset',
      name: 'ResetPasswordView',
      component: ResetPasswordView,
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
            props: (route) => {
                const lessonId = Number.parseInt(route.params.lessonId as string, 10);
                return {lessonId, ...route.params};
            },
            children: [
                ...lessonRoutes,
            ],
        },
    ],
    },

  ]
})

export default router
