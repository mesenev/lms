import UserProgress from '@/models/UserProgress';
import store from '@/store';
import axios from 'axios';
import {Action, getModule, Module, Mutation, VuexModule} from 'vuex-module-decorators';
import {Dictionary} from "vue-router/types/router";

@Module({namespaced: true, name: 'progress', store, dynamic: true})
class ProgressModule extends VuexModule {

  lessonProgress: Dictionary<UserProgress[]> = {};

  @Mutation
  setProgress(payload: Dictionary<UserProgress[]>) {
    this.lessonProgress = payload;
  }

  @Action
  async fetchLessonProgressByLessonId(id: number): Promise<UserProgress[]> {
    if (id in this.lessonProgress) {
      return this.lessonProgress[id];
    }

    let answer = {data: {}};
    await axios.get('/api/lessonprogress/', {params: {lesson_id: id}})
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    const result = answer.data as Array<UserProgress>;
    this.setProgress({[id]: result})
    return result;
  }
}

export default getModule(ProgressModule);
