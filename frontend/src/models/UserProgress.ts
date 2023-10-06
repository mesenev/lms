import type { UserModel } from "@/models/UserModel";

export interface UserProgress {
  id: number;
  attendance: boolean;
  lesson: number;
  progress?: Dictionary<string>;
  solved: Dictionary<Dictionary<string>>;
  user: number;
}
