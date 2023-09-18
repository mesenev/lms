<template>
  <div class="item">
    <div :class="['submit-header', 'status-' + submitEdit.status.toLowerCase()]">
      <div class="line">
        <h4 class="submit-title">ID решения: {{ submitId }}</h4>
        <span class="submit-status">Состояние: <span class="status">{{
            submitEdit.status
          }}</span></span>
      </div>
      <span class="submit-date">{{ submitEdit.updated_at | withoutSeconds }}</span>
    </div>
    <cv-skeleton-text v-if="loading"/>
    <div v-else>
      <code-editor-component :value="submitEdit.content" @input="inputContent"/>
      <div class="submit-lang">
        <div>Среда разработки:</div>
        <cv-dropdown
            v-model:value="submitEdit.de_id"
            :disabled="deOptions.length === 0"
            :items="deOptions"
            class="lang-choice"
            placeholder="Выберите язык программирования">
          <cv-dropdown-item v-for="de in deOptions" :key="de.value" :value="de.value">
            <span>{{ de.name }}</span>
          </cv-dropdown-item>
        </cv-dropdown>
      </div>
    </div>
    <div class="buttons-block-wrapper">
      <div class="handlers bx--row buttons-container">
        <div class="submit-container">
          <div class="input-file-container">
            <input type="file"
                   id="file_input" @change="handleFileUpload()">
            <component class="trash-icon icon" :is="TrashCan" @click.prevent.stop="deleteFile"/>
          </div>
          <cv-button
              v-if="!loading"
              :disabled="!canSubmit"
              class="submit-btn"
              @click="confirmSubmit">
            Отправить решение
          </cv-button>

          <cv-button-skeleton v-else></cv-button-skeleton>
          <cv-link
              v-if="!cats_account"
              :to="{
            name: 'profile-page',
            params: { userId: userStore.user.id }
          }">
            <cv-tooltip tip="Установите cats аккаунт для отправки"/>
          </cv-link>
        </div>
        <div v-if="isStaff" class="handlers-staff">
          <cv-button
              v-if="!loading"
              :disabled="isAcceptDisabled"
              class="submit-btn accepted"
              @click="acceptSubmit">
            Принять
          </cv-button>
          <cv-button-skeleton v-else></cv-button-skeleton>
          <cv-button
              v-if="!loading"
              :disabled="isRejectDisabled"
              class="submit-btn rejected"
              kind='danger'
              @click="rejectSubmit">
            Отклонить
          </cv-button>
          <cv-button-skeleton v-else></cv-button-skeleton>
        </div>
      </div>
    </div>
    <cv-inline-notification
        v-if="showNotification"
        :kind="notificationKind"
        :sub-title="notificationText"
        class="notification"
        @close="hideNotification"/>
  </div>
</template>

<script lang="ts" setup>
import CodeEditorComponent from '@/components/common/CodeEditorComponent.vue';
import { SUBMIT_STATUS } from '@/models/SubmitModel';
import type { SubmitModel } from '@/models/SubmitModel';
import type { ProblemModel } from '@/models/ProblemModel';
import useProblemStore from '@/stores/modules/problem';
import useSubmitStore from '@/stores/modules/submit';
import useUserStore from '@/stores/modules/user';
import { AxiosError } from 'axios';
import type { AxiosResponse } from 'axios';
import api from '@/stores/services/api'
import { de_options } from '@/utils/consts';
import _ from 'lodash';
import TrashCan from '@carbon/icons-vue/es/trash-can/20';
import { ref, computed, onMounted, watch } from 'vue'
import type { Ref } from 'vue';
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({ submitId: { type: Number, required: true }, isStaff: { type: Boolean, required: true } })
const emit = defineEmits<{
  (e: 'submit-created', id: string): void
}>()


const submitStore = useSubmitStore();
const problemStore = useProblemStore();
const userStore = useUserStore();

const submitEdit = ref<SubmitModel>({ ...submitStore.defaultSubmit });
const submit = ref<SubmitModel | null>(null);
const loading = ref(true);
const file_content = ref('');

const isChanged = computed((): boolean => {
  return !_.isEqual(submit.value, submitEdit.value);
})

function inputContent(content: string) {
  submitEdit.value.content = content;
}

function deleteFile() {
  const input = window.document.getElementById('file_input') as HTMLInputElement
  if (input.files?.length) {
    input.value = '';
    file_content.value = '';
  }
}

function readFileAsync(file: File) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = () => {
      resolve(reader.result);
    };

    reader.onerror = reject;

    reader.readAsText(file);
  })
}

async function handleFileUpload() {
  const input = window.document.getElementById('file_input') as HTMLInputElement

  if (input.files?.length) {
    file_content.value = await readFileAsync(input.files[0]) as string
  }
}

const isRejectDisabled = computed(() => {
  return isNewSubmit.value || submit.value?.status === SUBMIT_STATUS.WRONG_ANSWER;
})

const isAcceptDisabled = computed(() => {
  return isNewSubmit.value || submit.value?.status === SUBMIT_STATUS.OK;
})

function setNotification() {
  if (file_content.value.length != 0 &&
      submitEdit.value.content?.length !== 0) {
    notificationKind.value = 'error';
    notificationText.value = `Отправьте либо текст решения либо файл`;
    showNotification.value = true;
  } else {
    showNotification.value = false;
  }
}

