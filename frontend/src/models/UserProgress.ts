import {Dictionary} from "vue-router/types/router";
import UserModel from "@/models/UserModel";

export default interface UserProgress {
  id: number;
  //marks: Array<number>;
  attendance?: Array<boolean>;
  lesson?: number;
  course?: number;
  lessons?: Dictionary<string>;
  solved: Dictionary<Dictionary<string>>;
  user: UserModel | number;
}
