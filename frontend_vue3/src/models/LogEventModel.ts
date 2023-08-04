export const TYPE_MESSAGE = 'message';
export const TYPE_CATS_ANSWER = 'cats_answer';
export const TYPE_STATUS_CHANGE = 'status_change';
export const TYPE_SUBMIT = 'submit';
export const TYPE_CATS_SUBMIT = 'cats_submit';
export const TYPE_CATS_ERROR = 'cats_error';


export interface LogEventModel {
  id: number;
  problem: number;
  student: number;
  data: { message?: string; thumbnail?: string };
  type: string;
  author?: number;
  created_at?: string;
  submit?: number;
}
