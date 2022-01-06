<template>
  <div class="item">
    <h4 class="submit-title">Решение задачи</h4>
    <cv-inline-notification
      v-if="showNotification"
      :kind="notificationKind"
      :sub-title="notificationText"
      @close="hideNotification"/>
    <cv-skeleton-text v-if="loading"/>
    <div v-else>
      <code-editor-component v-model="submitEdit.content"/>
      <cv-dropdown
        v-model="submitEdit.de_id"
        :items="deOptions"
        :disabled="deOptions.length === 0"
        placeholder="Выберите язык программирования">
        <cv-dropdown-item v-for="de in deOptions" :key="de.value" :value="de.value">
          {{ de.name }}
        </cv-dropdown-item>
      </cv-dropdown>
      <cv-button
        v-if="!isStaff"
        :disabled="!canSubmit"
        class="submit-btn"
        v-on:click="confirmSubmit">
        Submit!
      </cv-button>
      <div v-if="isStaff" class="handlers">
        <cv-button
          :disabled="isAcceptDisabled"
          class="submit-btn accepted"
          v-on:click="acceptSubmit">
          Принять
        </cv-button>
        <cv-button
          kind='danger'
          :disabled="isRejectDisabled"
          class="submit-btn rejected"
          v-on:click="rejectSubmit">
          Отклонить
        </cv-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import CodeEditorComponent from '@/components/common/CodeEditorComponent.vue';
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import SubmitModel, { SUBMIT_STATUS } from '@/models/SubmitModel';
import ProblemModel from '@/models/ProblemModel';
import problemStore from '@/store/modules/problem';
import submitStore from '@/store/modules/submit';
import axios, { AxiosError, AxiosResponse } from 'axios';
import _ from 'lodash';
import { de_options } from '@/utils/consts';
import { Component, Prop, Watch } from 'vue-property-decorator';


@Component({ components: { CodeEditorComponent } })
export default class SubmitComponent extends NotificationMixinComponent {
  @Prop({ required: true }) submitId!: number;
  @Prop({ required: true }) isStaff!: boolean;
  submit: SubmitModel | null = null;
  submitStore = submitStore;
  problemStore = problemStore;
  submitEdit: SubmitModel = { ...this.submitStore.defaultSubmit };
  loading = true;

  async created() {
    await this.updateSubmit();
  }

  async updateSubmit() {
    this.loading = true;
    if (this.submitId) {
      this.submit = await this.submitStore.fetchSubmitById(this.submitId);
    } else {
      this.submit = null;
    }
    this.submitEdit = (this.submit) ? { ...this.submit } : { ...this.submitStore.defaultSubmit };
    if (this.submitEdit.de_id === '' && this.deOptions.length === 1)
      this.submitEdit.de_id = this.deOptions[0].value;
    this.loading = false;
  }


  get isChanged(): boolean {
    return !_.isEqual(this.submit, this.submitEdit);
  }

  get isRejectDisabled() {
    return this.isNewSubmit || this.submit?.status === SUBMIT_STATUS.WRONG_ANSWER;
  }

  get isAcceptDisabled() {
    return this.isNewSubmit || this.submit?.status === SUBMIT_STATUS.OK;
  }

  get canSubmit(): boolean {
    return this.submitEdit.content?.length !== 0
      && this.isChanged
      && this.submitEdit.de_id.length !== 0;
  }

  get problem(): ProblemModel {
    return this.problemStore.currentProblem as ProblemModel;
  }


  // TODO: workflow when already-made submit have de that is disabled
  get deOptions() {
    const options_on = this.problem.de_options.split(',')
    return de_options.filter(option => options_on.includes(option.value));
  }

  get isNewSubmit(): boolean {
    return isNaN(this.submitEdit.id);
  }

  @Watch('submitId')
  onSubmitIdChanged() {
    this.updateSubmit();
  }

  patchSubmit(status: string) {

    this.submitEdit = (this.submit)
      ? { ...this.submit, status: status }
      : { ...this.submitStore.defaultSubmit };

    axios.patch(`/api/submit/${this.submitEdit.id}/`, this.submitEdit)
      .then((response: AxiosResponse<SubmitModel>) => {
        this.submitStore.changeSubmitStatus(response.data);
        this.submit = { ...response.data };
        this.submitEdit = { ...this.submit };
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
    this.submitEdit = {
      ...this.submitEdit,
    };
    axios.post('/api/submit/', {
      ...this.submitEdit,
      'problem': this.problemStore.currentProblem?.id as number,
    }).then((response: AxiosResponse<SubmitModel>) => {
      this.submitStore.addSubmitToArray(response.data);
      this.$emit('submit-created', { id: response.data.id.toString() });
      this.submit = { ...response.data };
      this.submitEdit = { ...this.submit };
      this.notificationKind = 'success';
      this.notificationText = 'Попытка отправлена';
    }).catch((error: AxiosError) => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так ${error.message}`;
    }).finally(() => this.showNotification = true);
  }

}
</script>

<style lang="stylus" scoped>
.submit-title
  padding-bottom 0.5rem

.text-area-teacher
  opacity 90%
  border 0.5px solid rgba(0, 0, 0, .3)

.rejected
  margin-left 0.5rem

.handlers
  margin-top 0.5rem
  display flex
  flex-direction row
  justify-content flex-end


</style>
