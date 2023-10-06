import type { CourseModel } from "@/models/CourseModel";

export interface LinkModel {
  course: number;
  link: string;
  usages: number;
}
