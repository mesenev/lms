import CourseModel from '@/models/CourseModel';
import axios from 'axios';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ name: 'course' })
export default class CourseModule extends VuexModule {

  @Action
  async fetchCourseById(id: number): Promise<CourseModel> {
    let answer = { data: {} };
    await axios.get(`http://localhost:8000/api/course/${id}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as CourseModel;
  }
}
