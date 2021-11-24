import { BaseModel } from '@/models/BaseModel';
import UserModel from "@/models/UserModel";


export default interface LogEventModel extends BaseModel {
  type: string;
  text: string;
  sender: UserModel;
  submitId?: number;
}
