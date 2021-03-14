import {Dictionary} from "vue-router/types/router";
import UserModel from "@/models/UserModel";

export default interface UserProgress {
  id: number;
  //name: string;
  //marks: Array<number>;
  //attendance: Array<boolean>;
  lesson: number;
  solved: Dictionary<string>;
  user: UserModel;
}
