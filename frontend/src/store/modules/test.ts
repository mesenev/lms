import { Action, getModule, Module, Mutation, VuexModule } from "vuex-module-decorators";
import store from "@/store";
import { Dictionary } from "vue-router/types/router";
import TestModel from "@/models/TestModel";

@Module({ namespaced: true, name: 'test', store, dynamic: true })
class TestModule extends VuexModule {
  tests: Dictionary<TestModel[]> = {};

  get newTest() {
    return {
      id: NaN,
      name: '',
      description: '',
      questions: [],
      points: NaN,
      test_mode: '',
      is_hidden: true,
    } as TestModel
  }

  @Action
  async fetchTestsByLessonId(id: number) {
    return this.tests[id];
  }

  @Mutation
  addTest(test: TestModel, id: number) {
    if (this.tests[id])
      this.tests[id].push(test);
    else {
      const t: Array<TestModel> = [];
      t.push(test);
      this.tests[id] = t;
    }
  }
}

export default getModule(TestModule);
