import MaterialModel from '@/models/MaterialModel';
import store from '@/store';
import axios from 'axios';
import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'material', store, dynamic: true })
class MaterialModule extends VuexModule {

  _materials: Array<MaterialModel> = [];

  get materials(): Array<MaterialModel> {
    return this._materials;
  }

  private _currentMaterial: MaterialModel = {...this.getNewMaterial};

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
  setMaterials(payload: Array<MaterialModel>) {
    this._materials = payload;
  }

  @Mutation
  addMaterialToArray(element: MaterialModel) {
    this._materials.push(element);
    this._materials = [...this._materials];
  }

  @Mutation
  setCurrentMaterial(material: MaterialModel) {
    this._currentMaterial = material;
  }

  @Action
  async fetchMaterialById(id: number): Promise<MaterialModel> {
    let answer = {data: {}};
    await axios.get(`http://localhost:8000/api/material/${id}/`)
      .then(response => answer = response)
      .catch(error => {
        console.log(error);
      })
    return answer.data as MaterialModel;
  }
}

export default getModule(MaterialModule);
