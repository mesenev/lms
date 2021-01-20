<template>
<div>
  <cv-button size="field" kind="secondary" @click="Todo">
    Сгенерировать ссылку-приглашения
  </cv-button>
  <cv-text-input v-if="tmp > 0" :value="'Here needs links'" helper-text="Ваша ссылка:">
  </cv-text-input>
  <cv-text-input v-else :value="'Press the button'" helper-text="Ваша ссылка появится после нажатия" disabled="true">
  </cv-text-input>
</div>
</template>

<!-- TODO: backend wrk -->
<script>
import {Component, Vue} from "vue-property-decorator";

@Component({ components: {} })
export default class CourseView extends Vue {
  tmp = 0;
  Todo() {
    this.tmp += 1
  }
}
</script>

<style scoped>

</style>
