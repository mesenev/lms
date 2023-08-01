import { BaseModel } from '@/models/BaseModel';
import LessonModel from '@/models/LessonModel';

export interface ScheduleElement {
  date: number;
  lesson_id: number;
  isSelected: boolean;
}

export default interface CourseScheduleModel extends BaseModel {
  lessons: Array<ScheduleElement>;
  course: number;
  start_date: string;
  week_schedule: Record<string, string | null>;
}

