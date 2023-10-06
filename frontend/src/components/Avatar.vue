<template>
  <div>
    <img class="avatar"
         v-bind:src="pic_url"
         alt=""
         width="250"
         height="250">
  </div>
</template>

<script lang="ts" setup>
import {computed} from "vue";

const props = defineProps({
  avatar_url: {type: String, required: false}
});

const src = "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";

const pic_url = computed(() => {
  if (!props.avatar_url)
    return src;
  return props.avatar_url;
})
</script>

<style scoped lang="stylus">
.avatar
  object-fit: cover;
  border-radius: 150%;
</style>
