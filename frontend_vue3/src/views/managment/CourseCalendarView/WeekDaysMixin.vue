<script lang="ts" setup>
  import { computed } from 'vue';

  let monday_: boolean = false;
  let tuesday_: boolean = false;
  let wednesday_: boolean = false;
  let thursday_: boolean = false;
  let friday_: boolean = false;
  let saturday_: boolean = false;
  let sunday_: boolean = false;

  let newSchedule = {};

  const monday = computed({
    get(){
      return monday_;
    },
    set(value: boolean){
      monday_ = value;
      newSchedule = { ...newSchedule, 0: (value) ? '00:00' : null };
    }
  })

  const tuesday = computed({
    get(){
      return tuesday_;
    },
    set(value: boolean){
      tuesday_ = value;
      newSchedule = { ...newSchedule, 1: (value) ? '00:00' : null };
    }
  }) 

  const wednesday = computed({
    get(){
      return wednesday_;
    },
    set(value: boolean){
      wednesday_ = value;
      newSchedule = { ...newSchedule, 2: (value) ? '00:00' : null };
    }
  }); 

  const thursday = computed({
    get(){
      return _thursday
    },
    set(value: boolean){
      thursday_ = value;
      newSchedule = { ...newSchedule, 3: (value) ? '00:00' : null };
    }
  })

  const friday = computed({
    get(){
      return friday_;
    },
    set(value: boolean){
      friday_ = value;
      newSchedule = { ...newSchedule, 4: (value) ? '00:00' : null };
    }
  })

  const saturday = computed({
    get(){
      return saturday_;
    },
    set(value: boolean){
      saturday_ = value;
      newSchedule = { ...newSchedule, 5: (value) ? '00:00' : null };
    }
  })

  const sunday = computed({
    get(){
      return sunday_;
    },
    set(value: boolean){
      sunday_ = value;
      newSchedule = { ...newSchedule, 6: (value) ? '00:00' : null };
    }
  })

</script>
