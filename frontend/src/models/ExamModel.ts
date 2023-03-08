import QuestionModel from "@/models/QuestionModel";
import { BaseModel } from "@/models/BaseModel";

export default interface ExamModel extends BaseModel {
  lesson: number;
  description: string | null;
  questions: Array<QuestionModel>;
  max_points: number;
  test_mode: string;
  is_hidden: boolean;
}
