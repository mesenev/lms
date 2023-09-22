<script lang="ts" setup>
import type {UserModel} from "@/models/UserModel";
import useUserStore from "@/stores/modules/user";
import {useCourseStore} from "@/stores/modules/course";
import type {PropType} from "vue";
import {computed, onMounted, ref} from "vue";

const props = defineProps({
  userProp: {type: Object as PropType<UserModel>, required: false},
  userId: {type: Number, required: false},
})

const loading = ref(true);
const userStore = useUserStore();
const courseStore = useCourseStore();
const currentUser = ref<UserModel | null>(null);

const name = computed(() => {
  if (currentUser.value && currentUser.value.first_name && currentUser.value.last_name)
    return `${currentUser.value.first_name} ${currentUser.value.last_name}`;
  return currentUser.value?.username;
});

const picUrl = computed(() => {
  if (currentUser.value && currentUser.value.avatar_url)
    return currentUser.value.thumbnail;
  return "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";
});

const warning = computed(() => {
  if (!courseStore.currentCourse)
    return false;
  if (props.userId)
    return !(props.userId in userStore.currentCourseStudents);
  return !(props.userProp!.id in userStore.currentCourseStudents);
});

onMounted(async () => {
  if (!props.userProp && !props.userId)
    throw Error();
  if (props.userProp)
    currentUser.value = props.userProp;
  if (props.userId)
    currentUser.value = userStore.currentCourseStudents[props.userId];
  if (typeof currentUser.value === 'undefined')
    currentUser.value = await userStore.fetchUserById(props.userId!)
  loading.value = false;
})
</script>

<template>
  <div class="user-component">
    <div class="user-component--wrapper">
      <img alt="" class="user-component--avatar" :src="picUrl"/>
      <div class="user-component--name">
        <cv-inline-loading v-if="loading" state="loading" active/>
        <span v-else>{{ name }}</span>
      </div>
      <div v-if="warning" class="user-component--warning">
        <cv-tooltip tip="Пользователь не является студентом курса"/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="stylus">
.user-component
  width 200px
  height 32px

  &--wrapper
    display flex
    flex-flow row
    align-items center

  &--avatar
    height 32px
    width 32px
    border-radius: 150%
    padding 0
    margin 0

  &--name
    padding-left var(--cds-spacing-02)

  &--warning
    padding-left var(--cds-spacing-02)
    display flex
    align-items center

</style>
