import { Action, getModule, Module, Mutation, VuexModule } from "vuex-module-decorators";
import store from "@/store";
import { Dictionary } from "vue-router/types/router";
import ExamModel from "@/models/ExamModel";
import api from "@/store/services/api";
import QuestionModel from "@/models/QuestionModel";

@Module({ namespaced: true, name: 'exam', store, dynamic: true })
class ExamModule extends VuexModule {
  examsByLesson: Dictionary<ExamModel[]> = {};

  currentExam: ExamModel | null = null;

  get newExam() {
    return {
      id: NaN,
      name: '',
      lesson: NaN,
      description: '',
      questions: [],
      points: 0,
      test_mode: '',
      is_hidden: true,
    } as ExamModel;
  }

  @Action
  async fetchExamsByLessonId(id: number): Promise<ExamModel[]> {
    if (id in this.examsByLesson) {
      return this.examsByLesson[id];
    }
    let answer = { data: {} };
    await api.get('/api/exam/', { params: { lesson_id: id } })
        .then(response => answer = response)
        .catch(error => {
          console.log(error);
        });
    const result = answer.data as Array<ExamModel>;
    this.setExams({ [id]: result });
    return result;
  }

  @Action
  async fetchExamById(id: number): Promise<ExamModel> {
    let answer = { data: {} };
    await api.get(`/api/exam/${id}/`)
        .then(response => answer = response)
        .catch(error => {
          console.log(error);
        });
    return answer.data as ExamModel;
  }

  @Mutation
  changeCurrentExam(payload: ExamModel | null) {
    this.currentExam = payload;
  }

  @Mutation
  changeExamVisibility(test: ExamModel) {
    const curTest = this.examsByLesson[test.lesson].find(el => el.id === test.id);
    if (curTest != undefined) {
      curTest.is_hidden = test.is_hidden;
    }
  }

  @Mutation
  setExams(payload: Dictionary<ExamModel[]>) {
    this.examsByLesson = { ...this.examsByLesson, ...payload };
  }

  @Action
  async patchExam(params: { is_hidden: boolean; id: number }) {
    let answer = { data: {} };
    await api.patch(`/api/exam/${params.id}/`, { ...params })
        .then(response => answer = response)
        .catch(error => {
          console.log(error);
        });
    const result = answer.data as ExamModel;
    this.changeCurrentExam(result);
    this.changeExamVisibility(result);
    return result;
  }
}

export default getModule(ExamModule);
