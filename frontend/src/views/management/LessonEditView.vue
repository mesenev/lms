<template>
  <div class="bx--grid, head-content">
    <h1>Редактирование урока</h1>
    <div class="bx--row">
      <div class="bx--col">
        <h4>Название урока</h4>
        <input :class="`bx--text-input`"
               type="text"
               v-model="lessonTitle">
        <cv-button class="change__btn"
                   :disabled="canChangeLessonName"
                   @click="changeLessonName">
          Изменить название
        </cv-button>
      </div>
      <div class="bx--col">
        <h4>Срок окончания урока</h4>
        <cv-date-picker kind="single"
                        date-label=""
                        :cal-options="calOptions"
                        @change="actionChange"
                        v-model="modelValue">
        </cv-date-picker>
        <cv-button class="change__btn"
                   :disabled="canChangeLessonDeadline"
                   @click="changeLessonDeadline">
          Изменить срок
        </cv-button>
      </div>
      <div class="bx--col">
        <h4>Добавить материалы к уроку</h4>
        <cv-button class="add__btn"
                   @click="addMaterials">
          Добавить
        </cv-button>
      </div>
      <div class="bx--col">
        <div class="bx--col-lg-10">
          <h4>Добавить новое задание</h4>
          <cv-button class="add__problem__btn"
                     @click="addProblem">
            Добавить
          </cv-button>
        </div>
      </div>
    </div>

    <div class="bx--grid, main-content">
      <div class="bx--row row">
        <div class="bx--col">
          <h4>Классная работа:</h4>
          <cv-accordion align="align" v-for="problem in classwork" :key="problem.id">
            <div class="bx--grid, works">
              <div class="bx--row">
                <div class="bx--col, works-col">
                  <ProblemCard class="card" :problem="problem"
                               :delete-problem="deleteProblem"/>
                </div>
              </div>
            </div>
          </cv-accordion>
        </div>
        <div class="bx--col">
          <h4>Домашнаяя работа:</h4>
          <cv-accordion align="align" v-for="problem in homework" :key="problem.id">
            <div class="bx--grid, works">
              <div class="bx--row row">
                <div class="bx--col, works-col">
                  <ProblemCard class="card" :problem="problem"
                               :delete-problem="deleteProblem"/>
                </div>
              </div>
            </div>
          </cv-accordion>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import LessonCard from '@/components/LessonCard.vue';
import Problem from '@/components/Problem.vue';
import ProblemCard from "@/components/ProblemCard.vue";
import { modBStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: {
    ProblemCard,
    LessonCard, Problem,
  },
})
export default class CourseCalendarView extends Vue {
  @Prop() courseId!: number;

  store = modBStore;

  get getLesson() {
    return this.store.getLesson;
  }

  get classwork(): Array<ProblemModel> {
    return this.store.getLesson.classwork;
  }

  get homework(): Array<ProblemModel> {
    return this.store.getLesson.homework;
  }

  deleteProblem(problem: ProblemModel) {
    this.store.deleteProblem(problem);
  }


  lessonTitle: string = this.getLesson.name;
  lessonDeadline: string = this.getLesson.deadline;
}
</script>

<style scoped lang="stylus">
.head-content
  margin: 50px

.bx--col
  margin: 2rem

.works-col
  margin-right 0
  margin-bottom 1rem
  margin-left 1rem
  margin-top 1rem
  display flex

//border black 1px solid
.main-content
  border 2px black solid;
  margin: 50px

.bx--text-input
  border: 2px solid #222;
  padding: 5
  display: block;
  width: 100%;
  height: 50px;
  background: #fff;

.change__btn
  margin-top: 10px
  background-color: var(--cds-ui-05)

  &:hover
    background-color: var(--cds-ui-04)

.add__btn
  margin-top: 10px
  background-color: var($inverse-link)

.delete__btn
  &:hover
    background-color: var(--cds-ui-04)

.add__problem__btn
  margin-top: 10px
  background-color: var($support-03)
</style>
