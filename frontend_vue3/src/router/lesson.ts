import LessonView from "@/views/LessonView.vue";
import ProblemViewLayout from "@/views/ProblemViewLayout.vue"
import problemRoutes from "@/router/problem";
import LessonEditView from "@/views/managment/LessonEditView.vue";
import MaterialView from "@/views/MaterialView.vue";
import MaterialEditView from "@/views/managment/MaterialEditView.vue";

const lessonRoutes = [
    {
        path: '',
        name: 'LessonView',
        component: LessonView,
        props: (route) => {
        const lessonId = Number(route.params.lessonId);
        return { ...route.params, lessonId };
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
        path: 'edit',
        name: 'lesson-edit',
        component: LessonEditView,
        props: (route) => {
          const lessonId = Number.parseInt(route.params.lessonId as string, 10);
          return { lessonId };
        },
    },
    {
    path: 'material/:materialId',
    name: 'MaterialView',
    component: MaterialView,
    props: (route) => {
      const materialId = Number.parseInt(route.params.materialId as string, 10);
      return { materialId, ...route.params };
    },
  },
    {
    path: 'material/:materialId/edit',
    name: 'material-edit',
    component: MaterialEditView,
    props: (route) => {
      const materialId = Number.parseInt(route.params.materialId as string, 10);
      return { materialId };
    },
  },
]


export default lessonRoutes