import CourseModel from "@/models/CourseModel";
import PairModel from "@/models/UserProgress";

export default interface User {
  id: number;
  name: string;
  course: PairModel;
}
