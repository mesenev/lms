import {Dictionary} from "vue-router/types/router";
import UserModel from "@/models/UserModel";

export default interface UserProgress {
  id: number;
  attendance: boolean;
  lesson: number;
  progress?: Dictionary<string>;
  solved: Dictionary<Dictionary<string>>;
  user: number;
}
