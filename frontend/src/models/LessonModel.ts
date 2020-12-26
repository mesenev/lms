import ProblemModel from '@/models/ProblemModel';
import LessonContent from "@/models/LessonContent";

export default interface LessonModel {
    id: number;
    name: string;
    deadline: string;
    classwork: Array<ProblemModel>;
    homework: Array<ProblemModel>;
    materials: Array<LessonContent>;
}
