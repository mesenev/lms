import type { BaseModel } from "@/models/BaseModel.ts";

export interface BaseModel {
  id: number;
  name: string;
}

export interface MaterialModel extends BaseModel {
  lesson: number;
  content_type: string;
  content: string;
  is_teacher_only: boolean;
}
