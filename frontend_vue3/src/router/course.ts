import CourseView from '@/views/CourseView.vue';

const courseRoutes = [
  {
    path: '',
    name: 'CourseView',
    component: CourseView,
    props: (route) => {
      const courseId = Number(route.params.courseId);
      return { courseId };
    },
  },
];


export default courseRoutes;
