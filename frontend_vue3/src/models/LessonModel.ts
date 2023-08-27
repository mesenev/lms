import type { BaseModel } from "@/models/BaseModel";
import type { MaterialModel } from '@/models/MaterialModel';
import type { ProblemModel } from '@/models/ProblemModel';
import type { UserProgress } from '@/models/UserProgress';
import type { ExamModel } from "@/models/ExamModel";

export interface LessonModel extends BaseModel {
  course: number;
  description: string;
  deadline: string;
  problems: Array<ProblemModel>;
  exams: Array<ExamModel>;
  materials: Array<MaterialModel>;
  lessonContent?: string;
  progress: Array<UserProgress>;
  is_hidden: boolean;
  scores: Dictionary<number>;
}
