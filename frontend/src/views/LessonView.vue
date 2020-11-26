<template>
  <div>
    <Problem />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import CourseModel from '@/models/CourseModel';

export default defineComponent({
  name: 'CourseView',
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
