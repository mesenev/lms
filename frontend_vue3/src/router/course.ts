import CourseView from '@/views/CourseView.vue';
import CourseEditView from "@/views/managment/CourseEditView.vue";
import CourseRegistrationView from "@/views/CourseRegistrationView.vue";
import CourseCalendarView from "@/views/managment/CourseCalendarView.vue";
import CourseProgressView from "@/views/managment/CourseProgressView.vue";
import SolutionsListView from "@/views/managment/SolutionsListView.vue"

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
    path: 'schedule',
    name: 'course-calendar',
    component: CourseCalendarView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'progress',
    name: 'course-progress',
    component: CourseProgressView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'solutions-list',
    name: 'course-solutions-list',
    component: SolutionsListView,
    props: (route) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
];


export default courseRoutes;
