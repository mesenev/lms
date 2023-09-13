<template>
  <div>
    <h4 v-if="!isNaN(problem.id)"
        class="problem-description-container"
        v-html="description">
    </h4>
    <cv-skeleton-text v-else/>
  </div>
</template>

<script lang="ts" setup>
import ProblemModel from '@/models/ProblemModel';
import { onMounted } from "vue";

const props = defineProps({problem: {type: ProblemModel, required: true}})

let description = '';

onMounted(async () => {
    description = props.problem.description.replaceAll('download/img', 'https://imcs.dvfu.ru/cats/static/download/img');
  })

</script>

<style lang="stylus" scoped>
/deep/ .problem-description-container
  margin 0.5rem
  font-size 1rem

/deep/ .jsonly.problem_menu_trigger.problem_menu_click
  visibility hidden

/deep/ .button.copy_button
  visibility hidden

/deep/ .nav_container.hidden
  visibility hidden

/deep/ .narrow
  width 1px
  padding-right 1rem

/deep/ .problem-header
  border-collapse separate
  border-spacing 2px

/deep/ .timing
  visibility hidden

/deep/ .submit
  visibility hidden

/deep/ .nobr
  white-space nowrap

/deep/ .spell
  text-decoration underline
  color red

/deep/ .sample th, /deep/ .sample td
  border-collapse collapse;
  border 1px solid black;
  padding 5px

/deep/ hr
  visibility hidden

/deep/ b
  font-weight bold

/deep/ i
  font-style italic

/deep/ code
  font-family monospace

/deep/ tt
  font-family monospace

/deep/ ol
  display block
  list-style-type decimal
  margin-block-start 1em
  margin-block-end 1em
  margin-inline-start 0px
  margin-inline-end 0px
  padding-inline-start 40px

/deep/ ul
  display block
  list-style-type disc
  margin-block-start 1em
  margin-block-end 1em
  margin-inline-start 0px
  margin-inline-end 0px
  padding-inline-start 40px
  margin-top 5px
  margin-bottom 5px

/deep/ h3
  margin-top 1rem

</style>
