import { RouteConfig } from "vue-router";
import TestView from "@/views/TestView.vue";

const testRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'TestView',
    component: TestView,
  },
]

export default testRoutes;
