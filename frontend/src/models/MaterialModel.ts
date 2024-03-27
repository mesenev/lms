import type { BaseModel } from "@/models/BaseModel";

export interface MaterialModel extends BaseModel {
  lesson: number;
  content_type: string;
  content: string;
  is_teacher_only: boolean;
}
