import type { BaseModel } from "@/models/BaseModel";
import type { LessonModel } from '@/models/LessonModel';
import type { UserModel } from '@/models/UserModel';
import type { AuthorModel } from '@/models/UserModel';
import type { GroupModel } from "@/models/GroupModel.ts";

export interface CourseModel extends BaseModel {
  author: AuthorModel | null;
  cats_id: number | null;
  lessons: Array<LessonModel>;
  completed: boolean;
  description?: string;
  students: Array<UserModel>;
  schedule: number | null;
  de_options: string;
  groups: Array<GroupModel>;
}
