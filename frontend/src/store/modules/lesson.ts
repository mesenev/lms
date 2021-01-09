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
      deadline: '',
    } as LessonModel;
  }


}

