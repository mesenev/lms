import LessonView from "@/views/LessonView.vue";
import ProblemViewLayout from "@/views/ProblemViewLayout.vue"
import problemRoutes from "@/router/problem";
import LessonEditView from "@/views/managment/LessonEditView.vue";

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
]


export default lessonRoutes