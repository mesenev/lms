<template>
  <li v-if="!loading" :class="{'status-ok': isAccepted,
                 'status-wa': isRejected,
                 'status-aw': isAwaitingManual,
                 'status-np': !(isAccepted || isRejected || isAwaitingManual)}" class="status">
    <div class="status-back"></div>
    <router-link :to="target">
      <component
          :is="Checkmark16"
          v-if="isAccepted"
          class="icon-accepted">
      </component>
      <component
        :is="Checkmark16"
        v-else-if="isAwaitingManual"
        class="icon-accepted">
      </component>
      <component
          :is="Close16"
          v-else-if="isRejected"
          class="icon-rejected">
      </component>
      <span
          v-else
          class="icon-not-passed"
          v-text="'?'">
      </span>
    </router-link>
  </li>
  <li v-else>
    <cv-tag-skeleton></cv-tag-skeleton>
  </li>
</template>

<script lang="ts" setup>
import useSubmitStore from "@/stores/modules/submit"
import useUserStore from "@/stores/modules/user"
import ProblemModel from "@/models/ProblemModel";
import SubmitModel, { SUBMIT_STATUS } from "@/models/SubmitModel";
import Checkmark16 from "@carbon/icons-vue/es/checkmark/16";
import Close16 from "@carbon/icons-vue/es/close/16";
import { ref, Ref, computed, onMounted } from "vue";

  const props = defineProps({problem:{required: true, type: ProblemModel}})

  const submitStore = useSubmitStore();
  const userStore = useUserStore();
  const submit: Ref<SubmitModel | null> = ref(null);
  const loading = ref(true);
  const target: object = ref({});

  const getStatus = computed((): string | undefined => {
    return submit?.value.status;
  })

  const isAccepted = computed(() => {
    return getStatus.value === SUBMIT_STATUS.OK;
  })

  const isRejected = computed(() => {
    return getStatus.value === SUBMIT_STATUS.WRONG_ANSWER;
  })
  const isAwaitingManual = computed(() => {
    return getStatus.value === SUBMIT_STATUS.AWAITING_MANUAL;
  })

onMounted(async() => {
    await submitStore.fetchLastSubmit({
      user_id: userStore.user.id,
      problem_id: props.problem.id
    })
      .then((data: SubmitModel | null) => submit.value = data)
      .catch((error: string) => console.log(error));

    // TODO: MAKE SEPARATE TARGET METHOD FOR ALL NAVIGATION LINKS
    if (!!submit.value?.status) {
      target.value = {
        name: 'ProblemViewWithSubmit',
        params: {
          courseId: this.$route.params.courseId,
          lessonId: this.$route.params.lessonId,
          problemId: this.problem.id.toString(),
          submitId: this.submit.id.toString(),
        }
      };
    } else {
      target.value = {
        name: 'ProblemView', params: {
          courseId: this.$route.params.courseId,
          lessonId: this.$route.params.lessonId,
          problemId: this.problem.id.toString(),
        }
      };
    }
    loading.value = false;
  })

</script>

<style lang="stylus" scoped>
li
  border-radius 50px
  text-align center
  width 32px
  height 32px
  line-height 32px
  margin-bottom 1rem

.status
  width 24px
  height 24px
  line-height 24px
  margin 0.5rem 4px 0 4px
  position relative
  box-sizing border-box

  a
    position relative
    z-index 1
    display block
    width 100%
    height 100%

    &:focus
      outline none


  &-back
    width 28px
    height 28px
    position absolute
    top -2px
    left -2px
    border 1px solid #808080
    border-radius 50px
    display none

  &-ok
    background-color #4EB052

    svg
      width 18px
      height 18px
      margin 3px

  &-aw
    background-color #8fbd8f

    svg
      width 18px
      height 18px
      margin 3px

  &-wa
    background-color #DA1E28

    svg
      width 16px
      height 16px
      margin 4px

  &-np
    background-color transparent
    border 1px #808080 solid

    a
      color black
      text-decoration none

      &:hover
        text-decoration 1px underline

  &-np &-back
    top -3px
    left -3px

  &:hover &-back
    display unset

.icon
  &-rejected, &-accepted
    fill white

  &-not-passed
    fill black
    stroke black
    color var(--cds-text-01)
</style>
