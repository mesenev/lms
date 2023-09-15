<template>
  <cv-loading v-if="isLoading"/>
  <div
    v-else
    class="cats-package-window">
    <div v-for="message_keys in Object.keys(data)" v-bind:key="message_keys">
      <div class="head_of_message">
        {{ message_keys }}
      </div>
      <div class="message">
        {{ data[message_keys] }}
      </div>
    </div>

  </div>
</template>

<script lang="ts" setup>

import type { SubmitModel } from '@/models/SubmitModel';
import useSubmitStore from '@/stores/modules/submit';
import api from '@/stores/services/api';
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  submitIdProp: {type: Number, required: true}
})

const data = ref({});
const submitStore = useSubmitStore();

const isLoading = computed((): boolean => {
    return Object.keys(data.value).length === 0;
  })

onMounted(async () => {
    data .value= await submitStore.fetchCatsResult(props.submitIdProp);
  })

</script>


<style lang="stylus" scoped>
.head_of_message
  padding 10px
  width 100%
  height min-content
  font-size 1.7em
  font-weight bold

.message
  background rgba(207, 204, 174, 0.3);
  padding-left 5px
  padding-right 5px
  padding-bottom 10px
  padding-top 10px
  margin 10px


.cats-package-window
  height 100%
  background white


</style>

<style lang="stylus" scoped>

</style>
