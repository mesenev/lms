import { Action, getModule, Module, Mutation, VuexModule } from "vuex-module-decorators";
import store from "@/store";
import { Dictionary } from "vue-router/types/router";
import TestModel from "@/models/TestModel";

@Module({ namespaced: true, name: 'test', store, dynamic: true })
class TestModule extends VuexModule {
  tests: Dictionary<TestModel[]> = {};

  currentTest: TestModel | null = null;

  get newTest() {
    return {
      id: NaN,
      name: '',
      lesson: NaN,
      description: '',
      questions: [],
      points: NaN,
      test_mode: '',
      is_hidden: true,
    } as TestModel;
  }

  @Action
  async fetchTestsByLessonId(id: number) {
    return this.tests[id];
  }

  @Action
  fetchTestById(id: number): TestModel {
    return {
      id: 5,
      name: 'Test',
      description: 'Desc',
      questions: [
        {
          id: 1,
          question: 'Вопрос для поля ввода',
          test: 5,
          description: 'Описание отсутствует',
          answer_type: 'input',
          answers: [],
          correct_answers: ['5'],
          attachment_file: '',
          points: 5,
        },
        {
          id: 2,
          question: 'Выделите нечетное число',
          test: 5,
          description: 'Тут написано что то',
          answer_type: 'radio',
          answers: ['1', '4', '5'],
          correct_answers: ['5'],
          attachment_file: '',
          points: 5,
        },
        {
          id: 3,
          question: 'Выделите оценки Хорошо и Удовлетворительно',
          test: 5,
          description: 'Интересный факт про оценки',
          answer_type: 'checkbox',
          answers: ['1', '3', '4', '5'],
          correct_answers: ['3', '4'],
          attachment_file: '',
          points: 5,
        },
        {
          id: 5,
          question: 'Определение строки',
          test: 5,
          description: 'Описания нету',
          answer_type: 'text',
          answers: [],
          correct_answers: ['набор символов'],
          attachment_file: '',
          points: 5,
        },
      ],
      points: 10,
      test_mode: 'manual',
      is_hidden: true,
    } as TestModel;
  }

  @Mutation
  changeCurrentTest(payload: TestModel | null) {
    this.currentTest = payload;
  }

  @Mutation
  setTests(payload: Dictionary<TestModel[]>) {
    this.tests = { ...this.tests, ...payload };
  }

  @Action
  async patchTest(params: { is_hidden: boolean; id: number }) {
    return;
  }
}

export default getModule(TestModule);
