
export interface SolutionModel {
  id: number;
  exam: number;
  student: number;
  user_answers: Array<{ question_index: number; submitted_answers: Array<string> }>;
  solution_points: number;
  status: string;
  question_verdicts: Dictionary<string>;
}

export const SOLUTION_STATUS = {
  AWAIT_VERIFICATION: 'await',
  VERIFIED: 'verified',
};
