<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-10">
        <br>
        <h3> Задание {{ problem.id }}. {{ problem.name }}
          <cv-button class="rejected" kind="danger" size="small" v-on:click="rejectHandler">Rejected</cv-button> /
          <cv-button class="accepted" kind="secondary" size="small" v-on:click="acceptHandler">Accepted</cv-button>
        </h3>

        <h4> Описание: {{ problem.description }} </h4>
        <br>
        <label>
          <textarea
            v-if="problem.completed == false"
            v-model="areaData"
            id="text"
            cols="130"
            placeHolder="Сюда кодить надо"
            rows="20">
          </textarea>
          <textarea
            v-else
            cols="130"
            rows="20">
          </textarea>

          <!-- TODO: if complited -> textarea.value = last submit text -->

        </label>
        <div>
          <br>
          <cv-dropdown
            :placeholder="'Выберите язык программирования'"
            :items="problem.language">
          </cv-dropdown>
          <br>
          <cv-button v-on:click="buttonHandler" v-if="problem.completed == false"> Submit! </cv-button>
          <cv-button v-on:click="buttonHandler" v-else disabled="true"> Submit! </cv-button>
        </div>
      </div>
      <div class="bx--col-lg-3">
        <br>
        <ul>
          <li v-for="sub in submits" :key="sub.id">
            <cv-tile light>
              <cv-button size="small" kind="ghost" v-if="problem.completed == false" v-on:click="submitHandler(sub.id)"> <h5> Sub #{{sub.id}} </h5> </cv-button>
              <cv-button size="small" kind="ghost" v-else disabled="true" v-on:click="submitHandler(sub.id)"> <h5> Sub #{{sub.id}} </h5> </cv-button>
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
          <!-- TODO: normal student name realisation -->
        </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Problem from '@/components/Problem.vue';
import { mainStore } from '@/store';
import { Prop, Vue, Component } from 'vue-property-decorator';

@Component({ components: { Problem } })
export default class ProblemView extends Vue {
  private store = mainStore;
  studentsArray = this.store.getUsers;
  public areaData = '';
  private submits: object [] = [];
  submitCounter = 1;
  problemsArray = this.store.getProblems;
  @Prop() problemId!: number;

  get problem() {
    return this.problemsArray[0];
  }

  submitHandler(idSub: number) {
    const submit = this.submits[idSub - 1];
    this.areaData = Object.values(submit)[1];
    console.log(Object.values(submit)[1])
  }
  acceptHandler (){
    this.problem.completed = true;
  }
  rejectHandler (){
    this.problem.completed = false;
  }
  buttonHandler() {
    if (this.areaData !== ''){
      this.submits.push({
        id: this.submitCounter,
        title: this.areaData,
      })
      this.submitCounter++;
      console.log(this.submits)
    } else {
     alert('Type some code!')
    }
  }


}
</script>
<!--    TODO: solve a problem w/ getting single problem from array -->

<style scoped lang="stylus">
.accepted{
  background: #2ea92e;
  border-radius: 25px;
}
.rejected{
  background: #cd1d1d;
  border-radius: 25px;
}
</style>
