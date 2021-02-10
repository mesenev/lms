import problemRoutes from '@/router/problem';
import LessonView from '@/views/LessonView.vue';
import LessonProgressView from '@/views/management/LessonProgressView.vue';
import MaterialView from '@/views/MaterialView.vue';
import ProblemViewLayout from '@/views/ProblemViewLayout.vue';
import { RouteConfig } from 'vue-router';

const lessonRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'LessonView',
    component: LessonView,
  },
  {
    path: 'problem/:problemId',
    component: ProblemViewLayout,
    children: [
      ...problemRoutes,
    ],
    props: (route) => {
      const problemId = Number.parseInt(route.params.problemId as string, 10);
      return { problemId, ...route.params };
    },
  },
  {
    path: 'material/:materialId',
    name: 'MaterialView',
    component: MaterialView,
    props: (route) => {
      const materialId = Number.parseInt(route.params.materialId as string, 10);
      return { materialId, ...route.params };
    },
  },

  {
    path: 'progress',
    name: 'lesson-progress',
    component: LessonProgressView,
    props: (route) => {
      const lessonId = Number.parseInt(route.params.lessonId as string, 10);
      return { lessonId };
    },
  },
];


export default lessonRoutes;
