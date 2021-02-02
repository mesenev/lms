import LessonContent from "@/models/LessonContent";
import ProblemModel from '@/models/ProblemModel';
import UserProgress from "@/models/UserProgress";

export default interface LessonModel {
    id: number;
    course: number;
    name: string;
    description: string;
    deadline: string;
    problems: Array<ProblemModel>;
    materials: Array<LessonContent>;
    lessonContent?: string;
    progress: Array<UserProgress>;
}
