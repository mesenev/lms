<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class WeekDaysMixin extends Vue {
  monday_ = false;
  tuesday_ = false;
  wednesday_ = false;
  thursday_ = false;
  friday_ = false;
  saturday_ = false;
  sunday_ = false;

  newSchedule = {};

  get monday() {
    return this.monday_;
  }

  set monday(value: boolean) {
    this.monday_ = value;
    this.newSchedule = { ...this.newSchedule, 0: (value) ? '00:00' : null };
  }

  get tuesday() {
    return this.tuesday_;
  }

  set tuesday(value: boolean) {
    this.tuesday_ = value;
    this.newSchedule = { ...this.newSchedule, 1: (value) ? '00:00' : null };
  }

  get wednesday() {
    return this.wednesday_;
  }

  set wednesday(value: boolean) {
    this.wednesday_ = value;
    this.newSchedule = { ...this.newSchedule, 2: (value) ? '00:00' : null };
  }

  get thursday() {
    return this.thursday_;
  }

  set thursday(value: boolean) {
    this.thursday_ = value;
    this.newSchedule = { ...this.newSchedule, 3: (value) ? '00:00' : null };
  }

  get friday() {
    return this.friday_;
  }

  set friday(value: boolean) {
    this.friday_ = value;
    this.newSchedule = { ...this.newSchedule, 4: (value) ? '00:00' : null };
  }

  get saturday() {
    return this.saturday_;
  }

  set saturday(value: boolean) {
    this.saturday_ = value;
    this.newSchedule = { ...this.newSchedule, 5: (value) ? '00:00' : null };
  }

  get sunday() {
    return this.sunday_;
  }

  set sunday(value: boolean) {
    this.sunday_ = value;
    this.newSchedule = { ...this.newSchedule, 6: (value) ? '00:00' : null };
  }

}
</script>
