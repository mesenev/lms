<template>
  <div class="bx--grid">
    <div class="problem-view">
      <cv-inline-notification
        v-if="showNotification"
        @close="hideSuccess"
        :kind="notificationKind"
        :sub-title="notificationText"
      />
        <div class="problem bx--row">
          <div class="bx--col-lg-8">
            <h3 class="problem-name">Задание {{ problem.id }}. {{ problem.name }}</h3>
            <h4 class="problem-description">Описание: {{ problem.description }}</h4>
          </div>
        </div>
        <div class="problem-solution bx--row">
          <div
            class="code"
            :class="[isStaff ? 'bx--col-lg-8' : 'bx--col-lg-10']"
          >
            <cv-text-area
              light
              :class="{ 'text-area-teacher': isStaff, 'text-area-student': !isStaff }"
              :disabled="isCompleted || isStaff"
              v-model="submitEdit.content"
            >
            </cv-text-area>
            <cv-dropdown
              v-if="!isStaff && problem.language"
              placeholder="Выберите язык программирования"
              :items="problem.language"
            >
            </cv-dropdown>
            <cv-button
              v-if="!isStaff"
              v-on:click="confirmSubmit"
              class="submit-btn"
              :disabled="!canSubmit"
            >
              Submit!
            </cv-button>
            <div class="handlers" v-if="isStaff">
              <cv-button class="submit-btn rejected"
                         :disabled="this.submit.status === 'WA' || isNewSubmit"
                         v-on:click="rejectSubmit">
                Rejected
              </cv-button>
              <cv-button class="submit-btn accepted"
                         :disabled="this.submit.status === 'OK' || isNewSubmit"
                         v-on:click="acceptSubmit">
                Accepted
              </cv-button>
            </div>
          </div>
          <div
            class="submit"
            :class="[isStaff ? 'bx--col-lg-8' : 'bx--col-lg-6']"
          >
              <cv-structured-list
                class="submit-list"
                v-if="submits.length !== 0"
                selectable
                condensed
                @change="changeCurrentSubmit"
              >
                <template slot="headings">
                  <cv-structured-list-heading>
                    id
                  </cv-structured-list-heading>
                  <cv-structured-list-heading>
                    Статус
                  </cv-structured-list-heading>
                </template>
                <template slot="items">
                  <cv-structured-list-item
                    v-for="submit in submits"
                    :key="submit.id"
                    :value="submit.id.toString()"
                    name="submit"
                    :checked="submit.id === Math.max(...submits.map(s => s.id))"
                  >
                    <cv-structured-list-data>
                      {{ submit.id }}
                    </cv-structured-list-data>
                    <cv-structured-list-data>
                      <cv-tag :kind="statusColor(submit.status)"
                              :label="submit.status">
                      </cv-tag>
                    </cv-structured-list-data>
                  </cv-structured-list-item>
                </template>
              </cv-structured-list>
              <cv-tile
                v-else
                class="submit-list no-submits"
                kind="standard"
              >
                <h2>Oops</h2>
                <p>Пока ничего не отправлено :(</p>
              </cv-tile>
              <cv-structured-list
                  v-if="isStaff"
                  class="student-list"
                  selectable
                  condensed
                  @change="changeStudent"
                >
                  <template slot="headings">
                    <cv-structured-list-heading>
                      Ученик
                    </cv-structured-list-heading>
                  </template>
                  <template slot="items">
                    <cv-structured-list-item
                      v-for="student in students"
                      :key="student.id"
                      :value="student.id.toString()"
                      name="student"
                      :checked="student.id === Math.min(...students.map(s => s.id))"
                    >
                      <cv-structured-list-data>
                        <cv-tag :label="`img`" kind="gray"></cv-tag>
                        {{
                          student.first_name && student.last_name ?
                          student.first_name + ' ' + student.last_name :
                          student.username
                        }}
                      </cv-structured-list-data>
                    </cv-structured-list-item>
                  </template>
                </cv-structured-list>
          </div>
        </div>
    </div>
  </div>
</template>

<script lang="ts">
import { problemStore, submitStore, userStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';
import SubmitModel from '@/models/SubmitModel';
import axios, { AxiosError, AxiosResponse } from 'axios';
import _ from 'lodash';
import ProblemModel from '@/models/ProblemModel';
import UserModel from '@/models/UserModel';


// ToDo write all submit`s status associations
const statusAssociations: { [index: string]: string } = {
  'WA': 'red',
  'OK': 'green',
  'NP': 'gray',
};


@Component
export default class ProblemView extends Vue {
  @Prop() problemId!: number;

  private problemStore = problemStore;

  private userStore = userStore;

  private submitStore = submitStore;

  private user = this.userStore.user;

  private readonly defaultSubmitStatus = 'NP';

  private readonly courseId = Number(this.$route.params.courseId);

  private defaultSubmit: SubmitModel = {
    id: NaN,
    problem: this.problemId,
    student: { ...userStore.user },
    content: '',
    status: '',
  }

  get problem(): ProblemModel {
    return problemStore.currentProblem;
  }

  get isStaff(): boolean {
    return this.user.staff_for.includes(Number(this.courseId));
  }

  async changeStudent(id: string | number) {
    await this.submitStore.fetchSubmits({
      problemId: this.problemId,
      userId: Number(id),
    });
    this.submit = { ...this.defaultSubmit };
    this.submitEdit = { ...this.submit };
    if (!_.isEmpty(this.submits)) {
      this.changeCurrentSubmit(this.getLastSubmit().id);
    }
  }

  get submits(): SubmitModel[] {
    return this.submitStore.submits;
  }

  getLastSubmit(): SubmitModel {
    return this.submits[this.submits.length - 1];
  }

  private students: UserModel[] = [];

  private submit: SubmitModel = this.defaultSubmit;

  async created() {
    const problem = await this.problemStore.fetchProblemById(this.problemId);
    if (problem) {
      this.problemStore.setCurrentProblem(problem);
    }

    if (this.isStaff) {
      await userStore.fetchStudentsByCourseId(this.courseId)
        .then(students => this.students = students);

      if (!_.isEmpty(this.students)) {
        await this.submitStore.fetchSubmits({
          problemId: this.problemId,
          userId: this.students[0].id,
        })
      }
    } else {
      await this.submitStore.fetchSubmits({
        problemId: this.problemId,
        userId: this.user.id
      });
    }

    if (!_.isEmpty(this.submits)) {
      this.changeCurrentSubmit(this.getLastSubmit().id);
    }
  }

  public submitEdit: SubmitModel = { ...this.submit };

  patchSubmit(status: string) {
    if (this.isNewSubmit) {
      console.error('Submit does not exists!');
      return;
    }

    this.submitEdit = { ...this.submitEdit, status };

    axios.patch(`http://localhost:8000/api/submit/${this.submitEdit.id}/`, this.submitEdit)
      .then((response: AxiosResponse) => {
        this.submitStore.changeSubmitStatus(response.data);
        this.submit = { ...response.data };
        this.submitEdit = { ...this.submit };
        if (response.data.status === 'OK') {
          this.problemStore.fetchProblemById(this.problemId);
          this.problem.completed = true;
        }
        this.notificationKind = 'success';
        this.notificationText = `Работа оценена: ${status}`;
      })
      .catch((error: AxiosError) => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так ${error.message}`
      })
      .finally(() => this.showNotification = true);
  }

  acceptSubmit() {
    this.patchSubmit('OK');
  }

  rejectSubmit() {
    this.patchSubmit('WA');
  }

  confirmSubmit() {
    if (this.isNewSubmit) {
      delete this.submitEdit.id;
    }
    this.submitEdit = { ...this.submitEdit, status: this.defaultSubmitStatus };
    axios.post('http://localhost:8000/api/submit/', this.submitEdit)
      .then((response: AxiosResponse<SubmitModel>) => {
        this.submitStore.addSubmitToArray(response.data);
        this.submit = { ...response.data };
        this.submitEdit = { ...this.submit };
        this.notificationKind = 'success';
        this.notificationText = 'Попытка отправлена';
      })
      .catch((error: AxiosError) => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так ${error.message}`;
      })
      .finally(() => this.showNotification = true);
  }

  changeCurrentSubmit(id: string | number) {
    const _id = Number(id);
    this.submit = this.submits.find((submit) => {
      return submit.id === _id;
    }) || this.submit;
    this.submit = { ...this.submit };
    this.submitEdit = { ...this.submit };
  }

  get isNewSubmit(): boolean {
    return isNaN(this.submitEdit.id);
  }

  get isChanged(): boolean {
    return !_.isEqual(this.submit, this.submitEdit);
  }

  get isCompleted(): boolean {
    return !!this.submits.find((submit: SubmitModel) => (
      submit.status === 'OK'
    ));
  }

  get canSubmit(): boolean {
    return (
      !this.isCompleted &&
      this.submitEdit.content?.length !== 0 &&
      this.isChanged
    );
  }

  statusColor(status: string): string {
    return statusAssociations[status] || 'gray';
  }

  showNotification = false;

  notificationKind = 'success';

  notificationText = '';

  hideSuccess() {
    this.showNotification = false;
  }
}
</script>
<!--    TODO: solve a problem w/ getting single problem from array -->

<style lang="stylus">
.problem
  margin-bottom 1rem

.name
  display flex
  flex-direction row
  justify-content space-between
  align-items center

.submit-list, .student-list
  margin 0
  padding 0

.student-list
  margin-left 1rem

.submit-btn, .handlers button
  margin-top 1rem

.code
  width 100%

.submit
  display flex
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.problem-solution
  height 100%

.no-submits
  width 100%
  padding 0
  margin 0
  background-color inherit

.accepted, .rejected
  transition ease-in-out 0.25s

.accepted
  background-color var(--cds-inverse-support-02)
  &:hover
    background-color: var(--cds-support-02)

.rejected
  background-color var(--cds-inverse-support-01)
  &:hover
    background-color: var(--cds-support-01)

.text-area-teacher textarea:disabled
  cursor pointer
  color #000
  border-bottom: 1px solid transparent

.problem-view
  margin-top: 2rem

.handlers
  button:nth-child(2n)
    margin-left 5px

.code
  .bx--text-area
    height 30em
    //width 45rem
  .bx--label,
  .bx--label--disabled
    display none

</style>
