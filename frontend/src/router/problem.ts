import ProblemView from '@/views/ProblemView.vue';
import ProblemEditView from "@/views/managment/ProblemEditView.vue";

const problemRoutes = [
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
  {
    path: 'edit/',
    name: 'problem-edit',
    component: ProblemEditView,
    props: (route) => {
      const problemId = Number.parseInt(route.params.submitId as string, 10);
      return { problemId, ...route.params };
    },
  },
];


export default problemRoutes;
