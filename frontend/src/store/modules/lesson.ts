import LessonModel from '@/models/LessonModel';
import store from '@/store';
import axios from 'axios';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({
  namespaced: true,
  name: 'lesson',
  store,
  dynamic: true,
})
class LessonModule extends VuexModule {

  lessons: Array<LessonModel> = [];

  @Mutation
  setLessons(payload: Array<LessonModel>) {
    this.lessons = payload;
  }

  @Action
  async fetchLessons() {
    await axios.get('http://localhost:8000/api/lesson/')
      .then(response => {
        this.setLessons(response.data);
      }).catch(error => { console.log(error); })
  }

  @Action
  async fetchLessonById(id: number): Promise<LessonModel> {
    let answer = { data: {} };
    await axios.get(`http://localhost:8000/api/lesson/${id}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    const result = answer.data as LessonModel;
    return result;
  }

  @Mutation
  addLessonToArray(element: LessonModel) {
    this.lessons.push(element);
    this.lessons = [...this.lessons];
  }

  get getNewLesson(): LessonModel {
    return {
      id: NaN,
      course: NaN,
      name: '',
      description: '',
      lessonContent: '',
      problems: [],
      materials: [],
      deadline: '2000-01-01',
    } as LessonModel;
  }

}

export default getModule(LessonModule);
