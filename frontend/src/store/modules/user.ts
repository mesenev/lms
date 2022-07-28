import CourseModel from "@/models/CourseModel";
import UserModel from '@/models/UserModel';
import UserProgress from '@/models/UserProgress';
import store from '@/store';
import courseModule from '@/store/modules/course';
import axios from 'axios';
import { Dictionary } from 'vue-router/types/router';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators'

@Module({ namespaced: true, name: 'user', store, dynamic: true })
class UserModule extends VuexModule {
  public user: UserModel = {
    id: -1,
    username: '',
    first_name: '',
    last_name: '',
    staff_for: [],
    avatar_url: '',
    thumbnail: '',
    email: '',
    cats_account: null
  }

  // storage for all fetched users associated with courseId
  currentCourseStudents: Dictionary<UserModel> = {};
  cachedStudents: Dictionary<UserModel> = {};

  @Mutation fetchStudentsMutation(data: Dictionary<UserModel>) {
    this.currentCourseStudents = data;
  }

  @Mutation fetchCachedStudents(data: Dictionary<UserModel>) {
    this.cachedStudents = data;
  }

  @Mutation receiveUser(user: object) {
    this.user = user as UserModel;
  }

  @Mutation addStaffToArray(courseId: number) {
    this.user.staff_for.push(courseId);
    this.user.staff_for = [...this.user.staff_for];
  }

  @Action
  async fetchStudentsByCourseId(courseId: number): Promise<Dictionary<UserModel>> {
    const course: CourseModel = await courseModule.fetchCourseById(courseId);
    const answer = (course.students as UserModel[]).reduce<Dictionary<UserModel>>(
      (previousValue, currentValue) => {
        previousValue[currentValue.id] = currentValue;
        return previousValue;
      }, {});
    this.fetchStudentsMutation({ ...this.currentCourseStudents, [courseId]: answer });
    return answer;
  }

  @Action
  async fetchStudentsProgressByLessonId(): Promise<Array<UserProgress>> {
    let data = {data: {}}
    await axios.get('/api/lessonprogress/').then(response => data = response)
      .catch(error => {
        console.log(error);
      });
    return data.data as Array<UserProgress>;
  }

  @Action
  async fetchUserById(userId: number): Promise<UserModel> {
    let data = { data: {} }
    if (userId in this.currentCourseStudents)
      return this.currentCourseStudents[userId];
    if (userId in this.cachedStudents)
      return this.cachedStudents[userId];
    await axios.get(`/api/users/${userId}/`).then(response => data = response)
      .catch(error => {
        console.log(error);
      });
    this.fetchCachedStudents({ ...this.cachedStudents, [userId]: data.data as UserModel });

    return data.data as UserModel;
  }
}

export default getModule(UserModule);
