import MaterialModel from '@/models/MaterialModel';
import store from '@/store';
import axios from 'axios';
import { Dictionary } from "vue-router/types/router";
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'material', store, dynamic: true })
class MaterialModule extends VuexModule {

  _materials: Dictionary<MaterialModel[]> = {};

  private _currentMaterial: MaterialModel = {...this.getNewMaterial};

  @Action
  async fetchMaterials() {
    await axios.get('/api/material/')
      .then(response => {
        this.setMaterials(response.data);
      })
      .catch(error => {
        console.log(error);
      })
  }

  get currentMaterial(): MaterialModel {
    return this._currentMaterial;
  }

  get getNewMaterial(): MaterialModel {
    return {
      id: NaN,
      lesson: NaN,
      name: 'имя',
      content_type: 'text',
      content: 'иям',
    };
  }

  @Mutation
  setMaterials(payload: Dictionary<MaterialModel[]>) {
    this._materials = payload;
  }

  @Mutation
  setCurrentMaterial(material: MaterialModel) {
    this._currentMaterial = material;
  }

  @Action
  async fetchMaterialById(id: number): Promise<MaterialModel> {
    let answer = { data: {} };
    await axios.get(`/api/material/${id}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as MaterialModel;
  }

  @Action
  async fetchMaterialsByLessonId(id: number): Promise<MaterialModel[]> {
    if (id in this._materials) {
      return this._materials[id];
    }

    let answer = { data: {} };
    await axios.get('/api/material/', { params: { lesson_id: id } })
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    const result = answer.data as Array<MaterialModel>;
    this.setMaterials({ [id]: result })
    return result;
  }
}

export default getModule(MaterialModule);
