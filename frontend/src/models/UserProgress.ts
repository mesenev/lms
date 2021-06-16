import {Dictionary} from "vue-router/types/router";
import UserModel from "@/models/UserModel";

export default interface UserProgress {
  id: number;
  attendance?: Array<boolean>;
  lesson?: number;
  course?: number;
  progress?: Dictionary<string>;
  solved: Dictionary<Dictionary<string>>;
  user?: UserModel | any;
}
