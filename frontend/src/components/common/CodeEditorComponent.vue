<template>
  <label>
    <prism-editor v-model="code" :highlight="highlighter" class="my-editor" line-numbers/>
  </label>
</template>

<script lang="js">
import { Component, Prop, Watch, Vue } from 'vue-property-decorator';

import { PrismEditor } from 'vue-prism-editor';

import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/themes/prism-tomorrow.css'; // import syntax highlighting styles
@Component({ components: { PrismEditor } })
export default class CodeEditorComponent extends Vue {
  @Prop({ required: true }) value;
  code = 'console.log("Hello World")';

  @Watch('code')
  handler() {
    this.$emit('input', this.code);
  }

  created() {
    this.code = this.value;
  }

  highlighter(code) {
    return highlight(code, languages.js);
  }
};
</script>

<style lang="stylus" scoped>
.my-editor
  background-color: #f5f2f0;
  height 400px;
  font-family: Fira code,Fira Mono,Consolas,Menlo,Courier,monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px 10px;
  border #8D8D8D solid
  border-width 0.5px 0
</style>

<style lang="stylus">
.prism-editor__textarea
  border none
  outline none
</style>
