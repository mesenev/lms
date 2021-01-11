import LessonContent from "@/models/LessonContent";
import axios from 'axios';
import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ name: 'problem' })
export default class MaterialModule extends VuexModule {

  _materials: Array<LessonContent> = [];

  get materials(): Array<LessonContent> {
    return this._materials;
  }

  @Mutation
  setMaterials(payload: Array<LessonContent>) {
    this._materials = payload;
  }

  @Action
  async fetchMaterials() {
    await axios.get('http://localhost:8000/api/material/')
      .then(response => {
        this.setMaterials(response.data);
      })
      .catch(error => {
        console.log(error);
      })
  }

  @Mutation
  addMaterialToArray(element: LessonContent) {
    this._materials.push(element);
    this._materials = [...this._materials];
  }

  private _currentMaterial: LessonContent = {...this.getNewMaterial};

  @Mutation
  setCurrentMaterial(material: LessonContent) {
    this._currentMaterial = material;
  }

  get currentMaterial(): LessonContent {
    return this._currentMaterial;
  }

  get getNewMaterial(): LessonContent {
    return {
      id: NaN,
      lesson: NaN,
      name: 'имя',
      // eslint-disable-next-line @typescript-eslint/camelcase
      content_type: 'text',
      content: 'иям',
    };
  }

  @Action
  async fetchMaterialById(id: number): Promise<LessonContent> {
    let answer = { data: {} };
    await axios.get(`http://localhost:8000/api/material/${id}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as LessonContent;
  }
}
