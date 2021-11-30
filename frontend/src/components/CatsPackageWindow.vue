<template >
  <div class="cats-package-window">
    <div v-for="message_keys in Object.keys(getCatsData)" v-bind:key="message_keys">
      <div class = "head_of_message">
        {{message_keys}}
      </div>
      <div class = "message">
        {{getCatsData[message_keys]}}
      </div>
    </div>

  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class CatsPackageWindow extends Vue {
  get getCatsData(){
    // const уберем когда сюда что то поедет
    const catsData: {[key: string]: string} = {
      'Вердикт': 'Ошибка оформления кода. Подробнее ->',
      'Лог компиляции': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.\',Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempus, tellus eu scelerisque tincidunt, tortor lectus molestie odio, in sollicitudin justo lorem a eros.',
      'Время/Память': '100/100'
    }
    return catsData;
  }
}
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
