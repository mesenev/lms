import CourseView from '@/views/CourseView.vue';
import CourseEditView from "@/views/managment/CourseEditView.vue";
import CourseRegistrationView from "@/views/CourseRegistrationView.vue";

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
    {
    path: 'edit',
    name: 'course-edit',
    component: CourseEditView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
    {
    path: '/course-registration/:link/',
    name: 'course-registration',
    component: CourseRegistrationView,
    props: (route) => {
      return { linkProp: route.params.link }
    },
  },
];


export default courseRoutes;
