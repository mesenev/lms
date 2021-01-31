import CourseModel from "@/models/CourseModel";
import UserModel from '@/models/UserModel';
import UserProgress from '@/models/UserProgress';
import store from '@/store';
import courseModule from '@/store/modules/course';
import { Dictionary } from 'vue-router/types/router';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators'

@Module({ namespaced: true, name: 'user', store, dynamic: true })
class UserModule extends VuexModule {
  public user: UserModel = {
    id: -1, username: '', first_name: '', last_name: '', staff_for: [],
  }

  fetchedStudents: Dictionary<Array<UserModel>> = {};

  @Mutation receiveUser(user: object) {
    this.user = user as UserModel;
  }

  @Action
  async fetchStudentsByCourseId(courseId: number): Promise<Array<UserModel>> {
    const course: CourseModel = await courseModule.fetchCourseById(courseId);
    const answer = course.students as UserModel[];
    this.fetchedStudents = { ...this.fetchedStudents, courseId: answer }
    return answer;
  }

  @Action
  async fetchStudentsProgressByCourseId(courseId: number): Promise<Array<UserProgress>> {
    throw Error();
  }
}

export default getModule(UserModule);
