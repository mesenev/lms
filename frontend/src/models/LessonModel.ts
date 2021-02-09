import MaterialModel from '@/models/MaterialModel';
import ProblemModel from '@/models/ProblemModel';
import UserProgress from '@/models/UserProgress';
import { TutorialModel } from '@/models/TutorialModel';

export default interface LessonModel extends TutorialModel {
  course: number;
  description: string;
  deadline: string;
  problems: Array<ProblemModel>;
  materials: Array<MaterialModel>;
  lessonContent?: string;
  progress: Array<UserProgress>;
}
