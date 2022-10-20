import CourseModel from '@/models/CourseModel';
import CourseScheduleModel from '@/models/ScheduleModel';
import store from '@/store';
import userStore from '@/store/modules/user';
import api from '@/store/services/api'
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'course', store, dynamic: true })
class CourseModule extends VuexModule {
  currentCourse: CourseModel | null = null;
  courses: Array<CourseModel> = [];

  get is_staff() {
    if (!this.currentCourse)
      return false;
    return userStore.user.staff_for.includes(this.currentCourse.id);
  }

  get newCourse(): CourseModel {
    return {
      id: NaN, name: '', author: userStore.user, cats_id: null, lessons: [],
      completed: false, description: '', students: [], schedule: null, de_options: "",
    };
  }

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
    await api.get('/api/course/user_courses/')
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
    await api.get(`/api/course/${id}/`)
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

  @Action
  async fetchCourseScheduleByCourseId(id: number): Promise<CourseScheduleModel> {
    let answer = { data: {} };
    await api.get(`/api/course-schedule/by-course/${id}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as CourseScheduleModel;
  }
}

export default getModule(CourseModule);
