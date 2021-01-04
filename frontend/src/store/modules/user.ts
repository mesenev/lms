import UserModel from '@/models/UserModel';
import { Module, Mutation, VuexModule } from 'vuex-module-decorators'


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
}

