import ProblemModel from '@/models/ProblemModel';
import axios from 'axios';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ name: 'problem' })
export default class ProblemModule extends VuexModule {

  problems: Array<ProblemModel> = [];

  @Mutation
  setProblems(payload: Array<ProblemModel>) {
    this.problems = payload;
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
    this.problems.push(element);
    this.problems = [...this.problems];
  }

  get getNewProblem(): ProblemModel {
    return {
      id: NaN, lessonId: NaN, type: 'classwork', name: '', description: '',
      completed: false, manual: false, language: [],
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
}
