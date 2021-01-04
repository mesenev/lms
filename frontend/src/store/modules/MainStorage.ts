import CourseModel from '@/models/CourseModel';
import LessonContent from "@/models/LessonContent";
import LessonModel from '@/models/LessonModel';
import ProblemModel from '@/models/ProblemModel';
import UserProgress from "@/models/UserProgress";
import { Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ name: 'MainStorage' })
export default class MainStorage extends VuexModule {
  course: CourseModel = {
    id: 8,
    lessons: [{ id: 1, name: 'Урок 1' }, { id: 2, name: 'Урок 2' }] as Array<LessonModel>,
    completed: false,
    author: {
      id: 1,
      username: 'Антищенко',
      firstName: 'Антон',
      lastName: 'Антонович',
    },
    name: 'Алгоритмы и структуры данных (введение)',
  };

  private courses: Array<CourseModel> = [this.course, this.course, this.course, this.course]

  private language: Array<string> = ['C++', 'Python', 'C', 'Java']

  get avLang() {
    return this.language;
  }

  private problems: Array<ProblemModel> = [{
    id: 1,
    name: 'Чё тебе надо у меня дома, мент?',
    description: 'К джентельмену вломились силовые структуры.'
      + ' Помогите ему выяснить причину их появления и, по возможности,'
      + ' получить компенсацию за поломанное имущество.',
    completed: false,
    language: ['Java'],
    manual: true,
  } as ProblemModel,
    {
      id: 2,
      name: 'Контроль версий',
      description: 'что это такое ',
      completed: true,
      language: ['Java'],
      manual: true,
    } as ProblemModel];


  get problem() {
    return this.problems[0];
  }

  @Mutation setCourses(payload: Array<CourseModel>) {
    debugger
    this.courses = payload;
  }

  @Mutation changeProblemName(payload: string) {
    this.problem.name = payload;
  }

  @Mutation changeProblemDescription(payload: string) {
    this.problem.description = payload;
  }

  @Mutation changeProblemManual(payload: boolean) {
    this.problem.manual = payload;
  }

  @Mutation
  changeProblemLanguage(payload: Array<string>) {
    this.problem.language = payload;
  }

  private temporaryUserProgress: UserProgress = {
    id: 1,
    name: 'Vlad Maximov',
    marks: this.course.lessons.map(() => Math.floor(Math.random() * 4) + 2),
    attendance: this.course.lessons.map(() => false),
  }

  private users: Array<UserProgress> = [
    { ...this.temporaryUserProgress, id: 1, attendance: this.course.lessons.map(() => false) },
    {
      ...this.temporaryUserProgress,
      id: 2,
      name: 'Max Vladov',
      attendance: this.course.lessons.map(() => false),
    },
  ];

  @Mutation changeAttendance(payload: { userId: number; lessonId: number }) {
    const user = this.users[payload.userId];
    user.attendance[payload.lessonId] = (
      !user.attendance[payload.lessonId]
    );
    this.users = this.users.map((u) => ((u.id === user.id) ? user : u));
  }

  get getUsers() {
    return this.users;
  }

  private homework: Array<ProblemModel> = [
    {
      id: 3,
      name: 'Контроль версий',
      description: 'что это такое ',
      completed: false,
    } as ProblemModel];

  get getColumns() {
    return this.getCourse?.lessons.map((l) => l.name);
  }

  private material: Array<LessonContent> = [{
    id: 1,
    name: 'FAQ к уроку',
    text: 'Кто такие менты?',
  },
    {
      id: 2,
      name: 'Документация GIT',
    },
  ];

  private lesson1: LessonModel = {
    id: 5,
    name: 'Введение',
    deadline: '31.12.2020',
    classwork: this.problems,
    homework: this.homework,
    materials: this.material,
  }

  private lessons: Array<LessonModel> = [this.lesson1, this.lesson1, this.lesson1, this.lesson1]

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

  private allLessons: LessonModel[] = [
    { ...this.getLesson, id: 1, name: 'Урок 1' },
    { ...this.getLesson, id: 2, name: 'Урок 2' },
    { ...this.getLesson, id: 3, name: 'Урок 3' },
    { ...this.getLesson, id: 4, name: 'Урок 4' },
    { ...this.getLesson, id: 5, name: 'Урок 5' },
  ];

  get getNextLessonId(): number {
    return this.allLessons.length + 1;
  }

  get getAllLessons(): LessonModel[] {
    return this.allLessons;
  }

  @Mutation changeCourseName(payload: string) {
    this.course = { ...this.course, name: payload } as CourseModel;
  }

  @Mutation changeCourseDescription(payload: string) {
    this.course = { ...this.course, description: payload } as CourseModel;
  }

  @Mutation addLessonToCourse(payload: LessonModel) {
    this.course = { ...this.course, lessons: this.course.lessons.concat(payload) } as CourseModel;
  }

  @Mutation addLessonToAllLesson(payload: LessonModel) {
    this.allLessons = [...this.allLessons, payload];
  }

  @Mutation deleteLesson(payload: LessonModel) {
    this.course = {
      ...this.course,
      lessons: this.course.lessons.filter(
        (lesson) => lesson.id !== payload.id,
      ),
    };
  }

  get getLessons() {
    return this.lessons;
  }

}
