import UserModel from '@/models/UserModel';
import UserProgress from '@/models/UserProgress';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'


@Module({ name: 'user' })
export default class UserModule extends VuexModule {
  public user: UserModel = {
    id: -1,
    username: '',
    firstName: '',
    lastName: '',
  }

  @Mutation receiveUser(user: object) {
    this.user = user as UserModel;
  }

  @Action
  fetchStudentsByCourseId(courseId: number): Array<UserModel> {
    throw Error();
  }

  @Action
  async fetchStudentsProgressByCourseId(courseId: number): Promise<Array<UserProgress>> {
    throw Error();
  }
}

