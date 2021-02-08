import CourseModel from "@/models/CourseModel";
import LessonModel from "@/models/LessonModel";
import ProblemModel from "@/models/ProblemModel";
import LessonContent from "@/models/LessonContent";

declare module '@carbon/vue/src/index';
declare module '@carbon/*';
declare module '*.scss';

declare module '*.vue' {
  import type { DefineComponent } from 'vue';

  const component: DefineComponent<{}, {}, any>;
  export default component;
}

type Model = CourseModel | LessonModel | ProblemModel | LessonContent;
