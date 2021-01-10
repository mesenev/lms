<template>
  <div class="bx--grid">
    <div class="bx--row problem-view">
      <div class="bx--col-lg-10">
        <div class="name">
          <h3> Задание {{ problem.id }}. {{ problem.name }}</h3>
          <!-- TODO handlers are visible if user.status === teacher -->
          <div class="handlers">
            <cv-button class="rejected"
                       kind="danger"
                       size="small"
                       :disabled="!canPatch"
                       v-on:click="rejectSubmit">
              Rejected
            </cv-button>
            <cv-button class="accepted"
                       kind="secondary"
                       size="small"
                       :disabled="!canPatch"
                       v-on:click="acceptSubmit">
              Accepted
            </cv-button>
          </div>
        </div>
        <div class="description">
          <h4>Описание: {{ problem.description }}</h4>
        </div>
        <div class="submit">
          <!-- TODO: if completed -> textarea.value = last submit text -->
          <cv-text-area
            light
            class="code-text-area"
            label="Code..."
            v-model="submitEdit.content">
          </cv-text-area>
          <cv-dropdown
            placeholder="Выберите язык программирования"
            :items="problem.language">
          </cv-dropdown>
          <cv-button v-on:click="confirmSubmit"
                     class="submit-btn"
                     :disabled="!isChanged || submitEdit.content.length === 0">
            Submit!
          </cv-button>
        </div>
      </div>
      <div class="bx--col-lg-6">
        <cv-structured-list
          v-if="submits.length !== 0"
          light
          selectable
          @change="changeCurrentSubmit"
        >
          <template slot="headings">
            <cv-structured-list-heading>
              Username
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
import ProblemModel from '@/models/ProblemModel';
import SubmitModel from '@/models/SubmitModel';
import { problemStore, submitStore, userStore } from '@/store';
import axios from "axios";
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';


// ToDo write all submit`s status associations
const statusAssociations: { [index: string]: string } = {
  'WA': 'red',
  'OK': 'green',
  'NP': 'gray',
};


@Component({ components: { Problem } })
export default class ProblemView extends Vue {
  @Prop() problemId!: number;
  problem!: ProblemModel;
  loading = true;

  private store = problemStore;
  private submitStore = submitStore;

  async created() {
    this.problem = await this.store.fetchProblemById(this.problemId);
    if (_.isEmpty(this.submits)) {
      await this.submitStore.fetchSubmitsByProblemId(this.problemId);
    }
    this.loading = false;
  }


  private readonly defaultSubmitStatus = 'NP';

  get submits(): SubmitModel[] {
    return submitStore.submits;
  }

  private submit: SubmitModel = {
    id: NaN,
    problem: this.problem,
    student: {...userStore.user},
    content: '',
    status: '',
  }

  public submitEdit: SubmitModel = { ...this.submit };

  canPatch = false;

  patchSubmit(status: string) {
    if (this.isNewSubmit) {
      console.error('Submit does not exists!');
      return;
    }

    this.submitEdit = { ...this.submitEdit, status };

    axios.patch(`http://localhost:8000/api/submit/${this.submitEdit.id}/`, this.submitEdit)
      .then((response) => {
        this.submitStore.changeSubmitStatus(response.data);
        this.submit = { ...response.data, id: NaN };
        this.submitEdit = { ...this.submit };
        this.canPatch = false;
      })
      .catch(error => {
        console.error(error)
      })
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
      .then(response => {
        this.submitStore.addSubmitToArray(response.data);
        this.submit = { ...response.data };
        this.submitEdit = { ...this.submit };
        this.canPatch = true;
      })
  }

  changeCurrentSubmit(id: string) {
    const _id = Number(id);
    this.submit = this.submits.find((submit) => {
      return submit.id === _id;
    }) || this.submit;
    this.submit = { ...this.submit };
    this.submitEdit = { ...this.submit };
    this.canPatch = this.submit.status === 'NP';
  }

  get isNewSubmit(): boolean {
    return isNaN(this.submitEdit.id);
  }

  get isChanged(): boolean {
    return !_.isEqual(this.submit, this.submitEdit);
  }

  statusColor(status: string): string {
    if (statusAssociations.hasOwnProperty(status)) {
      return statusAssociations[status];
    }
    return 'gray';
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
