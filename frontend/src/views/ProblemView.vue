<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-10">
        <br>
        <h3> Задание {{ problem.id }}. {{ problem.name }} </h3>
        <h4> Описание: {{ problem.description }} </h4>
        <br>
      </div>
      <div class="bx--col-lg-6">
        <ul>
          <li v-for="todo in submits" :key="todo.id">
            <h5> Check submit number {{todo.id}} </h5>
          </li>
        </ul>
      </div>
      <div class="bx--col-lg-10">
        <label>
          <textarea
            v-model="areaData"
            id="text"
            cols="130"
            placeHolder="Сюда кодить надо"
            rows="20">
          </textarea>
        </label>
        <cv-button v-on:click="buttonHandler"> Print in log</cv-button>
        <cv-dropdown
          :placeholder="'Выберите язык программирования'"
          :value="value">
          <cv-dropdown-item value="YoptaScript">YoptaScript</cv-dropdown-item>
          <cv-dropdown-item value="Lolcat">LOLCODE</cv-dropdown-item>
          <cv-dropdown-item value="Brainfuck">Brainfuck</cv-dropdown-item>
        </cv-dropdown>
      </div>
    </div>
  </div>
</template>

<!--  TODO: need to improve list of user`s pushes -->
<!-- TODO: (add style (probably, tag?) and links like: press tag -> label.text = text of submit -->

<script lang="ts">

import Component from 'vue-class-component';
import Problem from '@/components/Problem.vue';
import Vue from 'vue';
import { mainStore } from '@/store';

@Component({ components: { Problem } })
export default class ProblemView extends Vue {
  private store = mainStore;
  public areaData = '';
  private submits = [];
  nextTodoId = 1;
  problemsArray = this.store.getProblems;

  get problem() {
    return this.problemsArray[0];
  }
  buttonHandler() {
    this.submits.push({
      id: this.nextTodoId,
      title: this.areaData,
    })
    this.nextTodoId++;
    console.log(this.submits);
  }


}
</script>
<!--    TODO: solve a problem w/ getting single problem from array -->

<style scoped>

</style>
