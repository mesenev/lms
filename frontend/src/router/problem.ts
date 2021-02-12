import ProblemView from '@/views/ProblemView.vue';
import { RouteConfig } from 'vue-router';

const problemRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'ProblemView',
    component: ProblemView,
  },
  {
    path: 'submit/:submitId',
    name: 'ProblemViewWithSubmit',
    component: ProblemView,
    props: (route) => {
      const submitIdProp = Number.parseInt(route.params.submitId as string, 10);
      return { submitIdProp, ...route.params };
    },
  },
];


export default problemRoutes;
