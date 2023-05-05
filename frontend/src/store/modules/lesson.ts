import LessonModel from '@/models/LessonModel';
import store from '@/store';
import api from '@/store/services/api'
import {Dictionary} from 'vue-router/types/router';
import {Action, getModule, Module, Mutation, VuexModule} from 'vuex-module-decorators';

@Module({
  namespaced: true,
  name: 'lesson',
  store,
  dynamic: true,
})
class LessonModule extends VuexModule {

  currentLesson: LessonModel | null = null;
  lessonsByCourse: Dictionary<LessonModel[]> = {};

  @Mutation
  setLessons(payload: Dictionary<LessonModel[]>) {
    this.lessonsByCourse = { ...this.lessonsByCourse, ...payload };
  }

  @Mutation
  changeCurrentLesson(payload: LessonModel | null) {
    this.currentLesson = payload;
  }

  @Mutation
  changeLessonVisibility(lesson: LessonModel) {
    const curLesson = this.lessonsByCourse[lesson.course].find(el => el.id === lesson.id);
    if (curLesson != undefined) {
      curLesson.is_hidden = lesson.is_hidden;
    }
  }

  @Action({rawError: true})
  async deleteLesson(id: number) {
    await api.delete(`/api/lesson/${id}/`);
  }

  @Action
  async fetchLessonById(id: number): Promise<LessonModel> {
    let answer = { data: {} };
    await api.get(`/api/lesson/${id}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as LessonModel;
  }

  get getNewLesson(): LessonModel {
    return {
      id: NaN,
      course: NaN,
      name: '',
      description: '',
      lessonContent: '',
      problems: [],
      exams: [],
      materials: [],
      deadline: '2000-01-01',
      progress: [],
      scores: {},
      is_hidden: true,
      is_control_work: false,
    } as LessonModel;
  }

  @Action
  async fetchLessonsByCourseId(id: number): Promise<LessonModel[]> {
    if (id in this.lessonsByCourse) { return this.lessonsByCourse[id]; }

    let answer = { data: {} };
    await api.get('/api/lesson/', { params: { course_id: id } })
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    const result = answer.data as Array<LessonModel>;
    this.setLessons({ [id]: result })
    return result;
  }

  @Action
  async patchLesson(params: { is_hidden: boolean; id: number }) {

    let answer = { data: {} };
    await api.patch(`/api/lesson/${params.id}/`, { ...params })
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    const result = answer.data as LessonModel;
    this.changeCurrentLesson(result);
    this.changeLessonVisibility(result);
    return result;
  }
}

export default getModule(LessonModule);
