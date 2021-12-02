export default interface SubmitModel {
  id: number;
  lesson: number;
  problem: { id: number; name: string };
  student: number;
  created_at: string;
  status: string;
  cats_submit?: number;
  content?: string;
  de_id: string;
}
