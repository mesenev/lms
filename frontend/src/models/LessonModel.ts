import LessonContent from "@/models/LessonContent";
import ProblemModel from '@/models/ProblemModel';

export default interface LessonModel {
    id: number;
    course: number;
    name: string;
    description: string;
    deadline: string;
    classwork: Array<ProblemModel>;
    homework: Array<ProblemModel>;
    materials: Array<LessonContent>;
    lessonContent?: string;
}
