<template>
  <div>
    <ul>
      <Lesson
        v-for="(todo, id) in note.todos"
        :todo="todo"
        :key="id"
      />
    </ul>
  </div>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'CourseView',
  props: {
    todo: {
      type: Object as PropType<CourseModel>,
      required: true,
    },
  },
  data() { return { editable: false }; },
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
