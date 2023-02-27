export default interface QuestionModel {
  text: string;
  description: string | null;
  answer_type: string;
  all_answers: Array<string>;
  correct_answers: Array<string>;
  attachment_url: string | null;
  points: number;
}

export const ANSWER_TYPE = {
  INPUT: 'input',
  TEXT_FIELD: 'text',
  RADIO: 'radio',
  CHECKBOXES: 'checkbox',
}
