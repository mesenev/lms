import { Action, getModule, Module, Mutation, VuexModule } from "vuex-module-decorators";
import store from "@/store";
import { Dictionary } from "vue-router/types/router";
import TestModel from "@/models/TestModel";
import api from "@/store/services/api";
import QuestionModel from "@/models/QuestionModel";

@Module({ namespaced: true, name: 'test', store, dynamic: true })
class TestModule extends VuexModule {
  testsByLesson: Dictionary<TestModel[]> = {};

  currentTest: TestModel | null = null;

  get newTest() {
    return {
      id: NaN,
      name: '',
      lesson: NaN,
      description: '',
      questions: [],
      points: 0,
      test_mode: '',
      is_hidden: true,
    } as TestModel;
  }

  @Action
  async fetchTestsByLessonId(id: number): Promise<TestModel[]> {
    if (id in this.testsByLesson) {
      return this.testsByLesson[id];
    }
    let answer = { data: {} };
    await api.get('/api/test/', { params: { lesson_id: id } })
        .then(response => answer = response)
        .catch(error => {
          console.log(error);
        });
    const result = answer.data as Array<TestModel>;
    this.setTests({ [id]: result });
    return result;
  }

  @Action
  async fetchTestById(id: number): Promise<TestModel> {
    let answer = { data: {} };
    await api.get(`/api/test/${id}/`)
        .then(response => answer = response)
        .catch(error => {
          console.log(error);
        });
    console.log(answer.data);
    return answer.data as TestModel;
  }

  @Mutation
  changeCurrentTest(payload: TestModel | null) {
    this.currentTest = payload;
  }

  @Mutation
  changeTestVisibility(test: TestModel) {
    const curTest = this.testsByLesson[test.lesson].find(el => el.id === test.id);
    if (curTest != undefined) {
      curTest.is_hidden = test.is_hidden;
    }
  }

  @Mutation
  setTests(payload: Dictionary<TestModel[]>) {
    this.testsByLesson = { ...this.testsByLesson, ...payload };
  }

  @Action
  async patchTest(params: { is_hidden: boolean; id: number }) {
    let answer = { data: {} };
    await api.patch(`/api/test/${params.id}/`, { ...params })
        .then(response => answer = response)
        .catch(error => {
          console.log(error);
        });
    const result = answer.data as TestModel;
    this.changeCurrentTest(result);
    this.changeTestVisibility(result);
    return result;
  }
}

export default getModule(TestModule);
