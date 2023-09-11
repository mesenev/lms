import LessonView from "@/views/LessonView.vue";
import ProblemViewLayout from "@/views/ProblemViewLayout.vue"
import problemRoutes from "@/router/problem";

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
]


export default lessonRoutes