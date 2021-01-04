import CourseModel from '@/models/CourseModel';
import axios from 'axios';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({name: 'course' })
export default class CourseModule extends VuexModule {

  courses: Array<CourseModel> = [];

  @Mutation
  setCourses(payload: Array<CourseModel>) {
    this.courses = payload;
  }

  @Action
  async fetchCourses() {
    await axios.get('http://localhost:8000/api/course/')
      .then(response => {
        console.log(response.data);
        this.setCourses(response.data);
      })
      .catch(error => {
        console.log(error);
      })
  }
  // @Action
  // async fetchCourseById(id: number) {
  //   await axios.get(`http://localhost:8000/api/course/${id}/`)
  //     .then(response => {
  //       console.log(response.data);
  //       this.addCourseToArray(response.data);
  //     })
  //     .catch(error => {
  //       console.log(error);
  //     })
  // }

  @Mutation
  addCourseToArray(element: CourseModel) {
    this.courses.push(element);
    this.courses = [...this.courses];
  }
}

