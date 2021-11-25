import store from '@/store';
import axios from 'axios';
import { Action, getModule, Module, VuexModule } from 'vuex-module-decorators'
import LogEventModel from "@/models/LogEventModel";
import * as types from "@/models/LogEventModel";

@Module({ namespaced: true, name: 'user', store, dynamic: true })
class LogEvent extends VuexModule {


  get getNewLogEventMessage(): LogEventModel {
    return {
      id: NaN, type: types.TYPE_MESSAGE, student: NaN, problem: NaN, data: { author: NaN }
    };
  }

  @Action
  async fetchLogEventsByProblemAndStudentIds(problemId: number, studentId: number):
    Promise<Array<LogEventModel>> {
    let answer = {};
    await axios.get('/api/logevent/', {
      params: {
        problem: problemId,
        student: studentId,
      },
    }).then(response => {
      answer = response.data;
    })
      .catch(error => {
        console.error(error);
      })
    return answer as Array<LogEventModel>;
  }

  @Action
  async createLogEvent(event: LogEventModel): Promise<LogEventModel|undefined> {
    let answer: { id?: number } = {};
    delete (event as {id?: number}).id;
    await axios.post('/api/logevent/', event).then(
      response => answer = response.data as LogEventModel
    ).catch(response => console.log('error creating event', response))
    if (answer.id !== undefined)
      return answer as LogEventModel;
    return undefined;
  }
}

export default getModule(LogEvent);
