import CatsProblemModel from '@/models/CatsProblemModel';
import ProblemModel from '@/models/ProblemModel';
import store from '@/store';
import api from '@/store/services/api'
import { Dictionary } from 'vue-router/types/router';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'problem', store, dynamic: true })
class ProblemModule extends VuexModule {

  problemsByLesson: Dictionary<ProblemModel[]> = {};
  catsProblems: Array<{ id: CatsProblemModel }> = [];
  currentProblem: ProblemModel | null = null;

  get getNewProblem(): ProblemModel {
    return {
      id: NaN, lesson: NaN, type: 'CW', name: '', description: '',
      completed: false, manual: false, language: null, cats_material_url: '', cats_id: NaN,
      de_options: '', test_mode: ''
    };
  }

  @Mutation
  changeCurrentProblem(payload: ProblemModel | null) {
    this.currentProblem = payload;
  }

  @Mutation
  setProblems(payload: Dictionary<ProblemModel[]>) {
    this.problemsByLesson = { ...this.problemsByLesson, ...payload };
  }

  @Action
  async fetchProblems(data: object) {
    //TODO: remove or fix (data here is set of fields to filter)
    await api.get('/api/problem/', { params: data })
      .then(response => {
        this.setProblems(response.data);
      })
      .catch(error => {
        console.log(error);
      })
  }

  @Action
  async fetchProblemById(problemId: number): Promise<ProblemModel> {
    let answer = { data: {} };
    await api.get(`/api/problem/${problemId}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as ProblemModel;
  }

  @Action
  async fetchCatsProblemById(catsId: number): Promise<CatsProblemModel> {
    let answer = { data: {} };
    await api.get(`/api/cats-problem/${catsId}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as CatsProblemModel;

  }

  @Action
  async patchProblem(problem: ProblemModel) {
    return await api.patch(`/api/problem/${problem.id}/`, problem);
  }

  @Action
  async fetchProblemsByLessonId(id: number): Promise<ProblemModel[]> {
    if (id in this.problemsByLesson) {
      return this.problemsByLesson[id];
    }
    let answer = { data: {} };
    await api.get('/api/problem/', { params: { lesson_id: id } })
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    const result = answer.data as Array<ProblemModel>;
    this.setProblems({ [id]: result })
    return result;
  }

  @Action
  async fetchProblemsForCourse(course_id: number): Promise<ProblemModel[]> {
    let answer = { data: {} };
    await api.get(`/api/problem/by-course/${course_id}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as Array<ProblemModel>;
  }
}

export default getModule(ProblemModule);
