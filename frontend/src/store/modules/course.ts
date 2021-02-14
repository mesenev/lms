import CourseModel from '@/models/CourseModel';
import store from '@/store';
import axios from 'axios';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'course', store, dynamic: true })
class CourseModule extends VuexModule {
  currentCourse: CourseModel | null = null;
  courses: Array<CourseModel> = [];

  @Mutation
  setCourses(payload: Array<CourseModel>) {
    this.courses = payload;
  }

  @Mutation
  changeCurrentCourse(payload: CourseModel | null) {
    this.currentCourse = payload;
  }

  @Action
  async fetchUserCourses() {
    await axios.get('/api/course/user_courses/')
      .then(response => {
        this.setCourses(response.data);
      })
      .catch(error => {
        console.log(error);
      })
  }

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

  @Mutation
  addCourseToArray(element: CourseModel) {
    this.courses.push(element);
    this.courses = [...this.courses];
  }
}

export default getModule(CourseModule);
