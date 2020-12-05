import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import { Module, VuexModule } from 'vuex-module-decorators';

@Module({ name: 'MainStorage' })
export default class MainStorage extends VuexModule {
  private course: CourseModel = {
    id: 8,
    lessons: [{ id: 1, name: 'Урок 1' }, { id: 2, name: 'Урок 2' }] as Array<LessonModel>,
    completed: false,
    name: 'Алгоритмы и структуры данных (введение)',
  }

  private courses: Array<CourseModel> = [this.course, this.course, this.course, this.course]

  private problems: Array<ProblemModel> = [{
    id: 1,
    name: '123',
    description: '456',
    completed: true,
  } as ProblemModel];

  get getCourse() {
    return this.course;
  }

  get getProblems() {
    return this.problems;
  }

  get getCourses() {
    return this.courses;
  }
}
