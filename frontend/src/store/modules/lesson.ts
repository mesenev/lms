import CourseModel from '@/models/CourseModel';
import axios from 'axios';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ name: 'course' })
export default class LessonModule extends VuexModule {

  lessons: Array<CourseModel> = [];

  @Mutation
  setLessons(payload: Array<CourseModel>) {
    this.lessons = payload;
  }

  @Action
  async fetchLessons() {
    await axios.get('http://localhost:8000/api/course/')
      .then(response => {
        console.log(response.data);
        this.setLessons(response.data);
      }).catch(error => { console.log(error); })
  }

  @Mutation
  addLessonToArray(element: CourseModel) {
    this.lessons.push(element);
    this.lessons = [...this.lessons];
  }
}

