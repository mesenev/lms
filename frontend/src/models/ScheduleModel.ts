import type { BaseModel } from '@/models/BaseModel';

export interface ScheduleElement {
  date: number;
  lesson_id: number;
  isSelected: boolean;
}

export interface CourseScheduleModel extends BaseModel {
  lessons: Array<ScheduleElement>;
  course: number;
  start_date: string;
  week_schedule: Record<string, string | null>;
}

