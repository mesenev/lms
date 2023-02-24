import { BaseModel } from '@/models/BaseModel';
import MaterialModel from '@/models/MaterialModel';
import ProblemModel from '@/models/ProblemModel';
import UserProgress from '@/models/UserProgress';
import { Dictionary } from "vue-router/types/router";
import TestModel from "@/models/TestModel";

export default interface LessonModel extends BaseModel {
  course: number;
  description: string;
  deadline: string;
  problems: Array<ProblemModel>;
  tests: Array<TestModel>;
  materials: Array<MaterialModel>;
  lessonContent?: string;
  progress: Array<UserProgress>;
  is_hidden: boolean;
  scores: Dictionary<number>;
}
