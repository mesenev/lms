import CourseModel from "@/models/CourseModel";
import UserModel from '@/models/UserModel';
import UserProgress from '@/models/UserProgress';
import { courseStore } from '@/store';
import { Dictionary } from 'vue-router/types/router';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'

@Module({ name: 'user' })
export default class UserModule extends VuexModule {
  public user: UserModel = {
    id: -1,
    username: '',
    first_name: '',
    last_name: '',
    staff_for: [],
  }

  fetchedStudents: Dictionary<Array<UserModel>> = {};

  @Mutation receiveUser(user: object) {
    this.user = user as UserModel;
  }

  @Action
  async fetchStudentsByCourseId(courseId: number): Promise<Array<UserModel>> {
    const course: CourseModel = await courseStore.fetchCourseById(courseId);
    const answer = course.students as UserModel[];
    this.fetchedStudents = { ...this.fetchedStudents, courseId: answer }
    return answer;
  }

  @Action
  async fetchStudentsProgressByCourseId(courseId: number): Promise<Array<UserProgress>> {
    throw Error();
  }
}

