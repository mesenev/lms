import ProblemModel from '@/models/ProblemModel';
import UserModel from '@/models/UserModel';

export default interface SubmitModel {
  id: number;
  problem: ProblemModel;
  student: UserModel;
  content?: string;
  status?: string;
}
