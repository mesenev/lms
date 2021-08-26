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
      <cv-text-area
        :rows="13"
        v-model="submitEdit.content"
        :class="{ 'text-area-teacher': isStaff, 'text-area-student': !isStaff }"
        :disabled="isStaff"
        light>
      </cv-text-area>
      <cv-dropdown
        v-if="!isStaff && languageList"
        :items="languageList"
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
        <cv-button
          :disabled="isNewSubmit"
          class="submit-btn accepted"
          v-on:click="acceptSubmit">
          Принять
        </cv-button>
        <cv-button
          kind='danger'
          :disabled="isNewSubmit"
          class="submit-btn rejected"
          v-on:click="rejectSubmit">
          Отклонить
        </cv-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import SubmitModel from '@/models/SubmitModel';
import problemStore from '@/store/modules/problem'
import submitStore from '@/store/modules/submit'
import axios, { AxiosError, AxiosResponse } from 'axios';
import _ from 'lodash';
import { Component, Prop, Watch } from 'vue-property-decorator';


@Component({ components: {} })
export default class SubmitComponent extends NotificationMixinComponent {
  @Prop({ required: true }) submitId!: number;
  @Prop({ required: true }) isStaff!: boolean;
  @Prop({ required: true }) languageList!: Array<string>;
  submit: SubmitModel | null = null;
  submitStore = submitStore;
  problemStore = problemStore;
  submitEdit: SubmitModel = { ...this.submitStore.defaultSubmit };
  loading = true;


  get isChanged(): boolean {
    return !_.isEqual(this.submit, this.submitEdit);
  }

  get canSubmit(): boolean {
    return this.submitEdit.content?.length !== 0 && this.isChanged;
  }

  get isNewSubmit(): boolean {
    return isNaN(this.submitEdit.id);
  }

  @Watch('submitId')
  onSubmitIdChanged() {
    this.updateSubmit();
  }

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
    this.loading = false;
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
        if (this.submit.status == 'OK')
          this.notificationKind = 'success';
        else
          this.notificationKind = 'error';
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
