import CatsProblemModel from '@/models/CatsProblemModel';
import ProblemModel from '@/models/ProblemModel';
import store from '@/store';
import axios from 'axios';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'problem', store, dynamic: true })
class ProblemModule extends VuexModule {

  _problems: Array<ProblemModel> = [];
  catsProblems: Array<{ id: CatsProblemModel }> = [];
  currentProblem: ProblemModel | null = null;

  @Mutation
  changeCurrentProblem(payload: ProblemModel | null) {
    this.currentProblem = payload;
  }

  get problems(): Array<ProblemModel> {
    return this._problems;
  }

  @Mutation
  setProblems(payload: Array<ProblemModel>) {
    this._problems = payload;
  }

  @Action
  async fetchProblems() {
    await axios.get('http://localhost:8000/api/problem/')
      .then(response => {
        this.setProblems(response.data);
      })
      .catch(error => {
        console.log(error);
      })
  }

  @Mutation
  addProblemToArray(element: ProblemModel) {
    this._problems.push(element);
    this._problems = [...this._problems];
  }

  get getNewProblem(): ProblemModel {
    return {
      id: NaN, lesson: NaN, type: 'CW', name: '', description: '',
      completed: false, manual: false, language: null, cats_material_url: '', cats_id: NaN,
    };
  }

  @Action
  async fetchProblemById(problemId: number): Promise<ProblemModel> {
    let answer = { data: {} };
    await axios.get(`http://localhost:8000/api/problem/${problemId}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as ProblemModel;
  }

  @Action
  async fetchCatsProblemById(catsId: number): Promise<CatsProblemModel> {
    let answer = { data: {} };
    await axios.get(`http://localhost:8000/api/cats-problem/${catsId}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as CatsProblemModel;

  }

  @Action
  async patchProblem(problem: ProblemModel) {
    return await axios.patch(`http://localhost:8000/api/problem/${problem.id}/`, problem);
  }
}

export default getModule(ProblemModule);
