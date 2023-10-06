<template>
  <div class="bx--grid">
    <div class="bx--row header"><h1>Редактирование задачи</h1></div>
    <div v-if="showNotification" class="bx--row">
      <cv-inline-notification
          :kind="notificationKind"
          :sub-title="notificationText"
          @close="() => showNotification = false"
      />
    </div>
    <div class="bx--row">
      <div class="bx--col-lg-7 items">
        <cv-skeleton-text
            v-if="loading"
            :line-count="6"
            :paragraph="true"
            :width="'80%'"/>
        <div v-else>
          <cv-text-input v-model.trim="problemEdit.name" label="Название"/>
          <cv-text-area v-model.trim="problemEdit.description" label="Описание"/>
          <div>
            <br>
            <cv-multi-select
                v-model:value="deChecks"
                :options="deOptions"
                class="course--de"
                label="Выберите среды разработки"
                title="Доступные среды для отправки решений"
                @change="deChanged">
              <template v-slot:helper-text>
                <cv-tooltip direction="right" tip="При пустом списке будет использованы настройки курса"/>
              </template>
            </cv-multi-select>
          </div>
        </div>
        <span style="padding-top: 20px">Выберите способ тестирования</span>
        <cv-radio-group style="margin-top: 10px; padding-bottom: 20px">

          <cv-radio-button @change=modChanged
                           name="group-1"
                           label="автоматическое"
                           value="auto"
                           v-model="testingMode"
          />
          <cv-radio-button @change=modChanged
                           name="group-1"
                           label="ручное"
                           value="manual"
                           v-model="testingMode"
          />
          <cv-radio-button @change=modChanged
                           name="group-1"
                           label="автоматическое и ручное"
                           value="auto_and_manual"
                           v-model="testingMode"
          />

        </cv-radio-group>
        <cv-button-skeleton v-if="problemUpdating"/>
        <cv-button
            v-else :disabled="!isChanged || loading"
            class="finishButton"
            @click="updateProblem">
          Обновить задачу
        </cv-button>

      </div>
      <div class="bx--col-lg-1"></div>
      <div class="bx--col-lg-7 items original-cats-problem">
        <cv-skeleton-text
            v-if="catsProblemLoading || !catsProblem"
            :line-count="6"
            :paragraph="true"
            :width="'80%'"/>
        <cv-accordion v-else>
          <cv-accordion-item>
            <template v-slot:title>
              Cats версия задачи
            </template>
            <template v-slot:content>
              <problem-description :problem="problem"/>
            </template>
          </cv-accordion-item>
        </cv-accordion>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import _ from 'lodash';
import useProblemStore from "@/stores/modules/problem";
import { computed, onMounted, ref } from "vue";
import type { ProblemModel } from "@/models/ProblemModel";
import type { CatsProblemModel } from "@/models/CatsProblemModel";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import ProblemDescription from "@/components/ProblemDescription.vue";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  problemId: { type: Number, required: true }
})


const problemStore = useProblemStore();
const problem = ref<ProblemModel>({ ...problemStore.getNewProblem });
const problemEdit = ref<ProblemModel>({ ...problemStore.getNewProblem });
const loading = ref(true);
const catsProblemLoading = ref(true);
const catsProblem = ref<CatsProblemModel | null>(null);
const problemUpdating = ref(false);
const testingMode = ref('');
const deChecks = ref<string[]>([]);
const deOptions = [
  {
    value: '3', label: 'Cross-platform C/C++ compiler',
    name: 'Cross-platform C/C++ compiler', disabled: false,
  },
  {
    value: '681949', label: 'Python 3.8.1',
    name: 'Python 3.8.1', disabled: false,
  },
];


function deChanged() {
  problemEdit.value = { ...problemEdit.value, de_options: deChecks.value.sort().join(',') };
}

function modChanged() {
  problemEdit.value = { ...problemEdit.value, test_mode: testingMode.value }
}

const isChanged = computed((): boolean => {
  return !_.isEqual(problem.value, problemEdit.value);
})

onMounted(async () => {
  loading.value = true;
  problem.value = await problemStore.fetchProblemById(props.problemId);
  problemEdit.value = { ...problem.value };
  deChecks.value = problemEdit.value.de_options.split(',');
  loading.value = false;
  catsProblem.value = await problemStore.fetchCatsProblemById(problem.value.id)
  testingMode.value = problemEdit.value.test_mode;
  catsProblemLoading.value = false;
})

function updateProblem(): void {
  problemUpdating.value = true;
  const request = problemStore.patchProblem(problemEdit.value);
  request.then(response => {
    notificationKind.value = 'success';
    notificationText.value = 'Задача успешно обновлена'
    problem.value = response.data;
    problemEdit.value = { ...problem.value };
    problemStore.changeCurrentProblem(response.data);
  });
  request.catch(error => {
    notificationText.value = `Что-то пошло не так: ${error.message}`;
    notificationKind.value = 'error';
  })
  request.finally(() => {
    showNotification.value = true;
    problemUpdating.value = false;
  });
}
</script>

<style scoped lang="stylus">
.items
  background-color var(--cds-ui-02)

.header
  padding-bottom 1.5rem
  padding-top 1rem

.original-cats-problem
  margin-top 1rem

</style>
