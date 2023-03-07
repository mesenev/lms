export default interface SolutionModel {
  id: number;
  exam: number;
  student: number;
  user_answers: Array<{question_index: number; submitted_answers: Array<string>}>;
  score: number;
  status: string;
  correct_questions_indexes: Array<number>;
}

export const SOLUTION_STATUS = {
  AWAIT_VERIFICATION: 'await',
  VERIFIED: 'verified',
}
