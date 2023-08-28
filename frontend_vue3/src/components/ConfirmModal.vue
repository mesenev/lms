<template>
  <div>
    <cv-modal
      class="confirm--modal"
      :visible="modalVisible"
      :primary-button-disabled="inAction"
      size="small"
      @primary-click="approve"
      @modal-hidden="hideModal">
      <template v-slot:label>Подтверждение</template>
      <template v-slot:title>Вы уверены?</template>
      <template v-slot:content>
        <div>
          {{ text }}
        </div>
      </template>
      <template v-slot:primary-button>Подтвердить</template>
      <template v-slot:secondary-button>Отмена</template>
    </cv-modal>
  </div>
</template>

<script lang="ts" setup>

import { ref, watch } from "vue";

const props = defineProps({
  modalTrigger: { type: Boolean, required: true },
  text: { type: String, required: true },
  approveHandler: { type: Function, required: true }
})

const emits = defineEmits(['show-modal'])

const modalVisible = ref(false);
const inAction = ref(false);

watch(() => props.modalTrigger, () => {
  modalVisible.value = true;
})

function hideModal() {
  modalVisible.value = false;
  sideModalAction();
}

function sideModalAction() {
  emits('show-modal');
}

async function approve() {
  inAction.value = true;
  await props.approveHandler();
  inAction.value = false;
  hideModal();
}
</script>

<style scoped>

</style>
