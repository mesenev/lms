import { BaseModel } from '@/models/BaseModel';
import LessonModel from '@/models/LessonModel';
import UserModel, { AuthorModel } from '@/models/UserModel';

export default interface CourseModel extends BaseModel {
  author: AuthorModel | null;
  lessons: Array<LessonModel>;
  completed: boolean;
  description?: string;
  students: Array<UserModel>;
  schedule: number | null;
}
