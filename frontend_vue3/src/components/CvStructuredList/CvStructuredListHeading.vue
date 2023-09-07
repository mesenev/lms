<template>
  <div
    :class="`cv-structured-list-heading ${carbonPrefix}--structured-list-th`"
  >
    <slot></slot>
  </div>
</template>

<script setup>
const carbonPrefix = 'bx';
</script>
