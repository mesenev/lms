import LessonModel from '@/models/LessonModel';
import axios from 'axios';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ name: 'lesson' })
export default class LessonModule extends VuexModule {

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
    return answer.data as LessonModel;
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

