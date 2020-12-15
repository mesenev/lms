import LessonModel from '@/models/LessonModel';

export default interface CourseModel {
  id: number;
  name: string;
  lessons: Array<LessonModel>;
  completed: boolean;
  description?: string;
}
