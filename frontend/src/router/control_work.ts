import { RouteConfig } from "vue-router";
import ControlWorkView from "@/views/ControlWorkView.vue";
import LessonEditView from "@/views/management/LessonEditView.vue";

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
  // {
  //   path: 'solution/:solutionId',
  //   name: 'ExamViewWithSolution',
  //   component: ControlWorkView,
  //   props: (route) => {
  //     const solutionId = Number.parseInt(route.params.solutionId as string, 10);
  //     return { solutionId, ...route.params };
  //   },
  // },
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
