<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class NotificationMixinComponent extends Vue {
  notificationKind = 'success';
  notificationText = '';
  showNotification = false;

  hideNotification() {
    this.showNotification = false;
  }
}
</script>
