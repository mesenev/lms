import { BaseModel } from '@/models/BaseModel';
import MaterialModel from '@/models/MaterialModel';
import ProblemModel from '@/models/ProblemModel';
import UserProgress from '@/models/UserProgress';

export default interface LessonModel extends BaseModel {
  course: number;
  description: string;
  deadline: string;
  problems: Array<ProblemModel>;
  materials: Array<MaterialModel>;
  lessonContent?: string;
  progress: Array<UserProgress>;
  is_hidden: boolean;
}
