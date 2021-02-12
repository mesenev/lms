import CourseRegistrationView from '@/views/CourseRegistrationView.vue';
import CourseEditView from '@/views/management/CourseEditView.vue';

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
];


export default routes;
