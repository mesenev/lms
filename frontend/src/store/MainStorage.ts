import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import {
  Module, VuexModule, Mutation,
} from 'vuex-module-decorators';
// import User from '@/models/User';
import UserProgress from "@/models/UserProgress";
import LessonContent from "@/models/LessonContent";

@Module({ name: 'MainStorage' })
export default class MainStorage extends VuexModule {
  private course: CourseModel = {
    id: 8,
    lessons: [{ id: 1, name: 'Урок 1' }, { id: 2, name: 'Урок 2' }] as Array<LessonModel>,
    completed: false,
    name: 'Алгоритмы и структуры данных (введение)',
  }

  @Mutation
  changeCourseName(payload: string) {
    this.course = { ...this.course, name: payload } as CourseModel;
  }

  @Mutation
  changeCourseDescription(payload: string) {
    this.course = { ...this.course, description: payload } as CourseModel;
  }

  @Mutation
  addLesson(payload: LessonModel) {
    this.course = { ...this.course, lessons: this.course.lessons.concat(payload) };
  }

  @Mutation
  deleteLesson(payload: LessonModel) {
    this.course = {
      ...this.course,
      lessons: this.course.lessons.filter(
        (lesson) => lesson !== payload
      )
    };
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

  private users: Array<UserProgress> = [
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

  private homework: Array<ProblemModel> = [{
    id: 3,
    name: 'Контроль версий',
    description: 'что это такое ',
    completed: false,
  }];

  private material: Array<LessonContent> = [{
    id: 1,
    name: 'FAQ к уроку',
    text: 'Кто такие менты?'
  },
    {
    id: 2,
    name: 'Документация GIT',
  }
  ];

  private lesson1: LessonModel = {
    id: 5,
    name: 'Введение',
    deadline: '31.12.2020',
    classwork: this.problems,
    homework: this.homework,
    materials: this.material
  }

  private lessons: Array<LessonModel> = [this.lesson1, this.lesson1, this.lesson1, this.lesson1]

  private language: Array<string> = [
    'C++', 'Python','C'
  ]

  get lang() {
    return this.language;
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

  get getLessons() {
    return this.lessons;
  }
}
