import LessonModel from '@/models/LessonModel';
import UserModel, { AuthorModel } from '@/models/UserModel';
import { TutorialModel } from '@/models/TutorialModel';

export default interface CourseModel extends TutorialModel {
  author: AuthorModel | null;
  lessons: Array<LessonModel>;
  completed: boolean;
  description?: string;
  students: Array<UserModel>;
}
