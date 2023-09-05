<script lang="ts">

import { computed, ref } from "vue";


export default function () {
  const monday_ = ref(false);
  const tuesday_ = ref(false);
  const wednesday_ = ref(false);
  const thursday_ = ref(false);
  const friday_ = ref(false);
  const saturday_ = ref(false);
  const sunday_ = ref(false);

  const newSchedule = ref({});

  const monday = computed({
      get: () => {
        return monday_.value
      },
      set: (value: boolean) => {
        monday_.value = value;
        newSchedule.value = { ...newSchedule, 0: (value) ? '00:00' : null };
      }
    }
  )

  const tuesday = computed({
      get: () => {
        return tuesday_.value
      },
      set: (value: boolean) => {
        tuesday_.value = value;
        newSchedule.value = { ...newSchedule, 1: (value) ? '00:00' : null };
      }
    }
  )

  const wednesday = computed({
      get: () => {
        return wednesday_.value
      },
      set: (value: boolean) => {
        wednesday_.value = value;
        newSchedule.value = { ...newSchedule, 2: (value) ? '00:00' : null };
      }
    }
  )

  const thursday = computed({
      get: () => {
        return thursday_.value
      },
      set: (value: boolean) => {
        thursday_.value = value;
        newSchedule.value = { ...newSchedule, 3: (value) ? '00:00' : null };
      }
    }
  )

  const friday = computed({
      get: () => {
        return friday_.value
      },
      set: (value: boolean) => {
        friday_.value = value;
        newSchedule.value = { ...newSchedule, 4: (value) ? '00:00' : null };
      }
    }
  )

  const saturday = computed({
      get: () => {
        return saturday_.value
      },
      set: (value: boolean) => {
        saturday_.value = value;
        newSchedule.value = { ...newSchedule, 5: (value) ? '00:00' : null };
      }
    }
  )

  const sunday = computed({
      get: () => {
        return sunday_.value
      },
      set: (value: boolean) => {
        sunday_.value = value;
        newSchedule.value = { ...newSchedule, 6: (value) ? '00:00' : null };
      }
    }
  )

  return {
    monday, tuesday, wednesday, thursday, friday, saturday, sunday
  }
}

</script>
