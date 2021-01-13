import UserModel from '@/models/UserModel';
import UserProgress from '@/models/UserProgress';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import CourseModel from "@/models/CourseModel";
import { courseStore } from '@/store';


@Module({ name: 'user' })
export default class UserModule extends VuexModule {
  public user: UserModel = {
    id: -1,
    username: '',
    first_name: '',
    last_name: '',
    staff_for: [],
  }

  @Mutation receiveUser(user: object) {
    this.user = user as UserModel;
  }

  @Action
  async fetchStudentsByCourseId(courseId: number): Promise<Array<UserModel>> {
    const course: CourseModel = await courseStore.fetchCourseById(courseId);
    return course.students as UserModel[];
  }

  @Action
  async fetchStudentsProgressByCourseId(courseId: number): Promise<Array<UserProgress>> {
    throw Error();
  }
}

