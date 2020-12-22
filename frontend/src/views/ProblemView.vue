<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-10">
        <br>
        <h3> Задание {{ problem.id }}. {{ problem.name }}
          <cv-button kind="secondary" size="small">Accept</cv-button>
          <cv-button kind="danger" size="small">Reject</cv-button> </h3>

        <!-- TODO: "Accept" button color: grey -> green -->

        <h4> Описание: {{ problem.description }} </h4>
        <br>
        <label>
          <textarea
            v-model="areaData"
            id="text"
            cols="130"
            placeHolder="Сюда кодить надо"
            rows="20">
          </textarea>
        </label>
        <div>
          <br>
          <cv-dropdown
            :placeholder="'Выберите язык программирования'"
            :value="value">
            <cv-dropdown-item value="YoptaScript">YoptaScript</cv-dropdown-item>
            <cv-dropdown-item value="Lolcat">LOLCODE</cv-dropdown-item>
            <cv-dropdown-item value="Brainfuck">Brainfuck</cv-dropdown-item>
          </cv-dropdown>
          <br>
          <cv-button v-on:click="buttonHandler"> Submit! </cv-button>
        </div>
      </div>
      <div class="bx--col-lg-3">
        <br>
        <ul>
          <li v-for="sub in submits" :key="sub.id">
            <cv-tile light>
              <cv-button size="small" kind="ghost"> <h5> Sub #{{sub.id}} </h5> </cv-button>
            </cv-tile>
          </li>
        </ul>
      </div>
      <div class="bx--col-lg-3">
        <br>
        <ul>
        <li v-for="sub in submits" :key="sub.id">
        <cv-tile light>
          <cv-button size="small" kind="ghost"> <h5> Student: {{studentsArray[Math.floor(Math.random() * 2)].name}} </h5> </cv-button>
        </cv-tile>
          <!-- TODO: students submit realisation -->
        </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<!-- TODO: links like: press tag -> label.text = text of submit -->

<script lang="ts">

import Component from 'vue-class-component';
import Problem from '@/components/Problem.vue';
import Vue from 'vue';
import { mainStore } from '@/store';

@Component({ components: { Problem } })
export default class ProblemView extends Vue {
  private store = mainStore;
  studentsArray = this.store.getUsers;
  public areaData = '';
  private submits: object [] = [];
  submitCounter = 1;
  problemsArray = this.store.getProblems;

  get problem() {
    return this.problemsArray[0];
  }
  buttonHandler() {
    if (this.areaData !== ''){
      this.submits.push({
        id: this.submitCounter,
        title: this.areaData,
      })
      this.submitCounter++;
    } else {
     alert('Type some code!')
    }
  }


}
</script>
<!--    TODO: solve a problem w/ getting single problem from array -->

<style scoped>

</style>
