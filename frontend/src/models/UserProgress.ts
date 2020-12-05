import Course from '@/models/CourseModel';

export default interface UserProgress {
  course: Course;
  marks: Array<number>;
}
