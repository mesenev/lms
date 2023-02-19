import AnswerModel from "@/models/AnswerModel";

export default interface QuestionModel {
  id: number;
  test: number;
  question: string;
  description: string | null;
  answer_type: string;
  answer: AnswerModel;
  attachment_file: string | null;
  points: number;
}
