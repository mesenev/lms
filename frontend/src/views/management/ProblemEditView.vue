<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-10">
        <br>
        <h4>Название</h4>
        <input :class="`bx--text-input`"
               type="text"
               v-model="problemTitle">
        <cv-button class="change__btn"
                   :disabled="canChangeProblemName"
                   @click="ChangeProblemName">
          Сменить название
        </cv-button>
        <br>
        <h4>Описание</h4>
        <cv-text-area v-model="problemDescription"
        ></cv-text-area>
        <cv-button class="change__btn"
                   :disabled="canChangeProblemDescription"
                   @click="ChangeProblemDescription">
          Сменить описание
        </cv-button>
        <h4>Языки решения</h4>
        <div>
          <br>
          <cv-multi-select label="Доступные языки"
                           v-model="problemLanguages"
                           :options="availableLanguages">
          </cv-multi-select>
          <h5>Выбраны сейчас:</h5>
          <cv-list>
            <cv-list-item v-for="l in problem.language" :key="l">{{ l }}</cv-list-item>
          </cv-list>
          <br>
          <cv-button class="change__btn"
                     :disabled="canChangeProblemLanguage"
                     @click="ChangeProblemLanguage">
            Изменить
          </cv-button>
        </div>
      </div>
      <div class="bx--col-lg-3">
        <cv-toggle value="problem.manual"
                   v-model="problemManual"
                   label="Ручная проверка"
        ></cv-toggle>
        <cv-button class="change__btn"
                   :disabled="canChangeProblemManual"
                   @click="ChangeProblemManual">
          Изменить
        </cv-button>
      </div>
      <div class="bx--col-lg-3">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Problem from '@/components/Problem.vue';
import { problemStore } from '@/store';
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Problem } })
export default class ProblemEditView extends Vue {
  private store = problemStore;
  problemsArray = this.store.problems;

  @Prop() problemId!: number;

  get problem() {
    return this.problemsArray[0];
  }

  availableLanguages = [
    {
      name: 'python',
      label: 'python',
      value: 'python',
    },
    {
      name: 'c/c++',
      label: 'c/c++',
      value: 'c/c++',
    },
  ];

  //v-modals
  problemTitle: string = this.problem.name;
  problemDescription: string = this.problem.description;
  problemManual: boolean = this.problem.manual;
  problemLanguages: Array<string> | null = this.problem.language;

  get canChangeProblemName() {
    return this.problem.name === this.problemTitle;
  }

  get canChangeProblemDescription() {
    return (this.problem.description || '') === this.problemDescription;
  }

  get canChangeProblemManual() {
    return this.problem.manual === this.problemManual;
  }

  get canChangeProblemLanguage() {
    return _.isEqual(this.problem.language, this.problemLanguages)
  }

  ChangeProblemName() {
    //
  }

  ChangeProblemDescription() {
    //
  }

  ChangeProblemManual() {
    //
  }

  ChangeProblemLanguage() {
    //
  }


}
</script>
<!--    TODO: solve a problem w/ getting single problem from array -->

<style scoped lang="stylus">

</style>
