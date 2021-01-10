import UserModel from '@/models/UserModel';

export default interface SubmitModel {
  id: number;
  problem: number;
  student: UserModel;
  content?: string;
  status?: string;
}
