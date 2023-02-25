import { RouteConfig } from "vue-router";
import TestView from "@/views/TestView.vue";
import TestEditView from "@/views/management/TestEditView.vue";

const testRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'TestView',
    component: TestView,
  },
  {
    path: 'edit/',
    name: 'test-edit',
    component: TestEditView,
    props: (route) => {
      const testId = Number.parseInt(route.params.testId as string, 10);
      return { testId, ...route.params };
    },
  },
];

export default testRoutes;
