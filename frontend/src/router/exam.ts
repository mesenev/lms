import ExamView from "@/views/ExamView.vue";
import ExamEditView from "@/views/managment/ExamEditView.vue";


const examRoutes = [
  {
    path: '',
    name: 'ExamView',
    component: ExamView,
  },
  {
    path: 'solution/:solutionId',
    name: 'ExamViewWithSolution',
    component: ExamView,
    props: (route: any) => {
      const solutionId = Number.parseInt(route.params.solutionId as string, 10);
      return { solutionId, ...route.params };
    },
  },
  {
    path: 'edit/',
    name: 'exam-edit',
    component: ExamEditView,
    props: (route: any) => {
      const examId = Number.parseInt(route.params.examId as string, 10);
      return { examId, ...route.params };
    },
  },
];

export default examRoutes;
