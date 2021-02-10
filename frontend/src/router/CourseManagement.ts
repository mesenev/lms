import CourseRegistrationView from '@/views/CourseRegistrationView.vue';
import CourseEditView from '@/views/management/CourseEditView.vue';
import LessonEditView from "@/views/management/LessonEditView.vue";
import MaterialEditView from "@/views/management/MaterialEditView.vue";

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
