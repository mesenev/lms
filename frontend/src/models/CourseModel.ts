import Lesson from '@/models/LessonModel.ts';

export default interface CourseModel {
  name: string;
  activeLessons: Array<Lesson>;
  completed: boolean;
}
