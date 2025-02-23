export const ANSWER_TYPE = {
  INPUT: 'input',
  TEXT_FIELD: 'text',
  RADIO: 'radio',
  CHECKBOXES: 'checkbox',
  CODE: 'code',
} as const;

export const LANGUAGE_TYPE = {
  PYTHON: 'python',
  C_CPP: 'C/C++',
} as const;
export type AnswerType = typeof ANSWER_TYPE[keyof typeof ANSWER_TYPE];
export type LanguageType = typeof LANGUAGE_TYPE[keyof typeof LANGUAGE_TYPE];

export interface QuestionModel {
  index: number;
  text: string;
  description: string | null;
  answer_type: AnswerType;
  all_answers: Array<string>;
  correct_answers: Array<string>;
  attachment_url: string | null;
  points: number;
  code?: string;
  language_type?: LanguageType;
  test_cases?: Array<{test_input: string; test_output: string}>;
}


