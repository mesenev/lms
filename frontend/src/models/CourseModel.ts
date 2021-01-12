import LessonModel from '@/models/LessonModel';
import UserModel from '@/models/UserModel';

export default interface CourseModel {
  id: number;
  name: string;
  author: UserModel|null;
  lessons: Array<LessonModel>;
  completed: boolean;
  description?: string;
  students: Array<UserModel>;
}
