import CourseModel from "@/models/CourseModel";
import UserModel from '@/models/UserModel';
import UserProgress from '@/models/UserProgress';
import store from '@/store';
import courseModule from '@/store/modules/course';
import { Dictionary } from 'vue-router/types/router';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import axios from 'axios';

@Module({ namespaced: true, name: 'user', store, dynamic: true })
class UserModule extends VuexModule {
  public user: UserModel = {
    id: -1, username: '', first_name: '', last_name: '', staff_for: [],
  }

  // storage for all fetched users associated with courseId
  fetchedStudents: Dictionary<Dictionary<UserModel>> = {};

  @Mutation fetchStudentsMutation(data: Dictionary<Dictionary<UserModel>>) {
    this.fetchedStudents = data;
  }

  @Mutation receiveUser(user: object) {
    this.user = user as UserModel;
  }

  @Action
  async fetchStudentsByCourseId(courseId: number): Promise<Dictionary<UserModel>> {
    const course: CourseModel = await courseModule.fetchCourseById(courseId);
    const answer = (course.students as UserModel[]).reduce<Dictionary<UserModel>>(
      (previousValue, currentValue) => {
        previousValue[currentValue.id] = currentValue;
        return previousValue;
      }, {});
    this.fetchStudentsMutation({ ...this.fetchedStudents, [courseId]: answer });
    return answer;
  }

  @Action
  async fetchStudentsProgressByLessonId(lessonId: number): Promise<Array<UserProgress>> {
    let data = { data: {}}
    await axios.get('http://localhost:8000/api/lessonprogress/').
      then( response => data = response)
      .catch(error => {
        console.log(error);
      })
    return data.data as Array<UserProgress>;
  }
}

export default getModule(UserModule);
