<script setup lang="ts">
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
import { ref, type Ref } from 'vue'

let reactive_item: Ref<number> = ref(0)

const non_reactive_item = [1, 2, 3]


function method(){
  reactive_item.value++
}


</script>

<template>
  {{ reactive_item }}
  {{ non_reactive_item }}
  <button @click="method"></button>
</template>
