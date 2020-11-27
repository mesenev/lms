import LessonModel from '@/models/LessonModel.ts';

export default interface CourseModel {
  name: string;
  activeLessons: Array<LessonModel>;
  completed: boolean;
}
