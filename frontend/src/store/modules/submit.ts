import SubmitModel from '@/models/SubmitModel';
import store from '@/store';
import axios, { AxiosResponse } from 'axios';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'submit', store, dynamic: true })
class SubmitModule extends VuexModule {
  private _submits: SubmitModel[] = []

  get defaultSubmit(): SubmitModel {
    return { id: NaN, problem: NaN, student: NaN, content: '', status: 'NP' };
  }

  get submits(): SubmitModel[] {
    return this._submits;
  }

  @Mutation
  setSubmits(submits: SubmitModel[]) {
    this._submits = submits;
  }

  @Mutation
  addSubmitToArray(submit: SubmitModel) {
    this._submits.push(submit);
    this._submits = [...this._submits];
  }

  @Action
  async fetchSubmits(payload: { problemId: number; userId: number }): Promise<Array<SubmitModel>> {
    let answer = {};
    await axios.get('http://localhost:8000/api/submit/', {
      params: {
        problem: payload.problemId,
        user: payload.userId,
      },
    })
      .then(response => {
        this.setSubmits(response.data);
        answer = response.data;
      })
      .catch(error => {
        console.error(error);
      })
    return answer as Array<SubmitModel>;
  }

  @Mutation
  changeSubmitStatus(payload: { id: number; status: string }) {
    this._submits.map((submit) => {
      if (submit.id === payload.id) {
        submit.status = payload.status;
      }
    })
    this._submits = [...this._submits];
  }

  @Action
  async fetchSubmitById(id: number): Promise<SubmitModel> {
    const answer = this.submits.find(x => x.id === id);
    if (answer) { return answer; }
    let data = {};
    await axios.get(`http://localhost:8000/api/submit/${id}/`)
      .then((response: AxiosResponse<SubmitModel>) => {
        this.addSubmitToArray(response.data);
        data = response.data
      })
      .catch(error => {
        console.error(error);
      })
    return data as SubmitModel;
  }
}

export default getModule(SubmitModule);
