import CourseView from '@/views/CourseView.vue';
import { RouteConfig } from 'vue-router';

const courseRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'CourseView',
    component: CourseView,
  },
];


export default courseRoutes;
