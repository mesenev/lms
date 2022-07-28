import store from '@/store';
import axios from 'axios';
import { Action, getModule, Module, VuexModule } from 'vuex-module-decorators'
import LogEventModel from "@/models/LogEventModel";
import * as types from "@/models/LogEventModel";

@Module({ namespaced: true, name: 'logevent', store, dynamic: true })
class LogEvent extends VuexModule {


  get getNewLogEventMessage(): LogEventModel {
    return {
      id: NaN, type: types.TYPE_MESSAGE, student: NaN, problem: NaN, data: {},
    };
  }

  @Action
  async fetchLogEventsByProblemAndStudentIds(
    data: { problem: number; student: number; limit: number; offset: number}
  ):
    Promise<Array<LogEventModel>> {
    let answer = {};
    await axios.get('/api/logevents/', {
      params: data,
    }).then(response => {
      answer = response.data.results;
    })
      .catch(error => {
        console.error(error);
      })
    return answer as Array<LogEventModel>;
  }

  @Action
  async deleteEvent(id: number) {
    let answer = {};
    await axios.delete(`/api/logevents/${id}/`).then(
      response => {
        answer = response.data;
      },
    ).catch(reason => {
      //
    });
    return answer;
  }

  @Action
  async createLogEvent(event: LogEventModel): Promise<LogEventModel | undefined> {
    let answer: { id?: number } = {};
    delete (event as { id?: number }).id;
    await axios.post('/api/logevents/', event).then(
      response => answer = response.data as LogEventModel,
    ).catch(response => console.log('error creating event', response))
    if (answer.id !== undefined)
      return answer as LogEventModel;
    return undefined;
  }
}

export default getModule(LogEvent);
