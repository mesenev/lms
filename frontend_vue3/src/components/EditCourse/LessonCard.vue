<template>
  <div class="card">
    <div class="title">
      <h5>{{ lesson.name }}</h5>
      <cv-tag v-for="problem in getLessonProblems"
              :key="problem"
              kind="red"
              :label="problem">
      </cv-tag>
    </div>
    <div class="icons">
      <component class="icon"
                 v-if="secondIcon"
                 :is="secondIcon"
                 @click="editLesson">
      </component>
      <component class="icon"
                 :is="getIcon"
                 @click="manipulation(lesson); changeIcon()">
      </component>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { PropType } from "vue";
import type { LessonModel } from "@/models/LessonModel";
import { computed, ref } from "vue";
import _ from "lodash";
import { useRouter } from "vue-router";

const props = defineProps({
  lesson: { type: Object as PropType<LessonModel>, required: true },
  manipulation: { type: Function, required: true },
  mainIcon: { type: Object, required: true },
  changeMainIcon: { type: Object, required: false },
  secondIcon: { type: Object, required: false }
})

const router = useRouter();

const currentIcon = ref(0);

const icons = [props.mainIcon, props.changeMainIcon || props.mainIcon];

const getIcon = computed(() => {
  return icons[currentIcon.value];
})

function changeIcon() {
  currentIcon.value = (currentIcon.value + 1) % icons.length;
}

const getLessonProblems = computed(() => {
  const problems: string[] = [];
  for (const [key, value] of Object.entries(props.lesson)) {
    if (_.isArrayLike(value) && _.isEmpty(value) && key === 'problems') {
      problems.push(`Empty ${key}`);
    }
  }
  return problems;
})

function editLesson() {
  router.push({ name: 'lesson-edit', params: { lessonId: props.lesson.id.toString() } });
}
</script>

<style scoped lang="stylus">
.card
  padding 20px
  display flex
  flex-direction row
  justify-content space-between
  align-items center

.title
  display flex
  flex-direction row
  align-items baseline

  h5
    margin-right: 5px

.icon
  transition ease-in-out 0.1s

.icon:active
  transform scale(0.9)

.icon:nth-child(odd)
  margin: 0 10px
</style>
