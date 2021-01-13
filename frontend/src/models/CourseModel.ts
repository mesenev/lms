import LessonModel from '@/models/LessonModel';
import UserModel, { AuthorModel } from '@/models/UserModel';

export default interface CourseModel {
  id: number;
  name: string;
  author: AuthorModel|null;
  lessons: Array<LessonModel>;
  completed: boolean;
  description?: string;
  students: Array<UserModel>;
}
