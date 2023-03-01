import { getModule, Module, Mutation, VuexModule } from "vuex-module-decorators";
import store from "@/store";
import QuestionModel from "@/models/QuestionModel";
import { Dictionary } from "vue-router/types/router";

@Module({ namespaced: true, name: 'question', store, dynamic: true })
class QuestionModule extends VuexModule {
  questions: Dictionary<QuestionModel[]> = {};

  get newQuestion(): QuestionModel {
    return {
      index: 0,
      text: '',
      description: '',
      answer_type: 'input',
      all_answers: [],
      correct_answers: [],
      attachment_url: '',
      points: 0,
    } as QuestionModel
  }

  @Mutation
  setQuestions(payload: Dictionary<QuestionModel[]>) {
    this.questions = {...this.questions, ...payload};
  }
}

export default getModule(QuestionModule);
