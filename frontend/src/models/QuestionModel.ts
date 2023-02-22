export default interface QuestionModel {
  id: number;
  test: number;
  question: string;
  description: string | null;
  answer_type: string;
  answers: Array<string>;
  correct_answers: Array<string>;
  attachment_file: string | null;
  points: number;
}

export const ANSWER_TYPE = {
  INPUT: 'input',
  TEXT_FIELD: 'text',
  RADIO: 'radio',
  CHECKBOXES: 'checkbox',
}
