<template>
  <div
    :class="[
      `cv-structured-list-data ${carbonPrefix}--structured-list-td`,
      {
        [`${carbonPrefix}--structured-list-content--nowrap`]: noWrap,
      },
    ]"
  >
    <slot></slot>
  </div>
</template>

<script setup>
const carbonPrefix = 'bx';

defineProps({
  noWrap: Boolean,
});

</script>
