import { BaseModel } from '@/models/BaseModel';
import UserModel from "@/models/UserModel";


export default interface MessageModel extends BaseModel {
  text: string;
  sender: UserModel;
  isSubmit: boolean;
  submitId?: number;
  lessonId: number;
  courseId: number;
}
