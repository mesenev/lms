<script lang="ts">

import {ref} from "vue";

export default function () {
  const notificationKind = ref('success');
  const notificationText = ref('');
  const showNotification = ref(false);

  function hideNotification() {
    showNotification.value = false;
  }

  return {
    notificationKind, notificationText, showNotification, hideNotification
  }
}
</script>
