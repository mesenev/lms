export default interface SubmitModel {
  id: number;
  problem: number;
  student: number;
  submit_date: string;
  status: string;
  content?: string;
}
