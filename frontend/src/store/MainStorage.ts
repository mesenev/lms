import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import { Module, VuexModule } from 'vuex-module-decorators';
import User from '@/models/User';

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
    name: 'Чё тебе надо у меня дома, мент?',
    description: 'К джентельмену вломились силовые структуры.'
      + ' Помогите ему выяснить причину их появления и, по возможности,'
      + ' получить компенсацию за поломанное имущество.',
    completed: false,
  },
    {
      id: 2,
      name: 'Контроль версий',
      description: 'что это такое ',
      completed: true,
    }as ProblemModel];

  private homework: Array<ProblemModel> = [{
    id: 3,
    name: 'Контроль версий',
    description: 'что это такое ',
    completed: false,
  }];

  private lesson1: LessonModel = {
    id: 5,
    name: 'Введение',
    deadline: '31.12.2020',
    classwork: this.problems,
    homework: this.homework,
    lessoncontent: 'Статья',
  }

  get getCourse() {
    return this.course;
  }

  get getProblems() {
    return this.problems;
  }

  get getCourses() {
    return this.courses;
  }

  get getLesson() {
    return this.lesson1;
  }
}
