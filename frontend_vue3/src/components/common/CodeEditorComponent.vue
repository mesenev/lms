<template>
  <label>
    <prism-editor v-model="code" :highlight="highlighter" class="my-editor" line-numbers/>
  </label>
</template>

<script lang="ts" setup>
import { PrismEditor } from 'vue-prism-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/themes/prism-tomorrow.css';
import { onMounted, ref, watch } from "vue"; // import syntax highlighting styles

const props = defineProps({
  value: { type: String, required: false, default: 'console.log("Hello World")'}
});

const emits = defineEmits(['input']);

const code = ref('console.log("Hello World")');

watch(() => code.value, () => {
  emits('input', code.value);
})

onMounted(() => {
  code.value = props.value;
})

function highlighter(code: string) {
  return highlight(code, languages.js);
}
</script>

<style lang="stylus" scoped>
.my-editor
  background-color: var(--cds-ui-01);
  height 400px;
  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px 10px;
  border var(--cds-ui-04) solid
  border-width 0.5px 0
</style>

<style lang="stylus">
.prism-editor__textarea
  border none
  outline none
</style>
