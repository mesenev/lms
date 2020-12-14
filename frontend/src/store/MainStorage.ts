import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import {
  Module, VuexModule, Mutation,
} from 'vuex-module-decorators';
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
    name: '123',
    description: '456',
    completed: true,
  } as ProblemModel];

  private users: Array<User> = [
    {
      id: 0,
      name: 'Vlad Maximov',
      courseLength: this.getCourse.lessons.length,
      marks: this.getCourse.lessons.map(() => Math.floor(Math.random() * 4) + 2),
      attendance: this.getCourse.lessons.map(() => false),
    },
    {
      id: 1,
      name: 'Max Vladov',
      courseLength: this.getCourse.lessons.length,
      marks: this.getCourse.lessons.map(() => Math.floor(Math.random() * 4) + 2),
      attendance: this.getCourse.lessons.map(() => false),
    },
  ];

  @Mutation
  changeAttendance(payload: { userId: number; lessonId: number }) {
    const user = this.users[payload.userId];
    user.attendance[payload.lessonId] = (
      !user.attendance[payload.lessonId]
    );
    this.users = this.users.map((u) => ((u.id === user.id) ? user : u));
  }

  get getUsers() {
    return this.users;
  }

  get getColumns() {
    return this.getCourse.lessons.map((l) => l.name);
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
}
