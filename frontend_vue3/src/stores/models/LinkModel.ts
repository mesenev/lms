import CourseModel from "@/models/CourseModel";

export default interface LinkModel {
  course: number;
  link: string;
  usages: number;
}
