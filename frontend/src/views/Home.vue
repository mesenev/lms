<template>
  <div>
    <span>Home</span>
    <div>
      <router-link to="/course/1">Курс</router-link> <br>
      <router-link to="/course/1/lesson/1">Урок</router-link> <br>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import CourseModel from '@/models/CourseModel';

export default defineComponent({
  name: 'Home',
  props: {
    todo: {
      type: Object as PropType<CourseModel>,
      required: true,
    },
  },
  data() {
    return {
      editable: false,
    };
  },
  methods: {
    onTextChange(e: { target: { value: string } }) { this.$emit('update-todo', e.target.value); },
  },
  computed: {
    checked: {
      get(): boolean { return true; },
      set(value: boolean) { this.$emit('checkbox-click', value); },
    },
  },
});
</script>

<style scoped>

</style>
