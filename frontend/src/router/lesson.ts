import LessonView from '@/views/LessonView.vue';
import { RouteConfig } from 'vue-router';

const lessonRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'LessonView',
    component: LessonView,
  },
];


export default lessonRoutes;
