<template>
  <router-link
    :to="{ name: 'CourseView', params: { courseId: course.id.toString() } }"
    class="list-element">
    <div class="list-element--main">
      <h5 class="list-element--title">{{ course.name }}</h5>
      <span class="list-element--info">Преподаватель: {{ teacher }}</span>
    </div>
    <!--    <span class="list-element&#45;&#45;info">Следующий урок: {{ "24/1" }}</span>-->
  </router-link>
</template>

<script lang="ts" setup>

import type { PropType } from "vue";
import type { CourseModel } from "@/models/CourseModel";
import useUserStore from "@/stores/modules/user";
import { computed } from "vue";

const props = defineProps({
  courseProp: { type: Object as PropType<CourseModel>, required: true }
})

const userStore = useUserStore();

const course = computed(() => {
  return props.courseProp;
})

const teacher = computed(() => {
  if (!course.value.author)
    return '';
  if (course.value.author.middle_name)
    return `${course.value.author.first_name} `
      + `${course.value.author.middle_name} `
      + `${course.value.author.last_name}`;
  return `${course.value.author.first_name} ${course.value.author.last_name}`;
})
</script>

<style scoped lang="stylus">
.list-element
  display flex
  flex-direction row
  justify-content space-between
  padding-right 0.5rem

.trash-icon
  margin-right 0.5rem

</style>
