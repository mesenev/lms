import { Action, getModule, Module, Mutation, VuexModule } from "vuex-module-decorators";
import store from "@/store";
import QuestionModel from "@/models/QuestionModel";
import { Dictionary } from "vue-router/types/router";

@Module({ namespaced: true, name: 'question', store, dynamic: true })
class QuestionModule extends VuexModule {
  questions: Dictionary<QuestionModel[]> = {};

  get newQuestion(): QuestionModel {
    return {
      id: NaN,
      question: '',
      test: NaN,
      description: '',
      answer_type: '',
      answers: [],
      correct_answers: [],
      attachment_file: '',
      points: NaN,
    } as QuestionModel;
  }
  @Action
  async fetchQuestionsByTestId(id: number) {
    return this.questions[id];
  }
  @Mutation
  addQuestion(question: QuestionModel, id: number) {
    this.questions[id].push(question);
  }
}

export default getModule(QuestionModule);
