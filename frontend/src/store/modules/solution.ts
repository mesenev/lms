import { Action, getModule, Module, Mutation, VuexModule } from "vuex-module-decorators";
import store from "@/store";
import SolutionModel from "@/models/SolutionModel";
import api from "@/store/services/api";

@Module({ namespaced: true, name: 'solution', store, dynamic: true })
class SolutionModule extends VuexModule {
  _solutions: SolutionModel[] = [];

  get solutions(): Array<SolutionModel> {
    return this._solutions;
  }

  get defaultSolution(): SolutionModel {
    return {
      id: NaN,
      exam: NaN,
      student: NaN,
      user_answers: [],
      score: NaN,
      status: 'await',
      correct_questions_indexes: [],
    };
  }

  @Mutation
  setSolutions(solutions: SolutionModel[]) {
    this._solutions = solutions;
  }

  @Action
  async fetchSolutionsByExamAndUser(payload: { examId: number; userId: number }): Promise<SolutionModel[]> {
    let answer = {};
    await api.get('/api/solution/', {
      params: {
        solution: payload.examId,
        user: payload.userId,
      }
    }).then(response => {
      answer = response.data;
      this.setSolutions(response.data);
    }).catch(error => {
      console.log(error);
    });
    return answer as Array<SolutionModel>;
  }

  @Action
  async fetchSolutionsByExam(examId: number): Promise<SolutionModel[]> {
    let answer = {};
    await api.get('/api/solution/', {
      params: {
        exam: examId,
      }
    }).then(response => {
      answer = response.data;
      this.setSolutions(response.data);
    }).catch(error => {
      console.log(error);
    });
    return answer as Array<SolutionModel>;
  }

  @Action({rawError: true})
  async fetchSolutionById(id: number): Promise<SolutionModel> {
    let answer = {};
    await api.get(`/api/solution/${id}/`).then(response => {
      answer = response.data;
    }).catch(error => {
      console.log(error);
      throw error;
    });
    return answer as SolutionModel;
  }
}

export default getModule(SolutionModule);
