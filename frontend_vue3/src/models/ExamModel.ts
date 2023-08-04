import type { QuestionModel } from "@/models/QuestionModel";
import type { BaseModel } from "@/models/BaseModel.ts";

export interface ExamModel extends BaseModel {
  lesson: number;
  description: string | null;
  questions: Array<QuestionModel>;
  max_points: number;
  test_mode: string;
  is_hidden: boolean;
}
