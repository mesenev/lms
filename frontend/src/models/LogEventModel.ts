export const TYPE_CATS = 'cats';
export const TYPE_SUBMIT = 'submit';
export const TYPE_MESSAGE = 'message';
export const TYPE_STATUS_CHANGE = 'status_change';

export default interface LogEventModel  {
  id: number;
  problem: number;
  student: number;
  data: { message?: string; submitId?: number; author: number; thumbnail?: string };
  created_at?: string;
  type: string;
}