const canSubmit = computed((): boolean => {
  setNotification();

  return (((submitEdit.value.content?.length !== 0
          && isChanged.value) || (file_content.value.length != 0))
      && submitEdit.value.de_id.length !== 0
      && cats_account.value) && !(file_content.value.length != 0 &&
      submitEdit.value.content?.length !== 0);

})

const cats_account = computed((): boolean => {
  return userStore.user.cats_account !== null;
})

const problem = computed((): ProblemModel => {
  return problemStore.currentProblem as ProblemModel;
})

// TODO: workflow when already-made submit have de that is disabled
const deOptions = computed(() => {
  const options_on = problem.value.de_options.split(',')
  return de_options.filter(option => options_on.includes(option.value));
})

const isNewSubmit = computed((): boolean => {
  return isNaN(submitEdit.value.id);
})

onMounted(async () => {
  await updateSubmit();
})

async function updateSubmit() {
  loading.value = true;
  if (props.submitId) {
    submit.value = await submitStore.fetchSubmitById(props.submitId);
  } else {
    submit.value = null;
  }
  submitEdit.value = (submit.value) ? { ...submit.value } : { ...submitStore.defaultSubmit };
  if (submitEdit.value.de_id === '' && deOptions.value.length === 1)
    submitEdit.value.de_id = deOptions.value[0].value;
  loading.value = false;
}

watch(() => props.submitId, (newVal, oldVal) => onSubmitIdChanged)

function onSubmitIdChanged() {
  updateSubmit();
}

function patchSubmit(status: string) {

  submitEdit.value = (submit.value)
      ? { ...submit.value, status: status }
      : { ...submitStore.defaultSubmit };


  api.patch(`/api/submit/${submitEdit.value.id}/`, submitEdit.value)
      .then((response) => {
        submitStore.changeSubmitStatus(response.data);
        submit.value = { ...response.data };
        submitEdit.value = { ...response.data };
        notificationKind.value = 'success';
        notificationText.value = `Работа оценена: ${status}`;
      })
      .catch((error: AxiosError) => {
        notificationKind.value = 'error';
        notificationText.value = `Что-то пошло не так ${error.message}`
      })
      .finally(() => showNotification.value = true);
}

function acceptSubmit() {
  patchSubmit('OK');
}

function rejectSubmit() {
  patchSubmit('WA');
}

function confirmSubmit() {

  submitEdit.value = {
    ...submitEdit.value
  }

  if (file_content.value.length != 0) {
    submitEdit.value.content = file_content.value
  }

  api.post('/api/submit/', {
    ...submitEdit.value, 'content': submitEdit.value.content,
    'problem': problemStore.currentProblem?.id as number,
  }).then((response: AxiosResponse<SubmitModel>) => {
    submitStore.addSubmitToArray(response.data);
    emit('submit-created', response.data.id.toString());
    submit.value = { ...response.data };
    submitEdit.value = { ...submit.value };
    problem.value.last_submit = submit.value;
    problemStore.changeCurrentProblem(problem.value)
    notificationKind.value = 'success';
    notificationText.value = 'Попытка отправлена';
  }).catch((error: AxiosError) => {
    notificationKind.value = 'error';
    notificationText.value = `Что-то пошло не так ${error.message}`;
  }).finally(() => showNotification.value = true);
}

</script>

<style lang="stylus" scoped>
.item
  padding 0
  position: relative;

  .notification
    position absolute
    bottom 7rem
    z-index 1

.submit-header
  padding 1em
  border-radius 5px 0 0 0

  .line
    display flex
    justify-content space-between
    padding-bottom 0.5rem

  .submit-status
    font-size 1.5em

  .submit-date
    font-size 1em


.status
  font-weight bold

  &-ok
    color white
    background-color #4EB052

    .submit-data
      color #d6d5d4

  &-aw
    color white
    background-color #8fbd8f

    .submit-data
      color #d6d5d4

  &-wa
    color white
    background-color #DA1E28

    .submit-data
      color #d6d5d4

  &-np
    color white
    background-color #393939

    .submit-data
      color #fafafa


.submit-lang
  display flex
  align-items center
  background var(--cds-ui-03)
  color var(--cds-text-01)
  padding 0.5rem

  div
    height 2.5rem;
    padding 0 0.5rem;
    display flex;
    align-items center;

  .lang-choice
    padding 0

.buttons-block-wrapper
  background-color var(--cds-ui-03)
  border-radius 0 0 0 5px

  .handlers
    display flex
    flex-direction row
    padding 0.5rem
    align-items center
    vertical-align center

.input-file-container
  display flex
  align-items center

input
  width: 80%


.handlers-staff
  display flex
  width fit-content
  gap 0.5rem

.submit-btn
  width min-content

//justify-content center

.buttons-container
  justify-content space-between
  margin 0 .05rem 0 .5rem

.submit-container
  display flex
  flex-direction row
  align-items center
  gap 0.5rem

</style>


<style lang="stylus" scoped>
.bx--dropdown
  border-bottom 0

/deep/ .bx--list-box__field
  display flex

  .bx--list-box__field, ui
    border 0.5px solid #8D8D8D
    background-color var(--cds-ui-background)
    border-radius 10px

.bx--list-box__menu-icon
  top 0.5rem

.cv-button
  padding 0 1rem
</style>
