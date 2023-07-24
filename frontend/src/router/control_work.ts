import { RouteConfig } from "vue-router";
import ControlWorkView from "@/views/ControlWorkView.vue";
import LessonEditView from "@/views/management/LessonEditView.vue";
import ProblemViewLayout from "@/views/ProblemViewLayout.vue";
import problemRoutes from "@/router/problem";

const controlWorkRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'ControlWorkView',
    component: ControlWorkView,
    props: (route) => {
      const controlWorkId = Number(route.params.controlWorkId);
      return { ...route.params, controlWorkId, lessonId: controlWorkId };
    },
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
    path: 'edit/',
    name: 'control-work-edit',
    component: LessonEditView,
    props: (route) => {
      const controlWorkId = Number.parseInt(route.params.controlWorkId as string, 10);
      return { controlWorkId, is_control_work: true, lessonId: controlWorkId, ...route.params };
    },
  },
];

export default controlWorkRoutes;
