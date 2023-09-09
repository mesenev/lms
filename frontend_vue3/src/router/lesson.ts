import LessonView from "@/views/LessonView.vue";

const lessonRoutes = [
    {
        path: '',
        name: 'LessonView',
        component: LessonView,
        props: (route) => {
        const lessonId = Number(route.params.lessonId);
        return { ...route.params, lessonId };
        },
    }
]


export default lessonRoutes