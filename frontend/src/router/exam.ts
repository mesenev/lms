import { RouteConfig } from "vue-router";
import ExamView from "@/views/ExamView.vue";
import ExamEditView from "@/views/management/ExamEditView.vue";

const examRoutes: Array<RouteConfig> = [
  {
    path: '',
    name: 'ExamView',
    component: ExamView,
    props: (route) => {
      const examId = Number.parseInt(route.params.examId as string, 10);
      return { examId, ...route.params };
    },
  },
  {
    path: 'edit/',
    name: 'exam-edit',
    component: ExamEditView,
    props: (route) => {
      const examId = Number.parseInt(route.params.examId as string, 10);
      return { examId, ...route.params };
    },
  },
];

export default examRoutes;
