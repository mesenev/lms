export default interface AnswerModel {
  id: number;
  file_url: FormData | null;
  text: string | null;
  is_correct: boolean;
}

export const ANSWER_TYPE = {
  STRING: 'Short',
  TEXT: 'Long',
  RADIO: 'Radio',
  CHECKBOX: 'Checkbox',
  FILE: 'File',
};
