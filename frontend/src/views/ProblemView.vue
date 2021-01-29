<template>
  <cv-grid class="problem-view">
    <cv-row>
      <div class="header-wrapper">
        <h2>{{ problem.name }}</h2>
      </div>
    </cv-row>
    <cv-row>
      <cv-inline-notification
        v-if="showNotification"
        @close="hideSuccess"
        :kind="notificationKind"
        :sub-title="notificationText"
      />
    </cv-row>
    <cv-row>
      <cv-column :lg="8">
        <div class="item">
          <ProblemDescription v-if="!isNaN(problem.id)" :problem="problem"/>
          <cv-skeleton-text v-else/>
        </div>
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column :lg="8">
        <div class="item">
          <h5>Решение</h5>
          <cv-text-area
            v-model="submitEdit.content"
            :class="{ 'text-area-teacher': isStaff, 'text-area-student': !isStaff }"
            :disabled="isCompleted || isStaff"
            light>
          </cv-text-area>
          <cv-dropdown
            v-if="!isStaff && problem.language"
            :items="problem.language"
            placeholder="Выберите язык программирования">
          </cv-dropdown>
          <cv-button
            v-if="!isStaff"
            :disabled="!canSubmit"
            class="submit-btn"
            v-on:click="confirmSubmit">
            Submit!
          </cv-button>
          <div v-if="isStaff" class="handlers">
            <cv-button :disabled="isNewSubmit" class="submit-btn rejected" v-on:click="rejectSubmit">
              Rejected
            </cv-button>
            <cv-button :disabled="isNewSubmit" class="submit-btn accepted" v-on:click="acceptSubmit">
              Accepted
            </cv-button>
          </div>
        </div>
      </cv-column>
      <cv-column :lg="3" class="submit">
        <div class="item">
          <cv-structured-list
            v-if="submits.length !== 0"
            class="submit-list"
            condensed selectable
            @change="changeCurrentSubmit">
            <template slot="headings">
              <cv-structured-list-heading>id</cv-structured-list-heading>
              <cv-structured-list-heading>Статус</cv-structured-list-heading>
            </template>
            <template slot="items">
              <cv-structured-list-item
                v-for="submit in submits"
                :key="submit.id"
                :checked="submit.id === Math.max(...submits.map(s => s.id))"
                :value="submit.id.toString()"
                name="submit">
                <cv-structured-list-data>{{ submit.id }}</cv-structured-list-data>
                <cv-structured-list-data>
                  <cv-tag :kind="statusColor(submit.status)" :label="submit.status"/>
                </cv-structured-list-data>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
          <cv-tile v-else class="submit-list no-submits" kind="standard">
            <h2>Oops</h2>
            <p>Пока ничего не отправлено :(</p>
          </cv-tile>
        </div>
      </cv-column>
      <cv-column v-if="isStaff">
        <div class="item">
          <cv-structured-list
            class="student-list"
            condensed selectable
            @change="changeStudent">
            <template slot="headings">
              <cv-structured-list-heading>
                Ученик
              </cv-structured-list-heading>
            </template>
            <template slot="items">
              <cv-structured-list-item
                v-for="student in students"
                :key="student.id"
                :checked="student.id === Math.min(...students.map(s => s.id))"
                :value="student.id.toString()"
                name="student">
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
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts">
import ProblemDescription from "@/components/ProblemDescription.vue";
import ProblemModel from '@/models/ProblemModel';
import SubmitModel from '@/models/SubmitModel';
import UserModel from '@/models/UserModel';
import { problemStore, submitStore, userStore } from '@/store';
import axios, { AxiosError, AxiosResponse } from 'axios';
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';

// ToDo write all submit`s status associations
const statusAssociations: { [index: string]: string } = {
  'WA': 'red',
  'OK': 'green',
  'NP': 'gray',
};


@Component({ components: { ProblemDescription } })
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
        userId: this.user.id,
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
.item
  background-color var(--cds-ui-background)
  padding 1rem

.bx--row
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

.text-area-student
.text-area-teacher
  border 1px solid black

.text-area-teacher textarea:disabled
  cursor pointer
  color #000

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
