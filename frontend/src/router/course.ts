import CourseView from '@/views/CourseView.vue';
import CourseEditView from "@/views/managment/CourseEditView.vue";
import CourseCalendarView from "@/views/managment/CourseCalendarView.vue";
import CourseProgressView from "@/views/managment/CourseProgressView.vue";
import SolutionsListView from "@/views/managment/SolutionsListView.vue"
import CourseGroupsView from "@/views/managment/CourseGroupsView.vue";

const courseRoutes = [
  {
    path: '',
    name: 'CourseView',
    component: CourseView,
    props: (route: any) => {
      const courseId = Number(route.params.courseId);
      return { courseId };
    },
  },
  {
    path: 'groups',
    name: 'course-groups',
    component: CourseGroupsView,
    props: (route: any) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'edit',
    name: 'course-edit',
    component: CourseEditView,
    props: (route: any) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'schedule',
    name: 'course-calendar',
    component: CourseCalendarView,
    props: (route: any) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'progress',
    name: 'course-progress',
    component: CourseProgressView,
    props: (route: any) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
  {
    path: 'solutions-list',
    name: 'course-solutions-list',
    component: SolutionsListView,
    props: (route: any) => {
      const courseId = Number.parseInt(route.params.courseId as string, 10);
      return { courseId };
    },
  },
];


export default courseRoutes;
