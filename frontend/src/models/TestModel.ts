import QuestionModel from "@/models/QuestionModel";
import { BaseModel } from "@/models/BaseModel";

export default interface TestModel extends BaseModel {
  description: string | null;
  questions: Array<QuestionModel>;
  points: number;
  test_mode: string;
  is_hidden: boolean;
}
