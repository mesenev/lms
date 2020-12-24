import ProblemModel from '@/models/ProblemModel';

export default interface LessonModel {
    id: number;
    name: string;
    deadline: string;
    classwork: Array<ProblemModel>;
    homework: Array<ProblemModel>;
    lessonContent?: string;
}
