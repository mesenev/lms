<template>
  <div class="bx--grid">
    <div class="bx--row problem-view">
      <div class="bx--col-lg-8">
        <cv-inline-notification
          v-if="showNotification"
          @close="hideSuccess"
          :kind="notificationKind"
          :sub-title="notificationText"
        />
        <div class="problem">
          <div class="name">
            <h3> Задание {{ problem.id }}. {{ problem.name }}</h3>
            <!-- TODO handlers are visible if user.status === teacher -->
            <div class="handlers">
              <cv-button class="rejected"
                         kind="danger"
                         size="small"
                         :disabled="this.submit.status === 'WA' || isNewSubmit"
                         v-on:click="rejectSubmit">
                Rejected
              </cv-button>
              <cv-button class="accepted"
                         kind="secondary"
                         size="small"
                         :disabled="this.submit.status === 'OK' || isNewSubmit"
                         v-on:click="acceptSubmit">
                Accepted
              </cv-button>
            </div>
          </div>
          <div class="description">
            <h4>Описание: {{ problem.description }}</h4>
          </div>
          <div class="submit">
            <cv-text-area
              light
              class="code-text-area"
              label="Code..."
              :disabled="isCompleted"
              v-model="submitEdit.content">
            </cv-text-area>
            <cv-dropdown
              v-if="problem.language"
              placeholder="Выберите язык программирования"
              :items="problem.language">
            </cv-dropdown>
            <cv-button v-on:click="confirmSubmit"
                       class="submit-btn"
                       :disabled="!canSubmit">
              Submit!
            </cv-button>
          </div>
        </div>
      </div>
      <div class="bx--col-lg-8">
        <cv-structured-list
          v-if="submits.length !== 0"
          light
          selectable
          @change="changeCurrentSubmit"
        >
          <template slot="headings">
            <cv-structured-list-heading>
              <!-- ToDo choose user  -->
              <cv-dropdown placeholder="Выберите ученика"  :items="['dsa']">

              </cv-dropdown>
            </cv-structured-list-heading>
            <cv-structured-list-heading>
              Status
            </cv-structured-list-heading>
          </template>
          <template slot="items">
            <cv-structured-list-item
              v-for="sub in submits"
              :key="sub.id"
              :value="sub.id.toString()"
              name="submit"
            >
              <cv-structured-list-data>
                {{ sub.student.username }}
              </cv-structured-list-data>
              <cv-structured-list-data>
                <cv-tag :kind="statusColor(sub.status)"
                        :label="sub.status">
                </cv-tag>
              </cv-structured-list-data>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Problem from '@/components/Problem.vue';
import { problemStore, userStore, submitStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';
import SubmitModel from '@/models/SubmitModel';
import axios, {AxiosError, AxiosResponse} from "axios";
import _ from 'lodash';
import ProblemModel from "@/models/ProblemModel";


// ToDo write all submit`s status associations
const statusAssociations: { [index: string]: string } = {
  'WA': 'red',
  'OK': 'green',
  'NP': 'gray',
};


@Component({ components: { Problem } })
export default class ProblemView extends Vue {
  @Prop() problemId!: number;

  private problemStore = problemStore;

  private userStore = userStore;

  private submitStore = submitStore;

  private readonly defaultSubmitStatus = 'NP';

  get problem(): ProblemModel {
    return this.problemStore.currentProblem;
  }

  get submits(): SubmitModel[] {
    return this.submitStore.submits.filter((submit) => {
      return submit.problem === this.problemId;
    });
  }

  private submit: SubmitModel = {
    id: NaN,
    problem: this.problemId,
    student: {...userStore.user},
    content: '',
    status: '',
  }

  async created() {
    await this.problemStore.fetchProblemById(this.problemId);
    await this.submitStore.fetchSubmits();
    if (!_.isEmpty(this.submits)) {
      this.submit = { ...this.submits[this.submits.length - 1] };
      this.submitEdit = { ...this.submit };
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
      .then((response) => {
        this.submitStore.changeSubmitStatus(response.data);
        this.submit = { ...response.data };
        this.submitEdit = { ...this.submit };
        if (response.data.status === 'OK') {
          this.problemStore.fetchProblemById(this.problemId);
          this.problem.completed = true;
        }
        this.notificationKind = 'success';
        this.notificationText = 'Работа оценена';
      })
      .catch(error => {
        console.error(error)
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

  changeCurrentSubmit(id: string) {
    const _id = Number(id);
    this.submit = this.submits.find((submit) => {
      return submit.id === _id;
    }) || this.submit;
    this.submit = { ...this.submit };
    this.submitEdit = { ...this.submit };
  }

  get isNewSubmit(): boolean {
    return _.isEmpty(this.submitEdit.status);
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
.name
  display flex
  flex-direction row
  justify-content space-between
  align-items center
  .handlers button
    margin-left 5px

problem-view, .name, .description, .submit, .submit-btn
  margin 10px 0

.accepted
  border-radius 25px

.rejected
  border-radius: 25px

.code-text-area .bx--text-area
  height 20em

</style>
